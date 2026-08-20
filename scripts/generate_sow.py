#!/usr/bin/env python3
"""
nypl_sow_generator.py — NYPL Vendor Digitization Statement of Work Generator

Reads an NYPL inventory Excel template and produces a formatted PDF Statement
of Work (SOW) for submission to a digitization vendor.

Usage:
    python nypl_sow_generator.py -i inventory.xlsx --vendor BLW --ocr

Dependencies:
    pip install pandas openpyxl reportlab
"""

import argparse
import datetime
import logging
import sys
from typing import Any

import pandas as pd
from reportlab.lib import colors
from reportlab.lib.pagesizes import letter
from reportlab.lib.styles import ParagraphStyle, getSampleStyleSheet
from reportlab.platypus import (
    HRFlowable,
    Paragraph,
    SimpleDocTemplate,
    Spacer,
    Table,
    TableStyle,
)

# ---------------------------------------------------------------------------
# Configuration
# ---------------------------------------------------------------------------

logging.basicConfig(level=logging.INFO, format="%(levelname)s: %(message)s")

# Vendor display-name registry
VENDORS: dict[str, str] = {
    "BLW": "Backstage Library Works",
    "CAW": "Chicago Albumen Works",
}

# Vendor address registry
VENDOR_ADDRESSES: dict[str, str] = {
    "BLW": "Backstage Library Works<br/>Nine S. Commerce Way<br/>Bethlehem, PA, US<br/>18017",
    "CAW": "Chicago Albumen Works<br/>174 Front Street<br/>Housatonic, MA 01236",
}

# Physical shipping destination for digital deliverables
DELIVERY_ADDRESS = """\
New York Public Library<br/>
31-11 Thomson Ave., Room 305<br/>
Long Island City, NY 11101"""

# ---------------------------------------------------------------------------
# Excel template constants
# ---------------------------------------------------------------------------

# The NYPL inventory template has 3 rows of institutional header (rows 0-2),
# row 3 is the true column header, and rows 4-5 are instruction / example
# rows that must be discarded before processing.
TEMPLATE_SKIP_ROWS: list[int] = [0, 1, 2, 4, 5]

REQUIRED_COLUMNS: list[str] = [
    "barcode",
    "object_type",
    "object_format",
    "[INFO] estimated_page_count",
]

# Column names with the [INFO] prefix used throughout the template
COL_PAGE_COUNT = "[INFO] estimated_page_count"
COL_IS_OVERSIZED = "[INFO] is_oversized"
COL_NEEDS_CATALOGING = "[INFO] needs_cataloging"

# Standard-industry microfilm frame estimates for 100-foot reels
MICROFILM_ESTIMATES: dict[str, int] = {
    "35mm": 800,
    "16mm": 2500,
}

# String values that map to boolean True for flag columns
TRUTHY_VALUES: frozenset[str] = frozenset({"YES", "Y", "TRUE", "1", "T"})

# ---------------------------------------------------------------------------
# PDF colour palette
# ---------------------------------------------------------------------------

CLR_NAVY        = colors.HexColor("#1A365D")   # Document title
CLR_BLUE        = colors.HexColor("#2B6CB0")   # Section headings / links
CLR_BLUE_LIGHT  = colors.HexColor("#EBF4FF")   # Table header background
CLR_STRIPE      = colors.HexColor("#F7FAFC")   # Alternating table row
CLR_RULE        = colors.HexColor("#BEE3F8")   # Horizontal divider
CLR_BORDER      = colors.HexColor("#CBD5E0")   # Table grid
CLR_HEADER_TXT  = colors.HexColor("#2D3748")   # Table header text
CLR_META        = colors.HexColor("#718096")   # Page header / footer text
CLR_ITALIC      = colors.HexColor("#4A5568")   # Disclaimer / fine print
CLR_TOTAL_BG    = colors.HexColor("#EBF8FF")   # Totals row background

# ---------------------------------------------------------------------------
# Helpers
# ---------------------------------------------------------------------------


