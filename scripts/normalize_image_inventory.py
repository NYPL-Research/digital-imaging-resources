#!/usr/bin/env python3
import argparse
import pandas as pd
import build_inventory_template
import xlsxwriter
import re
import sys
import os
import datetime
import logging
from bookops_nypl_platform import PlatformSession, PlatformToken

def setup_logging():
    """Sets up basic logging output."""
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(levelname)s - %(message)s'
    )

def init_platform_session() -> PlatformSession | None:
    """
    Attempts to initialize a Platform API session using environment variables.
    Returns None if credentials are missing or authentication fails.
    """
    client_id = os.getenv("OAUTH_CLIENT_ID")
    client_secret = os.getenv("OAUTH_CLIENT_SECRET")
    oauth_server = os.getenv("OAUTH_SERVER")

    if not (client_id and client_secret and oauth_server):
        logging.info("Platform API credentials not fully set in environment. Skipping API bnumber lookups.")
        return None

    try:
        token = PlatformToken(
            client_id=client_id,
            client_secret=client_secret,
            oauth_server=oauth_server
        )
        session = PlatformSession(authorization=token)
        logging.info("Successfully connected to NYPL Platform API for B-number enrichment.")
        return session
    except Exception as e:
        logging.warning(f"Failed to authenticate with Platform API: {e}. Proceeding without API lookups.")
        return None

def fetch_bnumber_for_barcode(session: PlatformSession, barcode: str, cache: dict) -> tuple:
    """
    Queries the Platform API for a barcode and returns the formatted b-number and call number.
    Uses an in-memory cache to avoid duplicate API calls.
    """
    if not barcode or not session:
        return "", ""

    if barcode in cache:
        return cache[barcode]

    try:
        response = session.get_item_list(barcode=barcode)
        if response.status_code == 200:
            data = response.json()
            items = data.get("data", [])
            if items:
                item = items[0]
                bib_ids = item.get("bibIds", [])
                bnumber = ""
                if bib_ids:
                    raw_bib = str(bib_ids[0])
                    bnumber = f"b{raw_bib}" if not raw_bib.startswith("b") else raw_bib
                call_number = item.get("callNumber", "")
                result = (bnumber, call_number)
                cache[barcode] = result
                return result
        
        # If no match or status code wasn't 200
        cache[barcode] = ("", "")
        return ("", "")
    except Exception as e:
        logging.warning(f"API query failed for barcode {barcode}: {e}")
        cache[barcode] = ("", "")
        return ("", "")

def clean_barcode(val):
    """Safely converts potential scientific notation floats back to string barcodes."""
    if pd.isna(val):
        return ""
        
    val_str = str(val).strip()
    if val_str.lower() in ["no barcode", "none", "n/a", "missing"]:
        return ""
        
    try:
        val_float = float(val)
        if val_float.is_integer():
            return str(int(val_float))
        return str(val_float)
    except ValueError:
        return val_str

def clean_unit_title(val):
    """Prevents Excel/pandas from turning strings like 'Oct. 1908' into timestamps."""
    if pd.isna(val) or str(val).strip() == "":
        return ""
    
    months = {
        1: 'Jan.', 2: 'Feb.', 3: 'March', 4: 'April', 5: 'May', 6: 'June',
        7: 'July', 8: 'Aug.', 9: 'Sept.', 10: 'Oct.', 11: 'Nov.', 12: 'Dec.'
    }
    
    if isinstance(val, (pd.Timestamp, datetime.datetime)):
        return f"{months.get(val.month, '')} {val.year}".strip()
        
    val_str = str(val).strip()
    match = re.match(r'^(\d{4})-(\d{2})-\d{2}(?:\s+00:00:00)?$', val_str)
    if match:
        year, month = int(match.group(1)), int(match.group(2))
        return f"{months.get(month, '')} {year}".strip()
        
    return val_str

def clean_page_count(val):
    """Extracts clean integer page counts from floats ('48.0') and text ('Approx 600')."""
    if pd.isna(val) or str(val).strip() == "":
        return ""
        
    val_str = str(val).replace(',', '').strip()
    
    try:
        val_float = float(val_str)
        if val_float.is_integer():
            return str(int(val_float))
        return str(val_float)
    except ValueError:
        pass
        
    match = re.search(r'(\d+(?:\.\d+)?)', val_str)
    if match:
        num_str = match.group(1)
        try:
            val_float = float(num_str)
            if val_float.is_integer():
                return str(int(val_float))
            return str(val_float)
        except ValueError:
            return num_str
            
    return val_str

