#!/usr/bin/env python3
import argparse
import pandas as pd
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.platypus import SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle

def parse_inventory(excel_path: str) -> dict:
    """Parses the Excel inventory sheet, skipping row metadata and aggregating statistics."""
    
    # Read sheet 'Inventory Template'
    # Skip rows 0, 1, 2 (title info), and 4, 5 (REQUIRED/OPTIONAL and description rows)
    df = pd.read_excel(excel_path, sheet_name='Inventory Template', header=0, skiprows=[0, 1, 2, 4, 5])
    
    # Clean whitespace from column names
    df.columns = [str(col).strip() for col in df.columns]

    # Convert estimated_page_count to integer, replacing missing values with 0
    df['[INFO] estimated_page_count'] = (
        pd.to_numeric(df['[INFO] estimated_page_count'], errors='coerce')
        .fillna(0)
        .astype(int)
    )

    # Clean boolean / categorical flags
    df['[INFO] is_oversized'] = df['[INFO] is_oversized'].astype(str).str.strip().str.upper()
    df['[INFO] needs_cataloging'] = df['[INFO] needs_cataloging'].astype(str).str.strip().str.upper()

    # Aggregations
    total_items = len(df)
    total_pages = df['[INFO] estimated_page_count'].sum()

    # Project metadata summaries
    project_codes = ", ".join(df['project_code'].dropna().astype(str).unique())
    funding_sources = ", ".join(df['funding_source'].dropna().astype(str).unique())
    divisions = ", ".join(df['division_code'].dropna().astype(str).unique())

    # Summary table by Object Type & Format
    type_format_summary = (
        df.groupby(['object_type', 'object_format'])
        .agg(
            item_count=('barcode', 'count'),
            total_est_pages=('[INFO] estimated_page_count', 'sum')
        )
        .reset_index()
    )

    # Counts for special considerations
    oversized_count = df[df['[INFO] is_oversized'].isin(['YES', 'Y', 'TRUE'])].shape[0]
    needs_cat_count = df[df['[INFO] needs_cataloging'].isin(['YES', 'Y', 'TRUE'])].shape[0]
    
    # Count non-empty physical condition notes
    condition_notes_count = df[
        df['physical_condition_notes'].notna() & 
        (df['physical_condition_notes'].astype(str).str.strip() != '')
    ].shape[0]

    return {
        'project_codes': project_codes or 'N/A',
        'funding_sources': funding_sources or 'N/A',
        'divisions': divisions or 'N/A',
        'total_items': total_items,
        'total_pages': total_pages,
        'type_format_summary': type_format_summary,
        'oversized_count': oversized_count,
        'needs_cat_count': needs_cat_count,
        'condition_notes_count': condition_notes_count,
    }