def get_clean_unique(series: pd.Series) -> list[str]:
    """Return unique, non-empty, non-NaN string values from a pandas Series."""
    return [
        str(v).strip()
        for v in series.dropna().unique()
        if str(v).strip() and str(v).lower() != "nan"
    ]


def get_column_or_empty(df: pd.DataFrame, col: str) -> pd.Series:
    """Return the named column, or an empty Series if the column is absent."""
    return df[col] if col in df.columns else pd.Series(dtype=str)


# ---------------------------------------------------------------------------
# Inventory parsing
# ---------------------------------------------------------------------------


def parse_inventory(excel_path: str) -> dict[str, Any]:
    """
    Parse the NYPL inventory Excel template and return aggregated statistics.

    Raises:
        FileNotFoundError: If the file path does not exist.
        ValueError: If the expected sheet or required columns are missing.
        RuntimeError: For all other read errors.
    """
    try:
        df = pd.read_excel(
            excel_path,
            sheet_name="Inventory Template",
            header=0,
            skiprows=TEMPLATE_SKIP_ROWS,
        )
    except FileNotFoundError:
        raise FileNotFoundError(f"File not found: {excel_path}")
    except ValueError as e:
        raise ValueError(
            "Could not find the sheet 'Inventory Template' in the Excel file."
        ) from e
    except Exception as e:
        raise RuntimeError(f"Unexpected error reading the Excel file: {e}") from e

    # Normalise column names
    df.columns = [str(col).strip() for col in df.columns]

    # Validate required columns
    missing = [c for c in REQUIRED_COLUMNS if c not in df.columns]
    if missing:
        raise ValueError(f"Missing required column(s): {', '.join(missing)}")

    # ---- Numeric coercion for page/frame counts ----------------------------
    df[COL_PAGE_COUNT] = (
        pd.to_numeric(df[COL_PAGE_COUNT], errors="coerce").fillna(0).astype(int)
    )

    # ---- Microfilm estimation logic ----------------------------------------
    # Apply standard industry frame estimates when the count is absent (0).
    for gauge, estimate in MICROFILM_ESTIMATES.items():
        is_gauge = df["object_format"].astype(str).str.contains(
            gauge, case=False, na=False
        )
        missing_count = df[COL_PAGE_COUNT] == 0
        df.loc[is_gauge & missing_count, COL_PAGE_COUNT] = estimate

    # ---- Boolean / categorical flag columns --------------------------------
    for col, default in [(COL_IS_OVERSIZED, "NO"), (COL_NEEDS_CATALOGING, "NO")]:
        if col in df.columns:
            df[col] = df[col].astype(str).str.strip().str.upper()
        else:
            df[col] = default

    if "physical_condition_notes" not in df.columns:
        df["physical_condition_notes"] = ""

    # ---- Aggregations ------------------------------------------------------
    total_items = len(df)
    total_est_images = int(df[COL_PAGE_COUNT].sum())

    project_codes = ", ".join(get_clean_unique(get_column_or_empty(df, "project_code")))
    funding_sources = ", ".join(
        get_clean_unique(get_column_or_empty(df, "funding_source"))
    )
    divisions = ", ".join(get_clean_unique(get_column_or_empty(df, "division_code")))

    type_format_summary = (
        df.groupby(["object_type", "object_format"])
        .agg(
            item_count=("barcode", "count"),
            total_est_pages=(COL_PAGE_COUNT, "sum"),
        )
        .reset_index()
    )

    oversized_count = df[df[COL_IS_OVERSIZED].isin(TRUTHY_VALUES)].shape[0]
    needs_cat_count = df[df[COL_NEEDS_CATALOGING].isin(TRUTHY_VALUES)].shape[0]
    condition_notes_count = df[
        df["physical_condition_notes"].notna()
        & (df["physical_condition_notes"].astype(str).str.strip() != "")
        & (df["physical_condition_notes"].astype(str).str.lower() != "nan")
    ].shape[0]

    return {
        "project_codes": project_codes or "N/A",
        "funding_sources": funding_sources or "N/A",
        "divisions": divisions or "N/A",
        "total_items": total_items,
        "total_est_images": total_est_images,
        "type_format_summary": type_format_summary,
        "oversized_count": oversized_count,
        "needs_cat_count": needs_cat_count,
        "needs_cataloging": needs_cat_count > 0,   # pre-computed flag
        "condition_notes_count": condition_notes_count,
    }


