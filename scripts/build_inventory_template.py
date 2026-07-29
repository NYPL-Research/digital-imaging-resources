#!/usr/bin/env python3
"""
NYPL Vendor Digital Imaging — Inventory Metadata Template Generator (v4)
Generates a schema-compliant Excel workbook with:
  1. Instructions & Guidelines tab (Active on open, includes Division Code lookup table)
  2. Inventory Template tab (3-row header block, 100 pre-formatted data entry rows & drop-downs)
  3. Hidden Schema Reference tab (Source data for dependent drop-down validation)
"""

import openpyxl
from openpyxl.styles import Font, PatternFill, Alignment, Border, Side
from openpyxl.worksheet.datavalidation import DataValidation
from openpyxl.utils import get_column_letter
from openpyxl.workbook.defined_name import DefinedName

def generate_inventory_template(output_filename="NYPL_Vendor_Digital_Imaging_Inventory_Template.xlsx"):
    wb = openpyxl.Workbook()

    # Setup sheets
    ws_inst = wb.active
    ws_inst.title = "Instructions & Guidelines"
    ws_template = wb.create_sheet(title="Inventory Template")
    ws_ref = wb.create_sheet(title="Schema Reference")

    # Enable gridlines on visible sheets
    ws_inst.views.sheetView[0].showGridLines = True
    ws_template.views.sheetView[0].showGridLines = True
    ws_ref.views.sheetView[0].showGridLines = True

    # ==============================================================================
    # --- 1. BUILD INSTRUCTIONS & GUIDELINES SHEET ---
    # ==============================================================================
    ws_inst.merge_cells("A1:G1")
    ws_inst["A1"] = "NYPL VENDOR DIGITAL IMAGING — INSTRUCTIONS & GUIDELINES"
    ws_inst["A1"].font = Font(name="Calibri", size=16, bold=True, color="FFFFFF")
    ws_inst["A1"].fill = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
    ws_inst["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws_inst.row_dimensions[1].height = 40

    ws_inst.merge_cells("A2:G2")
    ws_inst["A2"] = "Best Practices, Requirements, and Schema Guidelines for Completing Digitization Inventories"
    ws_inst["A2"].font = Font(name="Calibri", size=11, italic=True, color="FFFFFF")
    ws_inst["A2"].fill = PatternFill(start_color="334155", end_color="334155", fill_type="solid")
    ws_inst["A2"].alignment = Alignment(horizontal="center", vertical="center")
    ws_inst.row_dimensions[2].height = 24

    ws_inst.row_dimensions[3].height = 14 # Spacer

    def add_inst_section(ws, start_row, title, items, header_fill="0F766E", row_height=30):
        """Helper to build formatted guideline sections."""
        ws.merge_cells(start_row=start_row, start_column=1, end_row=start_row, end_column=7)
        c_head = ws.cell(row=start_row, column=1, value=title)
        c_head.font = Font(name="Calibri", size=12, bold=True, color="FFFFFF")
        c_head.fill = PatternFill(start_color=header_fill, end_color=header_fill, fill_type="solid")
        c_head.alignment = Alignment(horizontal="left", vertical="center", indent=1)
        ws.row_dimensions[start_row].height = 28
        
        current_row = start_row + 1
        for label, desc in items:
            ws.row_dimensions[current_row].height = row_height
            
            # Label cell (Col A)
            c_lbl = ws.cell(row=current_row, column=1, value=label)
            c_lbl.font = Font(name="Calibri", size=10, bold=True, color="1E293B")
            c_lbl.fill = PatternFill(start_color="F8FAFC" if current_row%2==0 else "FFFFFF", end_color="F8FAFC" if current_row%2==0 else "FFFFFF", fill_type="solid")
            c_lbl.alignment = Alignment(horizontal="left", vertical="top" if row_height >= 30 else "center", wrap_text=True)
            c_lbl.border = Border(left=Side(style='medium', color='CBD5E1'), top=Side(style='thin', color='E2E8F0'), bottom=Side(style='thin', color='E2E8F0'), right=Side(style='thin', color='E2E8F0'))
            
            # Description cells merged (Col B to G)
            ws.merge_cells(start_row=current_row, start_column=2, end_row=current_row, end_column=7)
            c_desc = ws.cell(row=current_row, column=2, value=desc)
            c_desc.font = Font(name="Calibri", size=10, color="334155")
            c_desc.fill = PatternFill(start_color="F8FAFC" if current_row%2==0 else "FFFFFF", end_color="F8FAFC" if current_row%2==0 else "FFFFFF", fill_type="solid")
            c_desc.alignment = Alignment(horizontal="left", vertical="top" if row_height >= 30 else "center", wrap_text=True)
            
            for col_i in range(2, 8):
                c_temp = ws.cell(row=current_row, column=col_i)
                right_side = Side(style='medium', color='CBD5E1') if col_i == 7 else Side(style='thin', color='E2E8F0')
                c_temp.border = Border(top=Side(style='thin', color='E2E8F0'), bottom=Side(style='thin', color='E2E8F0'), right=right_side)
                
            current_row += 1
        
        ws.row_dimensions[current_row].height = 14 # Bottom spacer
        return current_row + 1

    # Section 1: Scoping & Purpose
    sec1_items = [
        ("Purpose & Vendor Estimates", "This inventory directly informs vendor scoping, equipment preparation, and cost estimates. It is vital that this spreadsheet be filled out as completely and accurately as possible."),
        ("Completeness vs. Mandatory Fields", "Not every field is strictly required! Notice rows 5 and 6 of the template indicate REQUIRED vs OPTIONAL status and provide field descriptions. If optional metadata exists in your records, please include it!"),
        ("Internal Tracking Fields", "You do NOT need to fill out 'project_code' (Col C) if it is unassigned. The Vendor Digitization Services team will verify/complete internal tracking codes before submitting the inventory to a vendor.")
    ]
    r = add_inst_section(ws_inst, 4, "1. GENERAL PURPOSE & SCOPING GUIDELINES", sec1_items, "0F766E")

    # Section 2: Granularity & Barcodes (Amber Header for Critical Rules)
    sec2_items = [
        ("One Row per Physical Item", "Each physical item being digitized (e.g., each bound volume, box, folder, reel, or photograph) MUST get its own dedicated row. If multiple physical items belong to a single catalog record ('bnumber') or finding aid component, create separate rows for each physical item and repeat/reuse the 'bnumber' or 'shelf_locator' across those rows."),
        ("Multi-Work Bound Volumes", "If you know upfront that a single physical volume contains multiple distinct intellectual works that must be delivered as separate digital packages, create one row per intellectual unit, repeat the barcode across rows, and assign sequential unit indexes and titles."),
        ("Mandatory Barcodes", "Every item scheduled for digitization requires a valid 14-digit barcode ('barcode' - Col A) or the project cannot be initiated! If your items lack barcodes or if you require assistance with barcoding workflows, please contact the Vendor Digitization Services team.")
    ]
    r = add_inst_section(ws_inst, r, "2. ITEM-LEVEL GRANULARITY & BARCODE REQUIREMENTS (CRITICAL)", sec2_items, "B45309")

    # Section 3: Dropdown consistency
    sec3_items = [
        ("Use Drop-Down Menus", "To ensure data consistency and schema compliance, always use the built-in drop-down menus for 'division_code' (Col E), 'object_type' (Col H), and 'object_format' (Col I). Do not type manual overrides."),
        ("Curatorial Identifier Order", "Notice that 'division_code' (Col E), 'shelf_locator' (Col F), and 'bnumber' (Col G) are grouped logically together so you can log your core curatorial and catalog citations in sequence."),
        ("Dependent Format Filtering", "Notice that the options in the 'object_format' drop-down (Col I) automatically filter to match the top-level 'object_type' you select in Column H (e.g., selecting 'microform' will only display microform formats).")
    ]
    r = add_inst_section(ws_inst, r, "3. SCHEMA VALIDATION & DROP-DOWN CONSISTENCY", sec3_items, "0F766E")

    # Section 4: [INFO] Gold Headers
    sec4_items = [
        ("Why They Are Yellow", "Columns N ('[INFO] estimated_page_count'), O ('[INFO] is_oversized'), and P ('[INFO] needs_cataloging') are highlighted with a distinct yellow/gold header to differentiate them from archival metadata."),
        ("Purpose of [INFO] Fields", "This data is NOT retained in final archival digital packages or sidecars. However, it is essential for vendor cost estimates, sizing timelines, and capture equipment allocation—so please fill out these fields whenever possible! Use the 'needs_cataloging' dropdown (TRUE/FALSE) to flag items requiring metadata enhancement.")
    ]
    r = add_inst_section(ws_inst, r, "4. VENDOR ESTIMATE [INFO] FIELDS (YELLOW HIGHLIGHTS)", sec4_items, "D97706")

    # Section 5: Curatorial Division Codes
    div_items = [
        ("THE", "Billy Rose Theatre Division"),
        ("DAN", "Jerome Robbins Dance Division"),
        ("MUS", "Music Division"),
        ("RHA", "Rodgers and Hammerstein Archives of Recorded Sound"),
        ("TOFT", "Theatre on Film and Tape Archive"),
        ("BRG", "Berg Collection"),
        ("JWS", "Dorot Jewish Division"),
        ("GRD", "General Research Division"),
        ("ARN", "George Arents Collection"),
        ("MSS", "Manuscripts and Archives Division"),
        ("MAP", "Map Division"),
        ("LHG", "Milstein Division"),
        ("NYPLA", "NYPL Archives"),
        ("CPS", "Pforzheimer Collection"),
        ("RBK", "Rare Book Division"),
        ("ART", "Wallach Division: Art & Architecture Collection"),
        ("PHG", "Wallach Division: Photography Collection"),
        ("MMPC", "Wallach Division: Picture Collection"),
        ("PRN", "Wallach Division: Print Collection"),
        ("SPN", "Wallach Division: Spencer Collection"),
        ("SCF", "Schomburg Art and Artifacts Division"),
        ("SCR", "Schomburg Jean Blackwell Hutson Research and Reference Division"),
        ("SCM", "Schomburg Manuscripts, Archives and Rare Books Division"),
        ("SCL", "Schomburg Moving Image and Recorded Sound Division"),
        ("SCG", "Schomburg Photographs and Prints Division")
    ]
    r = add_inst_section(ws_inst, r, "5. CURATORIAL DIVISION CODES (COLUMN E DROPDOWN REFERENCE)", div_items, "1E40AF", row_height=22)

    # Auto-fit Instructions column widths
    ws_inst.column_dimensions["A"].width = 28
    for c_idx in range(2, 8):
        ws_inst.column_dimensions[get_column_letter(c_idx)].width = 16

    # ==============================================================================
    # --- 2. BUILD SCHEMA REFERENCE SHEET (HIDDEN ARCHITECTURE) ---
    # ==============================================================================
    ws_ref.merge_cells("A1:H1")
    ws_ref["A1"] = "NYPL Digitized Image Schema — Dependent Dropdown Source Data"
    ws_ref["A1"].font = Font(name="Calibri", size=14, bold=True, color="FFFFFF")
    ws_ref["A1"].fill = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
    ws_ref["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws_ref.row_dimensions[1].height = 35

    ref_headers = [
        "Object Types", 
        "reflective textual and graphic", 
        "reflective photographic", 
        "transmissive photographic", 
        "glass substrate", 
        "microform",
        "Oversized / Boolean Flags",
        "Division Codes"
    ]

    ws_ref.row_dimensions[3].height = 24
    for col_idx, header in enumerate(ref_headers, 1):
        c = ws_ref.cell(row=3, column=col_idx, value=header)
        c.font = Font(name="Calibri", size=10, bold=True, color="FFFFFF")
        c.fill = PatternFill(start_color="0F766E", end_color="0F766E", fill_type="solid")
        c.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        c.border = Border(left=Side(style='thin', color='CBD5E1'), right=Side(style='thin', color='CBD5E1'), top=Side(style='medium', color='1E293B'), bottom=Side(style='medium', color='1E293B'))

    object_types = [
        "reflective textual and graphic",
        "reflective photographic",
        "transmissive photographic",
        "glass substrate",
        "microform"
    ]

    formats_dict = {
        "reflective textual and graphic": ["bound volume", "loose paper"],
        "reflective photographic": ["photographic print"],
        "transmissive photographic": ["black-and-white negative", "color negative", "color transparency", "mounted slide"],
        "glass substrate": ["glass plate negative", "lantern slide"],
        "microform": ["16mm roll microfilm", "35mm roll microfilm", "microfiche", "aperture card"]
    }

    boolean_flags = ["TRUE", "FALSE"]
    division_codes = [code for code, name in div_items]

    # Write Object Types
    for idx, val in enumerate(object_types, start=4):
        c = ws_ref.cell(row=idx, column=1, value=val)
        c.font = Font(name="Calibri", size=10, bold=True, color="1E293B")
        c.fill = PatternFill(start_color="EFF6FF", end_color="EFF6FF", fill_type="solid")

    # Write Formats mapped to their respective columns
    col_map = {
        "reflective textual and graphic": 2,
        "reflective photographic": 3,
        "transmissive photographic": 4,
        "glass substrate": 5,
        "microform": 6
    }

    for obj_type, formats in formats_dict.items():
        col_num = col_map[obj_type]
        for idx, fmt in enumerate(formats, start=4):
            c = ws_ref.cell(row=idx, column=col_num, value=fmt)
            c.font = Font(name="Calibri", size=10, color="334155")

    # Write Boolean Flags (Col 7)
    for idx, flag in enumerate(boolean_flags, start=4):
        c = ws_ref.cell(row=idx, column=7, value=flag)
        c.font = Font(name="Calibri", size=10, bold=True, color="1E293B")
        c.alignment = Alignment(horizontal="center")

    # Write Division Codes (Col 8)
    for idx, code in enumerate(division_codes, start=4):
        c = ws_ref.cell(row=idx, column=8, value=code)
        c.font = Font(name="Calibri", size=10, bold=True, color="1E293B")
        c.alignment = Alignment(horizontal="center")

    # Define Workbook-Level Named Ranges for INDIRECT lookup formulas and dropdowns
    wb.defined_names.add(DefinedName("object_type_list", attr_text="'Schema Reference'!$A$4:$A$8"))
    wb.defined_names.add(DefinedName("reflective_textual_and_graphic", attr_text="'Schema Reference'!$B$4:$B$5"))
    wb.defined_names.add(DefinedName("reflective_photographic", attr_text="'Schema Reference'!$C$4:$C$4"))
    wb.defined_names.add(DefinedName("transmissive_photographic", attr_text="'Schema Reference'!$D$4:$D$7"))
    wb.defined_names.add(DefinedName("glass_substrate", attr_text="'Schema Reference'!$E$4:$E$5"))
    wb.defined_names.add(DefinedName("microform", attr_text="'Schema Reference'!$F$4:$F$7"))
    wb.defined_names.add(DefinedName("boolean_list", attr_text="'Schema Reference'!$G$4:$G$5"))
    wb.defined_names.add(DefinedName("division_code_list", attr_text=f"'Schema Reference'!$H$4:$H${3+len(division_codes)}"))

    # Auto-fit columns in Schema Reference
    for col in ws_ref.columns:
        max_len = max(len(str(cell.value or '')) for cell in col)
        col_letter = get_column_letter(col[0].column)
        ws_ref.column_dimensions[col_letter].width = max(max_len + 4, 15)

    # Hide reference sheet from standard users
    ws_ref.sheet_state = 'hidden'

    # ==============================================================================
    # --- 3. BUILD INVENTORY TEMPLATE SHEET ---
    # ==============================================================================
    # Define ordered columns, required/optional status, and field descriptions
    template_structure = [
        ("barcode", "REQUIRED", "14-digit code"),
        ("item_title", "OPTIONAL", "plain text, no formatting"),
        ("project_code", "REQUIRED", "assigned by VDS team"),
        ("collection_id", "REQUIRED", "3-7 digit code, not classmark"),
        ("division_code", "REQUIRED", "choose from dropdown"),
        ("shelf_locator", "OPTIONAL", "also known as classmark"),
        ("bnumber", "OPTIONAL", "from catalog"),
        ("object_type", "REQUIRED", "choose from dropdown"),
        ("object_format", "REQUIRED", "choose from dropdown"),
        ("aspace_component_id", "OPTIONAL", "from finding aid"),
        ("physical_condition_notes", "OPTIONAL", "condition observed at selection"),
        ("unit_index", "OPTIONAL", "for composite items like microfilm"),
        ("unit_title", "OPTIONAL", "for composite items like microfilm"),
        ("[INFO] estimated_page_count", "OPTIONAL", "logistics & estimates"),
        ("[INFO] is_oversized", "OPTIONAL", "choose from dropdown"),
        ("[INFO] needs_cataloging", "OPTIONAL", "choose from dropdown"),
    ]

    # Title Block
    ws_template.merge_cells("A1:P1")
    ws_template["A1"] = "NYPL DIGITAL IMAGING INVENTORY — SCHEMA 1.0"
    ws_template["A1"].font = Font(name="Calibri", size=16, bold=True, color="FFFFFF")
    ws_template["A1"].fill = PatternFill(start_color="1E293B", end_color="1E293B", fill_type="solid")
    ws_template["A1"].alignment = Alignment(horizontal="center", vertical="center")
    ws_template.row_dimensions[1].height = 40

    ws_template.merge_cells("A2:P2")
    ws_template["A2"] = "Standardized Sidecar Metadata Ingestion Sheet | Compliant with Digitized Image Schema v1.0"
    ws_template["A2"].font = Font(name="Calibri", size=11, italic=True, color="FFFFFF")
    ws_template["A2"].fill = PatternFill(start_color="334155", end_color="334155", fill_type="solid")
    ws_template["A2"].alignment = Alignment(horizontal="center", vertical="center")
    ws_template.row_dimensions[2].height = 24

    ws_template.row_dimensions[3].height = 10 # Spacer

    # Write 3-Row Header Block (Row 4: Name, Row 5: Required/Optional, Row 6: Description)
    ws_template.row_dimensions[4].height = 26
    ws_template.row_dimensions[5].height = 20
    ws_template.row_dimensions[6].height = 24

    for col_idx, (col_name, req_status, col_desc) in enumerate(template_structure, 1):
        c_head = ws_template.cell(row=4, column=col_idx, value=col_name)
        c_req  = ws_template.cell(row=5, column=col_idx, value=req_status)
        c_desc_cell = ws_template.cell(row=6, column=col_idx, value=col_desc)
        
        # Color coding for Header Names (Row 4)
        if col_idx in [14, 15, 16]: # [INFO] columns
            c_head.fill = PatternFill(start_color="D97706", end_color="D97706", fill_type="solid") # Warm Amber Gold
            c_head.font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
            c_req.fill = PatternFill(start_color="B45309", end_color="B45309", fill_type="solid")  # Lighter/dark amber
            c_req.font = Font(name="Calibri", size=9.5, bold=True, color="FFFFFF")
            c_desc_cell.fill = PatternFill(start_color="FEF3C7", end_color="FEF3C7", fill_type="solid") # Light amber tint
            c_desc_cell.font = Font(name="Calibri", size=9, italic=True, color="78350F")
        else:
            c_head.fill = PatternFill(start_color="0F766E", end_color="0F766E", fill_type="solid") # Deep Teal
            c_head.font = Font(name="Calibri", size=11, bold=True, color="FFFFFF")
            c_req.fill = PatternFill(start_color="0D9488", end_color="0D9488", fill_type="solid")  # Lighter Teal
            c_req.font = Font(name="Calibri", size=9.5, bold=True, color="FFFFFF")
            c_desc_cell.fill = PatternFill(start_color="CCFBF1", end_color="CCFBF1", fill_type="solid") # Light teal tint
            c_desc_cell.font = Font(name="Calibri", size=9, italic=True, color="134E4A")
            
        c_head.alignment = Alignment(horizontal="center" if col_idx not in [2, 11, 13] else "left", vertical="center", wrap_text=True)
        c_req.alignment = Alignment(horizontal="center", vertical="center")
        c_desc_cell.alignment = Alignment(horizontal="center", vertical="center", wrap_text=True)
        
        # Borders around the header block
        c_head.border = Border(left=Side(style='thin', color='CBD5E1'), right=Side(style='thin', color='CBD5E1'), top=Side(style='medium', color='1E293B'), bottom=Side(style='thin', color='E2E8F0'))
        c_req.border  = Border(left=Side(style='thin', color='CBD5E1'), right=Side(style='thin', color='CBD5E1'), top=Side(style='thin', color='E2E8F0'), bottom=Side(style='thin', color='E2E8F0'))
        c_desc_cell.border = Border(left=Side(style='thin', color='CBD5E1'), right=Side(style='thin', color='CBD5E1'), top=Side(style='thin', color='E2E8F0'), bottom=Side(style='medium', color='1E293B'))

    # Write 100 blank styled rows for data entry (Rows 7 to 106)
    for row_idx in range(7, 107):
        ws_template.row_dimensions[row_idx].height = 22
        fill_color = "FFFFFF" if row_idx % 2 != 0 else "F8FAFC"
        for col_idx in range(1, len(template_structure) + 1):
            c = ws_template.cell(row=row_idx, column=col_idx)
            c.font = Font(name="Calibri", size=10, color="1E293B")
            
            # Apply subtle warm tint to [INFO] data rows; neutral grey/white striping for standard columns
            if col_idx in [14, 15, 16]:
                c.fill = PatternFill(start_color="FFFBEB" if row_idx % 2 != 0 else "FEF3C7", end_color="FFFBEB" if row_idx % 2 != 0 else "FEF3C7", fill_type="solid")
            else:
                c.fill = PatternFill(start_color=fill_color, end_color=fill_color, fill_type="solid")
                
            c.border = Border(left=Side(style='thin', color='E2E8F0'), right=Side(style='thin', color='E2E8F0'), top=Side(style='thin', color='E2E8F0'), bottom=Side(style='thin', color='E2E8F0'))
            
            if col_idx in [1, 3, 4, 5, 6, 7, 8, 9, 12, 14, 15, 16]:
                c.alignment = Alignment(horizontal="center", vertical="center")
            else:
                c.alignment = Alignment(horizontal="left", vertical="center")

    # --- ADD DATA VALIDATION DROPDOWNS ---
    # 1. Division Code Dropdown (Col E)
    dv_div = DataValidation(type="list", formula1="division_code_list", allow_blank=True)
    dv_div.error = "Please select a valid division_code from the dropdown list."
    dv_div.errorTitle = "Invalid Division Code"
    dv_div.prompt = "Select a division code."
    dv_div.promptTitle = "Curatorial Division"

    # 2. Primary Dropdown: object_type (Col H)
    dv_type = DataValidation(type="list", formula1="object_type_list", allow_blank=True)
    dv_type.error = "Please select a valid object_type from the schema dropdown list."
    dv_type.errorTitle = "Invalid Object Type"
    dv_type.prompt = "Select an object_type from the list."
    dv_type.promptTitle = "Schema: object_type"

    # 3. Dependent Dropdown: object_format (Col I) -> Dynamically maps spaces/hyphens to underscores
    dv_format = DataValidation(type="list", formula1='INDIRECT(SUBSTITUTE(SUBSTITUTE($H7, " ", "_"), "-", "_"))', allow_blank=True)
    dv_format.error = "Please select a valid object_format matching the chosen object_type."
    dv_format.errorTitle = "Invalid Dependent Format"
    dv_format.prompt = "Select a format valid for the selected object_type."
    dv_format.promptTitle = "Dependent Schema Format"

    # 4. Boolean Flags for [INFO] columns (Col O: is_oversized, Col P: needs_cataloging)
    dv_bool = DataValidation(type="list", formula1="boolean_list", allow_blank=True)
    dv_bool.error = "Please select TRUE or FALSE."
    dv_bool.errorTitle = "Invalid Flag"

    ws_template.add_data_validation(dv_div)
    ws_template.add_data_validation(dv_type)
    ws_template.add_data_validation(dv_format)
    ws_template.add_data_validation(dv_bool)

    dv_div.add("E7:E106")
    dv_type.add("H7:H106")
    dv_format.add("I7:I106")
    dv_bool.add("O7:O106")
    dv_bool.add("P7:P106")

    # Freeze Panes below the 3-row header block (so headers, required status, and description stay visible)
    ws_template.freeze_panes = "A7"

    # Auto-fit columns
    for col_idx, (col_name, req_status, col_desc) in enumerate(template_structure, 1):
        col_letter = get_column_letter(col_idx)
        max_width = max(len(col_name), len(col_desc)) + 4
        ws_template.column_dimensions[col_letter].width = max(max_width, 16)

    wb.save(output_filename)
    print(f"Successfully generated: {output_filename}")

if __name__ == "__main__":
    generate_inventory_template()