def process_file(input_file, platform_session=None, project_code="", funding_source=""):
    """Reads CSV/XLSX, handles multi-sheet mapping, filters noise, queries API, and logs flags."""
    # 1. Read input file and track source sheet names
    if input_file.lower().endswith('.csv'):
        df = pd.read_csv(input_file)
        df['_source_sheet'] = 'CSV'
    elif input_file.lower().endswith('.xlsx'):
        sheets = pd.read_excel(input_file, sheet_name=None)
        df_list = []
        for sheet_name, sheet_df in sheets.items():
            sheet_df['_source_sheet'] = str(sheet_name)
            df_list.append(sheet_df)
        df = pd.concat(df_list, ignore_index=True)
    else:
        raise ValueError("Input file must be .csv or .xlsx")

    # 2. Standardize column names for fuzzy matching
    col_map = {str(col).strip().lower(): col for col in df.columns}
    
    # Define known mappings (lowercase stripped)
    known_mappings = {
        'title': ['title', 'item_title', 'item title'],
        'barcode': ['barcode'],
        'bnumber': ['bnumber', 'b-number', 'bib_id', 'bib id', 'b_number'],
        'call_number': ['call number', 'classmark', 'call_number'],
        'page_count': ['page count', 'pages', 'estimated_page_count'],
        'condition': ['condition'],
        'notes': ['notes'],
        'date_vol': ['date/volume', 'volume', 'date'],
        'bound_unbound': ['bound/unbound'],
        'format': ['format', 'item format', 'item_format', 'type'],
        'size': ['size', 'dimensions', 'length', 'feet', 'ft', 'physical size'],
        'cataloging': ['cataloging', 'cataloguing'],
        'funding_source': ['funding source', 'funding_source', 'funding']
    }
    
    # 3. Identify and warn about unmapped columns
    all_known_aliases = {alias for aliases in known_mappings.values() for alias in aliases}
    unmapped_cols = [
        orig_col for lower_col, orig_col in col_map.items() 
        if lower_col not in all_known_aliases and lower_col != '_source_sheet'
    ]
    
    if unmapped_cols:
        print("\n[WARNING] The following columns from your input sheet are NOT mapped to the template:")
        for col in unmapped_cols:
            print(f"  -> '{col}'")
        print("Data in these columns will be excluded from the output. If you need this data, please map it!\n")

    mapped_data = []
    current_title = ""
    barcode_api_cache = {}
    
    print("--- Processing Audit Log ---")
    
    # 4. Process row by row
    for _, row in df.iterrows():
        def get_val(*possible_names):
            for name in possible_names:
                if name in col_map:
                    val = row[col_map[name]]
                    if pd.notna(val) and str(val).strip() != "":
                        return str(val).strip()
            return ""

        source_sheet = str(row.get('_source_sheet', '')).strip()
        raw_title = get_val(*known_mappings['title'])
        barcode = clean_barcode(get_val(*known_mappings['barcode']))
        existing_bnumber = get_val(*known_mappings['bnumber'])
        call_num = get_val(*known_mappings['call_number'])
        page_count = clean_page_count(get_val(*known_mappings['page_count']))
        condition = get_val(*known_mappings['condition'])
        notes = get_val(*known_mappings['notes'])
        date_vol = clean_unit_title(get_val(*known_mappings['date_vol']))
        bound_unbound = get_val(*known_mappings['bound_unbound']).lower()
        fmt = get_val(*known_mappings['format'])
        size = get_val(*known_mappings['size'])
        cataloging_val = get_val(*known_mappings.get('cataloging', []))
        funding_val = get_val(*known_mappings.get('funding_source', []))
        
        final_funding = funding_val if funding_val else funding_source
        
        # Drop summary rows silently (e.g., "Total: 52 titles")
        if re.match(r'^total:\s*\d+', raw_title, re.IGNORECASE) or re.match(r'^total:\s*\d+', date_vol, re.IGNORECASE):
            continue

        # Update running title for hierarchical forward-filling
        if raw_title:
            current_title = raw_title
            
        # Check if this row actually contains item-level data
        has_item_data = any([barcode, call_num, page_count, condition, notes, date_vol, size])
        
        # If a row has NO item data (only a title, or completely blank), skip & flag it
        if not has_item_data:
            if raw_title:
                print(f"  [HEADER/SKIP] Sheet '{source_sheet}': Row has Title ('{raw_title}') but no item info. Saved as parent header & skipped in output.")
            continue
            
        # If an item IS being included but lacks a barcode, flag it!
        if not barcode:
            print(f"  [FLAG: NO BARCODE] Sheet '{source_sheet}': Included item with blank barcode | Title: '{current_title}' | Vol/Date: '{date_vol}' | Call Num: '{call_num}'")
            bnumber = existing_bnumber
        else:
            bnumber = existing_bnumber
            if platform_session and (not bnumber or not call_num):
                api_bnumber, api_call_num = fetch_bnumber_for_barcode(platform_session, barcode, barcode_api_cache)
                if not bnumber:
                    bnumber = api_bnumber
                if not call_num:
                    call_num = api_call_num

        # Combine condition, notes, and size safely
        phys_notes = []
        if condition: phys_notes.append(condition)
        if notes: phys_notes.append(notes)
        if size: phys_notes.append(f"Size: {size}")
        phys_notes_str = " ".join(phys_notes)
        
        # Regex for Oversize
        is_oversized = ""
        combined_text_for_size = f"{fmt} {phys_notes_str} {bound_unbound}"
        if re.search(r'oversize[d]?', combined_text_for_size, re.IGNORECASE):
            is_oversized = "Yes"

        # Microform vs. Reflective detection
        is_microform = (
            'micro' in source_sheet.lower() or
            'micro' in fmt.lower() or
            'reel' in fmt.lower() or
            re.search(r'\b\d+\s*(?:ft|feet)\b', str(size).lower()) is not None or
            re.search(r'\bmicro(?:film|fiche|form)?\b', f"{notes} {condition}".lower()) is not None
        )
        
        if is_microform:
            obj_type = "microform"
            if '16mm' in combined_text_for_size.lower():
                obj_format = "16mm roll microfilm"
            elif 'fiche' in combined_text_for_size.lower():
                obj_format = "microfiche"
            elif 'aperture' in combined_text_for_size.lower():
                obj_format = "aperture card"
            else:
                obj_format = "35mm roll microfilm"  # Default archival microfilm standard
        elif bound_unbound == 'unbound':
            obj_type = "reflective textual and graphic"
            obj_format = "loose paper"
        else:
            obj_type = "reflective textual and graphic"
            obj_format = "bound volume"
            
        needs_cataloging = "Yes" if cataloging_val.lower() in ['y', 'yes', 'true'] else ""
            
        mapped_row = {
            'barcode': barcode,
            'item_title': current_title,
            'project_code': project_code,
            'funding_source': final_funding,
            'collection_id': '',
            'division_code': '', 
            'shelf_locator': call_num,
            'bnumber': bnumber,
            'object_type': obj_type,
            'object_format': obj_format,
            'aspace_component_id': '',
            'physical_condition_notes': phys_notes_str,
            'unit_index': '',
            'unit_title': date_vol,
            '[INFO] estimated_page_count': page_count,
            '[INFO] is_oversized': is_oversized,
            '[INFO] needs_cataloging': needs_cataloging
        }
        mapped_data.append(mapped_row)
        
    print("-----------------------------\n")
    return mapped_data

def write_output(mapped_data, output_file):
    """Writes the mapped data into the validated XLSX template structure."""
    build_inventory_template.generate_inventory_template(output_filename=output_file, inventory_data=mapped_data)

def main():
    setup_logging()
    
    parser = argparse.ArgumentParser(
        description='Map legacy spreadsheet data to the digitization inventory template.'
    )
    parser.add_argument('-i', '--input', required=True, help='Input CSV or XLSX file')
    parser.add_argument('-o', '--output', required=True, help='Output XLSX file')
    parser.add_argument('-p', '--project-code', default='', help='Project code to apply to all items')
    parser.add_argument('-f', '--funding-source', default='', help='Funding source to apply to all items')
    args = parser.parse_args()

    # Initialize Platform Session if environment variables exist
    platform_session = init_platform_session()

    print(f"Reading and mapping data from '{args.input}'...")
    try:
        mapped_data = process_file(args.input, platform_session=platform_session, project_code=args.project_code, funding_source=args.funding_source)
        print(f"Successfully processed {len(mapped_data)} item rows.")
        
        write_output(mapped_data, args.output)
        print(f"Successfully wrote mapped template to '{args.output}'")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()