# ---------------------------------------------------------------------------
# PDF page callback
# ---------------------------------------------------------------------------


def add_header_footer(canvas, doc) -> None:  # noqa: ANN001 — ReportLab callback sig
    """Draw the NYPL page header and page-number footer on every page."""
    _ = doc  # Required by ReportLab's onPage callback signature; unused here.
    canvas.saveState()

    # ---- Footer: page number (bottom-right) --------------------------------
    canvas.setFont("Helvetica", 9)
    canvas.setFillColor(CLR_META)
    canvas.drawRightString(
        letter[0] - 50, 22, f"Page {canvas.getPageNumber()}"
    )

    # ---- Header: NYPL tag (top-left) with thin rule beneath ----------------
    canvas.setFont("Helvetica-Bold", 9)
    canvas.setFillColor(CLR_META)
    canvas.drawString(50, letter[1] - 26, "New York Public Library | Vendor Digitization Services")

    canvas.setStrokeColor(CLR_RULE)
    canvas.setLineWidth(0.75)
    canvas.line(50, letter[1] - 32, letter[0] - 50, letter[1] - 32)

    canvas.restoreState()


# ---------------------------------------------------------------------------
# PDF generation
# ---------------------------------------------------------------------------


def _build_styles() -> dict[str, ParagraphStyle]:
    """Return a dict of named ParagraphStyles for the SOW document."""
    base = getSampleStyleSheet()
    return {
        "title": ParagraphStyle(
            "DocTitle", parent=base["Heading1"],
            fontSize=20, leading=26,
            textColor=CLR_NAVY,
            spaceBefore=0, spaceAfter=10,
        ),
        "meta": ParagraphStyle(
            "DocMeta", parent=base["Normal"],
            fontSize=10, leading=14,
            textColor=CLR_META,
            spaceAfter=6,
        ),
        "heading": ParagraphStyle(
            "SectionHeader", parent=base["Heading2"],
            fontSize=12, leading=15,
            textColor=CLR_BLUE,
            spaceBefore=12, spaceAfter=6,
        ),
        "body": ParagraphStyle(
            "Body", parent=base["Normal"],
            fontSize=10, leading=14,
            spaceAfter=8,
        ),
        "list": ParagraphStyle(
            "List", parent=base["Normal"],
            fontSize=10, leading=14,
            spaceAfter=4, leftIndent=15,
        ),
        "table_body": ParagraphStyle(
            "TableBody", parent=base["Normal"],
            fontSize=9, leading=11,
            spaceAfter=0,
        ),
        "table_bold": ParagraphStyle(
            "TableBold", parent=base["Normal"],
            fontSize=9, leading=11,
            fontName="Helvetica-Bold",
            spaceAfter=0,
        ),
        "disclaimer": ParagraphStyle(
            "Disclaimer", parent=base["Normal"],
            fontSize=8.5, leading=12,
            textColor=CLR_ITALIC,
            spaceBefore=4, spaceAfter=4,
            fontName="Helvetica-Oblique",
        ),
    }