def generate_sow_pdf(data: dict, output_filename: str):
    """Generates a PDF Statement of Work containing boilerplate language and data summaries."""
    
    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        rightMargin=40, leftMargin=40,
        topMargin=40, bottomMargin=40
    )

    styles = getSampleStyleSheet()

    # Custom styles
    title_style = ParagraphStyle(
        'DocTitle',
        parent=styles['Heading1'],
        fontSize=20,
        leading=24,
        textColor=colors.HexColor("#1A365D"),
        spaceAfter=12
    )
    heading_style = ParagraphStyle(
        'SectionHeader',
        parent=styles['Heading2'],
        fontSize=13,
        leading=16,
        textColor=colors.HexColor("#2B6CB0"),
        spaceBefore=14,
        spaceAfter=6
    )
    body_style = ParagraphStyle(
        'Body',
        parent=styles['Normal'],
        fontSize=10,
        leading=14,
        spaceAfter=8
    )

    story = []

    # Title
    story.append(Paragraph("Statement of Work: Digitization Services", title_style))
    story.append(Spacer(1, 8))

    # Section 1: Overview
    story.append(Paragraph("1. Project Overview & Scope", heading_style))
    overview_text = f"""
    This Statement of Work (SOW) defines the requirements and deliverables for vendor digitization services. 
    The vendor will pick up, handle, digitize, and return items according to the specifications outlined below.
    <br/><br/>
    • <b>Project Code(s):</b> {data['project_codes']}<br/>
    • <b>Division(s):</b> {data['divisions']}<br/>
    • <b>Funding Source(s):</b> {data['funding_sources']}<br/>
    • <b>Total Item Volume:</b> {data['total_items']:,} item(s)<br/>
    • <b>Estimated Total Image Volume:</b> {data['total_pages']:,} pages/images
    """
    story.append(Paragraph(overview_text, body_style))

    # Section 2: Format Breakdown Table
    story.append(Paragraph("2. Inventory Breakdown", heading_style))
    
    table_data = [["Object Type", "Object Format", "Items", "Est. Page Count"]]
    for _, row in data['type_format_summary'].iterrows():
        table_data.append([
            str(row['object_type']),
            str(row['object_format']),
            f"{row['item_count']:,}",
            f"{row['total_est_pages']:,}"
        ])

    table = Table(table_data, colWidths=[160, 160, 80, 100])
    table.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), colors.HexColor("#EDF2F7")),
        ('TEXTCOLOR', (0,0), (-1,0), colors.HexColor("#2D3748")),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 9),
        ('BOTTOMPADDING', (0,0), (-1,0), 6),
        ('ALIGN', (2,0), (-1,-1), 'RIGHT'),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#CBD5E0")),
    ]))
    story.append(table)
    story.append(Spacer(1, 10))

    # Section 3: Special Handling Summary
    story.append(Paragraph("3. Special Handling & Logistics Flags", heading_style))
    special_text = f"""
    • <b>Oversized Items:</b> {data['oversized_count']} item(s) are flagged as oversized and require large-format scanning equipment.<br/>
    • <b>Condition Notes:</b> {data['condition_notes_count']} item(s) have documented physical condition notes requiring custom handling.<br/>
    • <b>Cataloging Required:</b> {data['needs_cat_count']} item(s) require metadata capture/cataloging upon return.
    """
    story.append(Paragraph(special_text, body_style))

    # Section 4: Specifications & Deliverables (Boilerplate)
    story.append(Paragraph("4. Technical Specifications & Quality Assurance", heading_style))
    specs_text = """
    Vendor shall adhere strictly to FADGI 3-Star (or higher) digitizing guidelines:
    <br/><br/>
    1. <b>Master Image Files:</b> Uncompressed 400+ DPI, 24-bit color TIFF format.<br/>
    2. <b>Access Files:</b> Searchable PDFs with optical character recognition (OCR) applied.<br/>
    3. <b>File Naming Standard:</b> Digital files must be named using the 14-digit primary <code>barcode</code> supplied in the inventory list.<br/>
    4. <b>Quality Control:</b> 100% inspection for sharpness, correct orientation, complete margin framing, and exact sequence matching.
    """
    story.append(Paragraph(specs_text, body_style))

    # Build PDF Document
    doc.build(story)
    print(f"SOW PDF generated successfully: {output_filename}")


def main():
    parser = argparse.ArgumentParser(
        description="Parse an inventory Excel file and generate a vendor Statement of Work (SOW) PDF."
    )
    parser.add_argument(
        "-i", "--input",
        required=True,
        metavar="INPUT_XLSX",
        help="Path to the input Excel (.xlsx) file containing the 'Inventory Template' sheet."
    )
    parser.add_argument(
        "-o", "--output",
        default="Digitization_Vendor_SOW.pdf",
        metavar="OUTPUT_PDF",
        help="Path for the generated output PDF file (default: Digitization_Vendor_SOW.pdf)."
    )

    args = parser.parse_args()

    sow_data = parse_inventory(args.input)
    generate_sow_pdf(sow_data, args.output)


if __name__ == "__main__":
    main()