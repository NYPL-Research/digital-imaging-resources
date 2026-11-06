#!/usr/bin/env python3

import os
import sys
import pandas as pd
from pyairtable import Api
from openpyxl.utils import get_column_letter

# Load credentials
TOKEN = os.getenv('AIRTABLE_TOKEN')
BASE_ID = os.getenv('AIRTABLE_BASE_ID')
TABLE_NAME = os.getenv('AIRTABLE_TABLE_NAME')

if not all([TOKEN, BASE_ID, TABLE_NAME]):
    print("❌ Error: Missing credentials in environment.")
    sys.exit(1)

api = Api(TOKEN)

# ==========================================
# 1. Fetch Main Table Data
# ==========================================
print(f"Fetching main table: {TABLE_NAME}...")
main_table = api.table(BASE_ID, TABLE_NAME)
records = main_table.all()

data = [record['fields'] for record in records]
df = pd.DataFrame(data)

# Convert lists (like multiple-selects or linked records) to comma-separated strings
for col in df.columns:
    df[col] = df[col].apply(lambda x: ', '.join(map(str, x)) if isinstance(x, list) else x)

# ==========================================
# 2. Fetch Linked Table and Resolve IDs
# ==========================================
LINKED_TABLE_NAME = 'Formats'
PRIMARY_FIELD_NAME = 'Format'

print(f"Fetching linked table '{LINKED_TABLE_NAME}' to resolve names...")
try:
    linked_table = api.table(BASE_ID, LINKED_TABLE_NAME)
    linked_records = linked_table.all()
    
    # Create mapping dictionary: {'rec123...': 'Audio Tape', 'rec456...': 'VHS'}
    id_to_name = {r['id']: r['fields'].get(PRIMARY_FIELD_NAME, 'Unknown Name') for r in linked_records}
    
    def swap_ids_for_names(val):
        if not isinstance(val, str) or 'rec' not in val:
            return val
            
        # Split by comma in case there are multiple linked records in one cell
        ids = [i.strip() for i in val.split(',')]
        
        # Swap the ID for the name if it exists in our dictionary
        names = [id_to_name.get(i, i) for i in ids]
        return ', '.join(names)

    # Apply the swap function to the "Format grouping" column
    if 'Format grouping' in df.columns:
        df['Format grouping'] = df['Format grouping'].apply(swap_ids_for_names)
        print("Successfully resolved 'Format grouping' IDs to text.")
except Exception as e:
    print(f"⚠️ Could not resolve linked records. Error: {e}")

# ==========================================
# 3. Clean Data and Export to Excel
# ==========================================
# Handle cases where 'LPA Division' might be empty
if 'LPA Division' not in df.columns:
    df['LPA Division'] = 'Unknown'
df['LPA Division'] = df['LPA Division'].fillna('Uncategorized')

output_file = 'LPA_Divisions_Export.xlsx'
print(f"Generating {output_file}...")

with pd.ExcelWriter(output_file, engine='openpyxl') as writer:
    divisions = df['LPA Division'].unique()
    
    for division in divisions:
        # Filter for current division
        division_df = df[df['LPA Division'] == division]
        
        # Clean sheet name (31 char limit, no special characters)
        safe_sheet_name = str(division).replace('/', '-').replace('\\', '-')[:31]
        
        # Write to sheet
        division_df.to_excel(writer, sheet_name=safe_sheet_name, index=False)
        
        # Auto-size columns
        worksheet = writer.sheets[safe_sheet_name]
        for idx, col_name in enumerate(division_df.columns, start=1):
            col_data_len = division_df[col_name].astype(str).map(len).max()
            header_len = len(str(col_name))
            max_len = max(col_data_len, header_len)
            
            # Add padding, cap width at 50
            adjusted_width = min(max_len + 2, 50)
            col_letter = get_column_letter(idx)
            worksheet.column_dimensions[col_letter].width = adjusted_width
            
        print(f" - Created sheet '{safe_sheet_name}' with {len(division_df)} rows.")

print("✅ Export complete!")