def _build_inventory_table(
    summary: pd.DataFrame, styles: dict[str, ParagraphStyle]
) -> Table:
    """Build the inventory breakdown table with alternating rows and a totals row."""
    tb = styles["table_body"]
    tbo = styles["table_bold"]

    header = [
        Paragraph("<b>Object Type</b>", tbo),
        Paragraph("<b>Object Format</b>", tbo),
        Paragraph("<b>Items</b>", tbo),
        Paragraph("<b>Est. Images</b>", tbo),
    ]
    rows = [header]

    for _, row in summary.iterrows():
        rows.append([
            Paragraph(str(row["object_type"]), tb),
            Paragraph(str(row["object_format"]), tb),
            Paragraph(f"{row['item_count']:,}", tb),
            Paragraph(f"{row['total_est_pages']:,}", tb),
        ])

    # Totals row
    rows.append([
        Paragraph("<b>TOTAL</b>", tbo),
        Paragraph("", tb),
        Paragraph(f"<b>{summary['item_count'].sum():,}</b>", tbo),
        Paragraph(f"<b>{summary['total_est_pages'].sum():,}</b>", tbo),
    ])

    table = Table(rows, colWidths=[160, 160, 80, 100])

    # Alternating stripe commands (skip header row 0 and totals row -1)
    stripe_cmds = [
        ("BACKGROUND", (0, i), (-1, i), CLR_STRIPE)
        for i in range(2, len(rows) - 1, 2)
    ]

    table.setStyle(TableStyle([
        # Header row
        ("BACKGROUND",    (0, 0),  (-1, 0),  CLR_BLUE_LIGHT),
        ("TEXTCOLOR",     (0, 0),  (-1, 0),  CLR_HEADER_TXT),
        ("BOTTOMPADDING", (0, 0),  (-1, 0),  8),
        ("TOPPADDING",    (0, 0),  (-1, 0),  8),
        # Totals row
        ("BACKGROUND",    (0, -1), (-1, -1), CLR_TOTAL_BG),
        ("TOPPADDING",    (0, -1), (-1, -1), 6),
        ("BOTTOMPADDING", (0, -1), (-1, -1), 6),
        ("LINEABOVE",     (0, -1), (-1, -1), 1.0, CLR_BLUE),
        # Global
        ("FONTSIZE",      (0, 0),  (-1, -1), 9),
        ("VALIGN",        (0, 0),  (-1, -1), "MIDDLE"),
        ("TOPPADDING",    (0, 1),  (-1, -2), 5),
        ("BOTTOMPADDING", (0, 1),  (-1, -2), 5),
        ("GRID",          (0, 0),  (-1, -1), 0.4, CLR_BORDER),
        *stripe_cmds,
    ]))

    return table


