#!/usr/bin/env python3
import argparse
import pandas as pd
import xlsxwriter
import re
import sys
import datetime

def clean_barcode(val):
    """Safely converts potential scientific notation floats back to string barcodes."""
    if pd.isna(val):
        return ""
    try:
        val_float = float(val)
        if val_float.is_integer():
            return str(int(val_float))
        return str(val_float)
    except ValueError:
        return str(val).strip()

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

def process_file(input_file):
    """Reads CSV/XLSX, handles multi-sheet mapping, filters noise, and logs flags."""
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
        'call_number': ['call number', 'classmark', 'call_number'],
        'page_count': ['page count', 'pages', 'estimated_page_count'],
        'condition': ['condition'],
        'notes': ['notes'],
        'date_vol': ['date/volume', 'volume', 'date'],
        'bound_unbound': ['bound/unbound'],
        'format': ['format', 'item format', 'item_format', 'type'],
        'size': ['size', 'dimensions', 'length', 'feet', 'ft', 'physical size']
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
        call_num = get_val(*known_mappings['call_number'])
        page_count = clean_page_count(get_val(*known_mappings['page_count']))
        condition = get_val(*known_mappings['condition'])
        notes = get_val(*known_mappings['notes'])
        date_vol = clean_unit_title(get_val(*known_mappings['date_vol']))
        bound_unbound = get_val(*known_mappings['bound_unbound']).lower()
        fmt = get_val(*known_mappings['format'])
        size = get_val(*known_mappings['size'])
        
        # Drop summary rows silently (e.g., "Total: 52 titles")
        if re.match(r'^total:\s*\d+', raw_title, re.IGNORECASE) or re.match(r'^total:\s*\d+', date_vol, re.IGNORECASE):
            continue

        # Update running title for hierarchical forward-filling
        if raw_title:
            current_title = raw_title
            
        # Check if this row actually contains item-level data
        has_item_data = any([barcode, call_num, page_count, condition, notes, date_vol, size])
        
        # Issue #3: If a row has NO item data (only a title, or completely blank), skip & flag it
        if not has_item_data:
            if raw_title:
                print(f"  [HEADER/SKIP] Sheet '{source_sheet}': Row has Title ('{raw_title}') but no item info. Saved as parent header & skipped in output.")
            continue
            
        # Issue #3: If an item IS being included but lacks a barcode, flag it!
        if not barcode:
            print(f"  [FLAG: NO BARCODE] Sheet '{source_sheet}': Included item with blank barcode | Title: '{current_title}' | Vol/Date: '{date_vol}' | Call Num: '{call_num}'")
            
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

        # Issue #1: Robust Microform vs. Reflective detection
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
            
        mapped_row = {
            'schema_version': '1.0.0',
            'project_code': '',
            'barcode': barcode,
            'division_code': '', 
            'bnumber': '',
            'classmark': call_num,
            'aspace_component_id': '',
            'collection_id': '',
            'item_title': current_title,
            'object_type': obj_type,
            'object_format': obj_format,
            'physical_condition_notes': phys_notes_str,
            'unit_index': '',
            'unit_title': date_vol,
            '[INFO] estimated_page_count': page_count,
            '[INFO] is_oversized': is_oversized
        }
        mapped_data.append(mapped_row)
        
    print("-----------------------------\n")
    return mapped_data

def write_output(mapped_data, output_file):
    """Writes the mapped data into the validated XLSX template structure."""
    workbook = xlsxwriter.Workbook(output_file)
    worksheet = workbook.add_worksheet('Inventory')
    vocab_sheet = workbook.add_worksheet('Vocab (Hidden)')
    vocab_sheet.hide()

    headers = [
        'schema_version', 'project_code', 'barcode', 'division_code', 
        'bnumber', 'classmark', 'aspace_component_id', 'collection_id', 
        'item_title', 'object_type', 'object_format', 'physical_condition_notes', 
        'unit_index', 'unit_title', '[INFO] estimated_page_count', '[INFO] is_oversized'
    ]

    header_format = workbook.add_format({'bold': True, 'bg_color': '#E0E0E0', 'border': 1})
    info_header_format = workbook.add_format({'bold': True, 'bg_color': '#FFF2CC', 'border': 1})

    for col_num, header in enumerate(headers):
        if header.startswith('[INFO]'):
            worksheet.write(0, col_num, header, info_header_format)
        else:
            worksheet.write(0, col_num, header, header_format)

    worksheet.set_column('A:P', 22)

    vocab = {
        "reflective textual and graphic": ["bound volume", "loose paper"],
        "reflective photographic": ["photographic print"],
        "transmissive photographic": ["black-and-white negative", "color negative", "color transparency", "mounted slide"],
        "glass substrate": ["glass plate negative", "lantern slide"],
        "microform": ["16mm roll microfilm", "35mm roll microfilm", "microfiche", "aperture card"]
    }

    row = 0
    for obj_type, formats in vocab.items():
        safe_name = re.sub(r'[^a-zA-Z0-9_]', '_', obj_type)
        vocab_sheet.write(row, 0, obj_type)
        for col, fmt in enumerate(formats):
            vocab_sheet.write(row, col + 1, fmt)
        start_cell = xlsxwriter.utility.xl_rowcol_to_cell(row, 1, row_abs=True, col_abs=True)
        end_cell = xlsxwriter.utility.xl_rowcol_to_cell(row, len(formats), row_abs=True, col_abs=True)
        workbook.define_name(safe_name, f"='Vocab (Hidden)'!{start_cell}:{end_cell}")
        row += 1

    end_type_cell = xlsxwriter.utility.xl_rowcol_to_cell(row - 1, 0, row_abs=True, col_abs=True)
    workbook.define_name('ObjectTypes', f"='Vocab (Hidden)'!$A$1:{end_type_cell}")

    # Set up dependent validations
    worksheet.data_validation('J2:J1048576', {'validate': 'list', 'source': '=ObjectTypes'})
    for i in range(2, 2001):  # Apply dependent validation to first 2000 rows
        worksheet.data_validation(f'K{i}', {'validate': 'list', 'source': f'=INDIRECT(SUBSTITUTE(J{i}, " ", "_"))'})

    # Write the data
    for row_num, row_data in enumerate(mapped_data, start=1):
        for col_num, header in enumerate(headers):
            val = row_data.get(header, "")
            if header == '[INFO] estimated_page_count' and str(val).isdigit():
                worksheet.write_number(row_num, col_num, int(val))
            else:
                worksheet.write_string(row_num, col_num, str(val))

    workbook.close()

def main():
    parser = argparse.ArgumentParser(
        description='Map legacy spreadsheet data to the digitization inventory template.'
    )
    parser.add_argument('-i', '--input', required=True, help='Input CSV or XLSX file')
    parser.add_argument('-o', '--output', required=True, help='Output XLSX file')
    args = parser.parse_args()

    print(f"Reading and mapping data from '{args.input}'...")
    try:
        mapped_data = process_file(args.input)
        print(f"Successfully processed {len(mapped_data)} item rows.")
        
        write_output(mapped_data, args.output)
        print(f"Successfully wrote mapped template to '{args.output}'")
    except Exception as e:
        print(f"Error: {e}")
        sys.exit(1)

if __name__ == '__main__':
    main()