def generate_sow_pdf(
    data: dict[str, Any], args: argparse.Namespace, output_filename: str
) -> None:
    """Generate a PDF Statement of Work from parsed inventory data."""

    doc = SimpleDocTemplate(
        output_filename,
        pagesize=letter,
        rightMargin=50, leftMargin=50,
        topMargin=55, bottomMargin=50,
    )

    styles = _build_styles()
    story: list = []

    today_str = datetime.date.today().strftime("%B %-d, %Y")
    vendor_full_name = VENDORS.get(args.vendor, args.vendor)
    vendor_full_address = VENDOR_ADDRESSES.get(args.vendor, vendor_full_name)
    needs_cataloging: bool = data["needs_cataloging"]

    # ---- Title block -------------------------------------------------------
    story.append(Paragraph("Statement of Work: Image-Based Digitization", styles["title"]))
    story.append(Paragraph(
        f"<b>Project:</b> {data['project_codes']} &nbsp;&nbsp;|&nbsp;&nbsp; <b>Date:</b> {today_str}",
        styles["meta"],
    ))
    story.append(HRFlowable(width="100%", thickness=1.5, color=CLR_NAVY, spaceAfter=10))

    # ---- Contact block -----------------------------------------------------
    link_color = CLR_BLUE.hexval()
    story.append(Paragraph(
        f"<b>Statement of Work prepared by:</b><br/>"
        f"New York Public Library, Vendor Digitization Services<br/>"
        f"{args.contact_name} — "
        f'<a href="mailto:{args.contact_email}" color="{link_color}">'
        f"{args.contact_email}</a>"
        f"<br/><br/>"
        f"<b>Estimate Requested From:</b><br/>"
        f"{vendor_full_address}",
        styles["body"],
    ))
    story.append(Spacer(1, 4))

    # ---- Introduction ------------------------------------------------------
    story.append(Paragraph("Introduction", styles["heading"]))
    story.append(Paragraph(
        f"The New York Public Library (NYPL) invites {vendor_full_name} to submit a "
        "formal cost estimate for image-based digitization services in support of an archival "
        "preservation initiative. This Statement of Work (SOW) defines the project scope, "
        "technical specifications, and deliverable requirements to serve as the basis for "
        "that estimate.<br/><br/>"
        "All work is contingent upon issuance of an NYPL Purchase Order (PO). No work may "
        "commence prior to receipt of an authorized PO. Please submit your estimate by email "
        "to the NYPL contacts listed above. Where a Master Service Agreement (MSA) is in "
        "effect, all pricing must conform to its established terms; any materials, formats, "
        "or services that fall outside existing MSA scope must be identified and quoted "
        "separately.<br/><br/>"
        "<b>Please structure your estimate with a separate subtotal for each of the "
        "following cost categories:</b>",
        styles["body"],
    ))

    # Build ordered list of estimate subtotals dynamically
    subtotals = [
        "(a) Image capture and digitization services — itemized by object type and format, "
        "with separate line items for any applicable special handling surcharges",
        "(b) Return shipping costs for digital storage media",
    ]
    optional_items: list[str] = []
    if args.vendor_shipping:
        optional_items.append("Secure transit / shipping of physical materials")
    if args.vendor_packing:
        optional_items.append("On-site collection packing and preparation services")
    if args.ocr:
        optional_items.append("OCR / Text extraction services")
    if needs_cataloging:
        optional_items.append(
            "Cataloging and bibliographic services "
            "(original cataloging and bibliographic record creation)"
        )

    for i, label in enumerate(optional_items, start=ord("d")):
        subtotals.append(f"({chr(i)}) {label}")

    for item in subtotals:
        story.append(Paragraph(item, styles["list"]))
    story.append(Spacer(1, 8))

    # ---- Section 1: Project Overview ---------------------------------------
    story.append(HRFlowable(width="100%", thickness=0.5, color=CLR_RULE, spaceAfter=2))
    story.append(Paragraph("1. Project Overview &amp; Scope", styles["heading"]))
    story.append(Paragraph(
        f"• <b>Project Code(s):</b> {data['project_codes']}<br/>"
        f"• <b>Division(s):</b> {data['divisions']}<br/>"
        f"• <b>Funding Source(s):</b> {data['funding_sources']}<br/>"
        f"• <b>Total Item Volume:</b> {data['total_items']:,} item(s)<br/>"
        f"• <b>Estimated Total Image Volume:</b> {data['total_est_images']:,} pages / images",
        styles["body"],
    ))

    # ---- Section 2: Inventory Breakdown ------------------------------------
    story.append(HRFlowable(width="100%", thickness=0.5, color=CLR_RULE, spaceAfter=2))
    story.append(Paragraph("2. Inventory Breakdown", styles["heading"]))
    story.append(_build_inventory_table(data["type_format_summary"], styles))
    story.append(Paragraph(
        "Note: Where exact frame counts for microforms are unavailable, estimates are "
        "calculated using standard 100-foot reel averages — typically 800 frames for 35mm "
        "and 2,500 frames for 16mm — based on common library digitization benchmarks. "
        "Actual counts will vary by reduction ratio, document size, and filming standard.",
        styles["disclaimer"],
    ))
    story.append(Spacer(1, 6))

    # ---- Section 3: Special Handling ---------------------------------------
    story.append(HRFlowable(width="100%", thickness=0.5, color=CLR_RULE, spaceAfter=2))
    story.append(Paragraph("3. Special Handling &amp; Logistics Flags", styles["heading"]))
    story.append(Paragraph(
        f"• <b>Oversized Items:</b> {data['oversized_count']} item(s) flagged as oversized.<br/>"
        f"• <b>Condition Notes:</b> {data['condition_notes_count']} item(s) have documented "
        f"physical condition notes.<br/>"
        f"• <b>Cataloging Required:</b> {data['needs_cat_count']} item(s) require cataloging "
        f"and bibliographic services from the vendor.",
        styles["body"],
    ))

    # ---- Section 4: Technical Specifications -------------------------------
    story.append(HRFlowable(width="100%", thickness=0.5, color=CLR_RULE, spaceAfter=2))
    story.append(Paragraph("4. Technical Specifications", styles["heading"]))
    story.append(Paragraph(
        "Vendor shall adhere strictly to NYPL's image-based digitization standards. "
        "Please review the following required documentation:<br/><br/>"
        f"<b>1. Digital Asset Specifications:</b><br/>"
        f'<a href="https://nypl-research.github.io/digital-imaging-resources/docs/vendor_digitization/digital_asset_specifications/" color="{link_color}">digital_asset_specifications</a>'
        f"<br/><br/>"
        f"<b>2. JSON Sidecar Schema and Validation:</b><br/>"
        f'<a href="https://nypl-research.github.io/digital-imaging-resources/docs/vendor_digitization/json_schema_sidecar/" color="{link_color}">json_schema_sidecar</a>'
        f"<br/><br/>"
        f"<b>3. Inventory Spreadsheet Instructions:</b><br/>"
        f'<a href="https://nypl-research.github.io/digital-imaging-resources/docs/vendor_digitization/inventory_spreadsheet_spec/" color="{link_color}">inventory_spreadsheet_spec</a>',
        styles["body"],
    ))

    # ---- Section 4 key requirements callout --------------------------------
    story.append(Paragraph(
        "<b>Key Requirements (see full specification for detail):</b>",
        styles["body"],
    ))
    key_reqs = [
        "<b>No silent substitution.</b> The vendor shall not substitute file formats, "
        "compression methods, color profiles, bit depths, resolutions, OCR formats, "
        "naming conventions, metadata fields, or delivery structures without prior "
        "written approval from the Library.",

        "<b>File counts per physical item.</b> Transmissive film and glass negatives "
        "require six (6) files per physical item (two preservation masters, two service "
        "files, and two access JPEGs — one negative-polarity and one positive-polarity "
        "each). Natively positive slides and transparencies require three (3) files. "
        "Reflective materials follow the standard three-file structure unless otherwise "
        "specified. Vendors must confirm their pricing reflects the correct file count "
        "for each format in this project.",

        "<b>JSON sidecar 1:1 pairing and co-location.</b> Every delivered asset — "
        "including all preservation masters, service files, access derivatives, and OCR "
        "files — must be accompanied by exactly one matching JSON sidecar file. Bulk or "
        "combined JSON manifests do not satisfy this requirement. The sidecar filename "
        "must match its paired asset character-for-character, changing only the "
        "extension to .json, and must reside in the same directory as its paired asset.",

        "<b>Continuous absolute sequence numbering.</b> For multi-unit items (e.g., "
        "microfilm reels containing multiple distinct intellectual works), the physical "
        "frame sequence must be continuous across the complete barcode-level object. "
        "Sequence numbering must not reset at intellectual unit boundaries. "
        "All files derived from the same physical frame must share the same "
        "absolute sequence number.",

        "<b>Pilot batch required before mass production.</b> The vendor must deliver "
        "a representative pilot batch consisting of at least one complete bag per format type "
        "for Library review and approval before full production begins. Mass production shall "
        "not commence until the Library provides written approval of the pilot, unless this "
        "requirement is explicitly waived in writing.",
    ]
    for req in key_reqs:
        story.append(Paragraph(f"• {req}", styles["list"]))
    story.append(Spacer(1, 6))

    # ---- Section 5: Expanded Services (conditional) -----------------------
    has_expanded = any([args.vendor_shipping, args.vendor_packing, args.ocr, needs_cataloging])
    if has_expanded:
        story.append(HRFlowable(width="100%", thickness=0.5, color=CLR_RULE, spaceAfter=2))
        story.append(Paragraph("5. Expanded Services Requirements", styles["heading"]))

        expanded: list[tuple[str, str]] = []
        if args.vendor_packing:
            expanded.append((
                "On-Site Packing and Collection Preparation",
                "The Contractor shall provide professional, on-site packing services at NYPL "
                "facilities prior to transport using archival-grade, acid-free, or "
                "high-density packing materials. Pre-transport inventory verification against "
                "the NYPL manifest is required.",
            ))
        if args.vendor_shipping:
            expanded.append((
                "Secure Transportation",
                "The Contractor shall provide secure, climate-controlled logistics with "
                "shock/vibration mitigation. Cargo areas must remain locked at all times, "
                "and transit must be dedicated exclusively to NYPL materials unless "
                "otherwise authorized.",
            ))
        if args.ocr:
            expanded.append((
                "OCR and Text Extraction",
                "The Contractor shall provide OCR / text extraction services for suitable "
                "materials. Deliverables may include Searchable PDF, plain text, ALTO XML, "
                "or METS/ALTO packages as defined in final project specs. Searchable PDF "
                "shall not be the exclusive deliverable without explicit NYPL approval.",
            ))
        if needs_cataloging:
            expanded.append((
                "Cataloging and Bibliographic Services",
                "The Contractor shall provide cataloging, bibliographic record creation, or "
                "metadata remediation services conforming to NYPL-specified standards "
                "(e.g., RDA, MARC21). The Contractor shall not make direct changes in NYPL "
                "systems unless expressly authorized.",
            ))


        for title, body in expanded:
            story.append(Paragraph(f"<b>{title}:</b>", styles["body"]))
            story.append(Paragraph(body, styles["list"]))

    # ---- Section 6 (or 5): Deliverables & Shipping -------------------------
    delivery_section = 6 if has_expanded else 5
    story.append(HRFlowable(width="100%", thickness=0.5, color=CLR_RULE, spaceAfter=2))
    story.append(Paragraph(f"{delivery_section}. Deliverables &amp; Shipping Addresses", styles["heading"]))
    story.append(Paragraph(
        f"Please ship the first hard drive immediately for review, and the remainder in "
        f"batches of 3–5 hard drives.<br/><br/>"
        f"<b>Ship Digital Assets (Hard Drives) To:</b><br/>"
        f"{args.contact_name}<br/>"
        f"{DELIVERY_ADDRESS}",
        styles["body"],
    ))

    # ---- Build PDF ---------------------------------------------------------
    doc.build(story, onFirstPage=add_header_footer, onLaterPages=add_header_footer)
    logging.info("SOW PDF generated: %s", output_filename)


# ---------------------------------------------------------------------------
# CLI Entry Point
# ---------------------------------------------------------------------------


def main() -> None:
    parser = argparse.ArgumentParser(
        description=(
            "Parse an NYPL inventory Excel file and generate a vendor "
            "Statement of Work (SOW) PDF."
        )
    )
    parser.add_argument(
        "-i", "--input", required=True, metavar="INPUT_XLSX",
        help="Path to the input Excel (.xlsx) file containing the 'Inventory Template' sheet.",
    )
    parser.add_argument(
        "-o", "--output", default="Digitization_Vendor_SOW.pdf", metavar="OUTPUT_PDF",
        help="Path for the generated output PDF (default: Digitization_Vendor_SOW.pdf).",
    )

    # Vendor & scope flags
    parser.add_argument(
        "--vendor", choices=list(VENDORS.keys()), default="BLW",
        help="Target vendor for the SOW.",
    )
    parser.add_argument("--ocr", action="store_true", help="Include OCR/text extraction services.")
    parser.add_argument("--vendor-shipping", action="store_true", help="Include secure vendor transit.")
    parser.add_argument("--vendor-packing", action="store_true", help="Include on-site vendor packing.")

    # Contact info — no hardcoded personal defaults
    parser.add_argument(
        "--contact-name", required=True, metavar="NAME",
        help="Full name of the NYPL contact authoring the SOW.",
    )
    parser.add_argument(
        "--contact-email", required=True, metavar="EMAIL",
        help="Email address of the NYPL contact authoring the SOW.",
    )

    args = parser.parse_args()

    logging.info("Processing inventory: %s", args.input)
    try:
        sow_data = parse_inventory(args.input)
    except (FileNotFoundError, ValueError, RuntimeError) as exc:
        logging.error(str(exc))
        sys.exit(1)

    generate_sow_pdf(sow_data, args, args.output)


if __name__ == "__main__":
    main()
