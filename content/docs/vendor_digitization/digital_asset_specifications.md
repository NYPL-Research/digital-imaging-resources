---
title: "Digital Asset Specifications"
linkTitle: "Digital Asset Specifications"
weight: 30
toc_hide: false
description: "Digital Asset Specifications for outsourced digitization of image-based collection materials."
---

## 1. Purpose

This appendix defines baseline digital asset specifications for outsourced digitization of image-based collection materials. It is intended to support project-specific scopes of work (SOWs) and may be incorporated into any applicable vendor digitization agreements or contracts.

These specifications establish expected deliverables for several broad material categories:

- Reflective textual and graphic materials
- Reflective photographic materials
- Transmissive photographic materials, including film negatives, transparencies, slides, and glass plates
- Microform materials, including 16mm and 35mm roll microfilm, microfiche, and aperture cards
- Associated metadata, OCR, manifests, checksums, and quality control documentation.

Project-specific scopes may supplement or modify these requirements, but deviations must be approved in writing by the Library before production begins.

## 2. General Principles

### 2.1 Preservation and Access Deliverables

The Library may request multiple deliverable types for each project. These should be clearly distinguished by role.

| Role | Working Name | Purpose |
|---|---|---|
| Preservation | U-File | Highest-quality preservation-oriented file; minimal processing; intended to retain the full informational content of the source object. |
| Production / Service | S-File | Cropped, oriented, and otherwise normalized file for internal use, derivative creation, access workflows, or ingest into discovery systems. |
| Access Derivative | JPEG | Lightweight access derivative for online display or review. |
| OCR / Text Derivative | OCR package | Searchable text, ALTO, hOCR, PDF, or other text deliverables, when applicable. |
| Metadata / Documentation | Manifest package | Metadata, checksums, QC reports, exception reports, and other project documentation. |

Not every project will require every role. Each project-specific scope should identify required deliverables.

### 2.2 No Silent Substitution

The vendor shall not substitute file formats, compression methods, color profiles, bit depths, resolutions, OCR formats, naming conventions, metadata fields, or delivery structures without prior written approval from the Library.

### 2.3 Accurate Source-Sized Resolution

When resolution is specified in pixels per inch, the PPI shall be measured relative to the physical dimensions of the original source object, not the dimensions of a derivative file or resized output. Image files must include accurate resolution metadata in the appropriate TIFF or image header fields.

### 2.4 FADGI Conformance

Where applicable, digitization should be performed according to the FADGI Technical Guidelines for Digitizing Cultural Heritage Materials, using the appropriate object category, star level, targets, and conformance evaluation tools for the source material.

Unless otherwise specified:

- General textual and manuscript materials should meet FADGI 3-Star requirements at minimum.
- Rare, special, photographic, fine-detail, and high-value materials should meet FADGI 4-Star requirements where feasible.
- Transmissive materials should use appropriate transmissive targets and evaluation methods.
- Vendor documentation should identify the FADGI category and star level targeted for each project.

### 2.5 Targets and Calibration

The vendor shall utilize appropriate technical targets, calibration procedures, and process-control documentation for each material type to ensure FADGI compliance.

#### 2.5.1 Reflective Materials (Object-Level Targets)

For reflective textual, graphic, and photographic print materials (Sections 3 and 4), the vendor shall utilize appropriate Image Science Associates (ISA) GoldenThread targets (such as the ISA Object Target or Device Target, as appropriate for the material size).

**Preservation (U-Files):** Targets must be captured inline with the source material as object-level target-bearing images. The target must be positioned within the frame so that it is fully visible, un-obscured, and flat, without overlapping any portion of the source collection item.

**Production / Service (S-Files):** The target must be digitally cropped out of the final delivered image. The crop must completely exclude the target while retaining a slight, uniform, and visible border of the capture background around the physical edges of the collection object. Overly tight cropping, flush cropping, or any crop that cuts into the physical boundary of the object is strictly prohibited.

#### 2.5.2 Transmissive Materials (Batch/Session Calibration)

For transmissive materials (Section 5), technical calibration targets must be captured at the start of each production session or batch to establish, verify, and document equipment profiles.

Transmissive targets shall be included in the final delivery as separate, uncropped target images.

Targets must not be embedded within or captured inline with the source collection object images, unless an exception is explicitly requested and authorized in the project-specific SOW

## 3. Reflective Textual, Manuscript, Bound Volume, and Graphic Materials

### 3.1 Included Materials

This category includes:

- Bound volumes
- Rare books
- Manuscripts
- Loose paper
- Archival folders
- Correspondence
- Ledgers
- Scrapbooks
- Maps, posters, broadsides, and other graphic works, unless treated as oversized special projects
- Mixed paper-based collections.

Photographic prints may be handled under this category for routine access projects, but preservation-quality photographic print digitization should follow the photographic reflective specifications in Section 4.

### 3.2 Recommended Baseline Specifications

| Feature | Preservation / U-File | Service / S-File | Access Derivative |
|---|---|---|---|
| File format | TIFF | TIFF or other approved format | JPEG |
| Compression | Lossless ZIP (Deflate) | Lossless ZIP (Deflate) | Lossy JPEG |
| Bit depth | 16-bit | 8-bit | 8-bit |
| Color mode | RGB | RGB | RGB |
| Color profile | Adobe RGB (1998) | sRGB | sRGB |
| Resolution | Minimum 400 PPI for fine-detail material; minimum 300 PPI may be acceptable for modern textual records if approved | Match U-File unless resized by project specification | Typically 3500 px long side; do not upscale smaller originals |
| Cropping | Full object visible; no cropping into object; border/background retained as specified | Cropped with slim border; no loss of content | Match S-File crop |
| Orientation | As captured or normalized, project-specific | Correct reading orientation | Correct reading orientation |
| FADGI Aim | 3-Star minimum; 4-Star for rare/special/fine-detail materials where feasible | Not applicable unless specified | Not applicable |
| Processing | Minimal; no undocumented enhancement | Approved crop, orientation, deskew, and tonal normalization | Derived from S-File |

### 3.3 Handling of Bound Volumes

Unless explicitly authorized by the Library, bound volumes must be digitized non-destructively. The vendor shall use appropriate cradles, supports, lighting, and capture methods to avoid damage to bindings, pages, covers, inserts, and foldouts.

Project-specific instructions should define capture requirements for:

- Front cover
- Back cover
- Spine
- Endpapers
- Blank pages
- Foldouts
- Inserts
- Tipped-in items
- Page edges
- Bookplates
- Ownership marks
- Barcodes or labels.

## 4. Reflective Photographic Prints

### 4.1 Included Materials

This category includes:

- Black-and-white photographic prints
- Color photographic prints
- Mounted photographs
- Cabinet cards
- Cartes de visite
- Annotated prints
- Photographs with significant versos, mounts, stamps, captions, or enclosures.

### 4.2 Recommended Baseline Specifications

| Feature | Preservation / U-File | Service / S-File | Access Derivative |
|---|---|---|---|
| File format | TIFF | TIFF or other approved format | JPEG |
| Compression | Lossless ZIP (Deflate) | Lossless ZIP (Deflate) | Lossy JPEG |
| Bit depth | 16-bit | 8-bit or 16-bit, project-specific | 8-bit |
| Color mode | RGB | RGB | RGB |
| Color profile | Adobe RGB (1998) | sRGB | sRGB |
| Resolution | Minimum 600 PPI at original size, or higher for small/fine-detail photographs | Match U-File unless otherwise specified | Typically 3500 px long side; do not upscale smaller originals |
| Cropping | Full photograph visible; mount/border retained as specified | Cropped with slim border; no loss of content | Match S-File crop |
| FADGI Aim | 4-Star preferred | Not applicable unless specified | Not applicable |
| Processing | Minimal; faithful reproduction | Approved crop, orientation, and tonal normalization | Derived from S-File |

### 4.3 Versos, Mounts, and Enclosures

Project-specific instructions must state whether the vendor should capture:

- Versos
- Captions
- Stamps
- Annotations
- Mounts
- Sleeves
- Enclosures
- Folder labels
- Item labels
- Barcodes.

When versos or associated enclosures are captured, the file naming convention must clearly distinguish front, back, mount, sleeve, enclosure, or label images.

## 5. Transmissive Photographic Materials: Film, Slides, Transparencies, and Glass

### 5.1 Included Materials

This category covers transmissive media, divided into two operational tracks based on whether the original source image is a negative or a native positive:

**Negative Materials Track:** Black-and-white negatives, color negatives, sheet film negatives, roll film negatives, nitrate negatives, acetate negatives, and glass plate negatives.

**Positive Materials Track:** Color transparencies, mounted slides (Kodachrome, Ektachrome, etc.), lantern slides, and glass transparencies.

### 5.2 Preservation and Derivative Concept

To preserve both the physical reality of a transmissive artifact and its human-readable interpretation, different asset counts and processing approaches are required depending on whether the original source media is a negative or a native positive:

**For Negative Materials (Film & Glass):** The vendor must maintain parallel production tracks, delivering six (6) files total per physical item: two preservation, two service (one negative, one positive), and two access JPEGs (one negative, one positive). The two mandatory preservation files are defined as follows:

**Negative Preservation Master (U-File):** A faithful, raw, un-inverted capture of the source negative as a negative image. For color negatives, the integral film base and orange mask must remain fully intact. The primary purpose of this file is to retain the absolute, objective physical and informational content of the film base.

**Positive Preservation Master:** A high-fidelity, digitally inverted positive image derived directly from the raw capture. This master must be tonally adjusted and optimized for visual interpretation, preserving maximum tonal information across the histogram while strictly avoiding highlight or shadow clipping, excessive contrast compression, or data loss.

**For Positive Materials (Slides & Transparencies):** Because these items are natively positive, no inversion or dual-tracking is required. The vendor shall deliver three (3) files total per physical item: one preservation (U-File), one production/service (S-File), and one web display/access JPEG. The preservation master represents a faithful, raw capture of the positive transparency or slide without any undocumented tonal adjustments.

### 5.3 Black-and-White Film Negatives (6-File Dual Track)

| Feature | Negative Preservation | Positive Preservation | Service Files (Both Negative & Positive required) | Access Derivatives (Both Negative & Positive required) |
|---|---|---|---|---|
| File format | TIFF | TIFF | TIFF | JPEG |
| Compression | Lossless ZIP (Deflate) | Lossless ZIP (Deflate) | Lossless ZIP (Deflate) | Lossy JPEG |
| Bit depth | 16-bit | 16-bit | 8-bit | 8-bit |
| Color mode | Grayscale | Grayscale | Grayscale | Grayscale |
| Color Profile | Gray Gamma 2.2 | Grey Gamma 2.2 | Grey Gamma 2.2 | Grey Gamma 2.2 |
| Resolution | Project-specific based on film format | Match negative preservation | Match or resize from preservation files | Match or resize from service files |
| Cropping | Full image area; rebate/edge markings retained if specified; no loss of image content | Cropped/oriented as specified | **Negative Service:** Matches Neg Master crop.<br><br>**Positive Service:** Matches Pos Master crop. | **Negative Access:** Matches Neg Service crop.<br><br>**Positive Access:** Matches Pos Service crop. |
| Processing | No inversion; no clipping; no undocumented tonal enhancement | Inverted and adjusted for visual clarity; no highlight/shadow clipping | **Negative Service:** Non-inverted; normalized contrast.<br><br>**Positive Service:** Inverted; approved visual optimization. | Derived directly from the corresponding Negative and Positive Service files |
| FADGI Aim | 4-Star preferred where feasible | Not applicable | Not applicable | Not applicable |

### 5.4 Color Film Negatives (6-File Dual Track)

| Feature | Negative Preservation | Positive Preservation | Service Files (Both Negative & Positive required) | Access Derivatives (Both Negative & Positive required) |
|---|---|---|---|---|
| File format | TIFF | TIFF | TIFF | JPEG |
| Compression | Lossless ZIP (Deflate) | Lossless ZIP (Deflate) | Lossless ZIP (Deflate) | Lossy |
| Bit depth | 16-bit per channel | 16-bit per channel | 8-bit per channel | 8-bit per channel |
| Color mode | RGB | RGB | RGB | RGB |
| Color profile | Adobe RGB (1998) | Adobe RGB (1998) | sRGB | sRGB |
| Resolution | Native optical resolution specified by film format | Match corresponding preservation | Match corresponding preservation | Typically 3500 px long side unless otherwise specified |
| Cropping | Full film frame visible; full rebate and edge markings retained. | Oriented as specified; may be cropped to image frame per SOW. | **Neg Service:** Matches Neg Master crop.<br><br>**Pos Service:** Matches Pos Master crop. | Matches corresponding Service Master crop exactly. |
| Processing | Raw capture; no corrections. Orange mask fully intact. | Digitally inverted, orange mask neutralized, color-corrected. No clipping. | Approved contrast and color-balance normalization. | Derived directly from corresponding Service files. |
| FADGI Aim | 4-Star preferred where feasible | Not applicable | Not applicable | Not applicable |

### 5.5 Color Transparencies and Mounted Slides (3-File Single Track)

This section applies to natively positive film transmissive materials (e.g., Kodachrome, Ektachrome, slides).

| Feature | Preservation / U-File | Service / S-File | Access Derivative |
|---|---|---|---|
| File format | TIFF | TIFF | JPEG |
| Compression | Lossless ZIP (Deflate) | Lossless ZIP (Deflate) | Lossy JPEG |
| Bit depth | 16-bit per channel (48-bit RGB) | 8-bit per channel (24-bit RGB) | 8-bit |
| Color mode | RGB | RGB | RGB |
| Color profile | Adobe RGB (1998) | sRGB | sRGB |
| Resolution | Native optical resolution per SOW. No software upscaling. | Match Preservation pixel dimensions exactly. | Typically 3500 px on long side. Do not upscale smaller originals. |
| Cropping | Full frame visible; slide mount or film border and background safety margin retained. | Slide mount/border cropped out; slight background safety margin retained. | Match S-File crop |
| Processing | Faithful, raw capture of the transparency; no undocumented adjustments. | Approved baseline contrast, color-balance, and tonal normalization. | Derived directly from the Service via standard downsampling. |
| FADGI Aim | 4-Star preferred | Not applicable unless specified | Not applicable |

### 5.6 Glass Plate Negatives and Glass Transparencies

Glass materials require specialized handling and will be mapped to the file structures established above via individual project SOWs:

**Glass Plate Negatives:** Shall follow the six (6) file dual-track role structure, inversion logic, and bit-depth specifications outlined for film negatives in Section 5.3 (Grayscale) or Section 5.4 (Color).

**Glass Transparencies and Lantern Slides:** Shall follow the three (3) file single-track role structure outlined for positive transmissive materials in Section 5.5.

#### 5.6.1 Technical Modifications for Glass Substrates

Regardless of the file track utilized, all glass-based materials must adhere to the following baseline modifications:

**Resolution:** Sampling frequency shall be defined in the project SOW relative to the physical dimensions of the glass plate (typically a minimum of 400 to 600 PPI natively), without digital interpolation.

**Cropping:** For Preservation file (U-Files), the entire physical glass plate must be fully visible. The vendor must retain all physical edges, corners, emulsion damage, glass cracks, silver mirroring, and historical labels or markings.

**Color Mode:** If a black-and-white glass negative exhibits severe chemical deterioration, silver mirroring, or hand-coloring, the Library may mandate an RGB color capture in the SOW to preserve these physical attributes.

### 5.7 Glass and Fragile Transmissive Handling Requirements

The vendor shall use handling and capture methods appropriate for fragile glass and transmissive photographic materials. Requirements may include:

- Low-heat or cold illumination
- Minimal exposure time
- Appropriate custom supports for cracked or structurally compromised glass
- No direct physical pressure placed on emulsion surfaces (e.g., placing glass plates emulsion-side up on a low-iron, anti-reflective lower glass shelf)
- Meticulous handling of flaking, lifting, or lifting emulsions
- Procedures for broken or cracked plates
- Immediate reporting of unstable or unsafe items
- Project-specific approval before attempting capture of damaged items.

Specific equipment may be proposed by the vendor, but the Scope of Work should describe the required outcome rather than requiring a named lighting system unless the Library has a specific technical reason to mandate it.

### 5.8 Inversion and Tonal Adjustment Requirements

For negative-to-positive conversions, the vendor shall provide a fully documented, repeatable inversion workflow. Positive files must be visually optimized for immediate display while retaining full tonal representation across the histogram.

The vendor shall avoid:

- Clipping highlights or shadows
- Excessive contrast expansion
- Unnatural tonal compression
- Automated correction that obscures source characteristics
- Removal of historically or physically meaningful marks
- Inconsistent positive rendering across a batch.

The Library may require approval of a pilot batch before production begins, especially for negative inversion and glass plate projects.

## 6. Microform Materials

### 6.1 Included Materials

This category includes:

- 16mm roll microfilm
- 35mm roll microfilm
- Positive microfilm
- Negative microfilm
- Silver gelatin, diazo, and vesicular film
- Microfiche
- Aperture cards
- Microfilm containing newspapers, books, manuscripts, records, drawings, or other source documents.

### 6.2 General Approach

Microform materials are already surrogates of original documents. The primary goal is usually legibility, completeness, accurate sequencing, and support for OCR and access. However, preservation files should still be created in a stable, well-documented format with sufficient tonal information to support future derivative creation.

### 6.3 Recommended Baseline Specifications

| Feature | Preservation / U-File | Production / Service / S-File | OCR / Text Derivative (Package) |
|---|---|---|---|
| File format | TIFF, single-page preferred unless multi-page is explicitly approved | TIFF (single-page or multi-page as specified in SOW) | Searchable PDF, ALTO XML, hOCR, plain text, or project-specific package |
| Compression | Lossless ZIP (Deflate) | Project-specific | Project-specific |
| Bit depth | 8-bit grayscale | 8-bit grayscale | N/A |
| Color mode | Grayscale unless source requires color | Grayscale unless source requires color | N/A |
| Resolution | 4,000 PPI for 35mm film or 6,000 PPI for 16mm film, measured across the film base | Match preservation or project-specific derivative size | OCR generated from approved image files |
| Cropping | Page/frame-level crop as specified; no cropped text or content | Cropped, deskewed, and oriented for reading | N/A |
| Enhancements | Deskew, crop, orientation, polarity correction, and tonal adjustment may be allowed if documented and approved | Searchable access package | OCR confidence and exception reporting as specified |
| Sequencing | Reel, frame, page, issue, volume, or item order as specified | Match preservation sequence | Match image sequence |

### 6.4 Reduction Ratio and Source-Sized PPI

When PPI is specified relative to original page size, the vendor shall document the method used to determine or estimate reduction ratio. If the reduction ratio is unknown, the vendor shall document assumptions and notify the Library if the source material cannot reasonably meet the required effective resolution.

### 6.5 Microfilm OCR

For OCR projects, the vendor shall provide project-specific OCR deliverables. Searchable PDF alone should not be the only OCR deliverable unless explicitly approved.

Possible OCR deliverables include:

- Searchable PDF
- Plain text
- ALTO XML
- hOCR
- METS/ALTO packages
- OCR confidence reports
- Exception reports for unreadable frames or pages.

The vendor shall identify source conditions likely to limit OCR quality, such as poor exposure, skew, density variation, bleed-through, blurred frames, damaged film, handwritten text, unusual typography, mixed languages, or complex layouts.

### 6.6 Aperture Cards and Technical Drawings

Aperture cards and microforms containing technical drawings, maps, or oversized originals may require higher effective resolution, special cropping, or delivery structures. Project-specific scopes should define these requirements separately.

## 7. File Naming and Directory Structure

### 7.1 General Naming Variations

All files delivered under this agreement shall follow a consistent, underscore-delimited naming convention based on the Library-issued 14-digit barcode identifier (pattern: `33433\d{9}`). To keep filenames clean and optimized for ingestion, the naming schema adapts based on the material microfilm/negative workflow:

1. **Standard Workflow (Reflective Materials, Slides, and Transparencies):**  
   `[barcode]_[side-or-sequence]_[role].[extension]`

2. **Dual-Track Negative Workflow (Film and Glass Negatives Only):**  
   `[barcode]_[component]_[side-or-sequence][role].[extension]`

3. **Multi-Unit Split Workflow (Only Microfilm Reels containing distinct sub-content):**  
   `[barcode]_u[unit]_[sequence]_[role].[extension]`

**Zero-Padding:** All page, frame, and asset sequences must be zero-padded to a strict five-digit (5) width (e.g., 00001). Sub-unit modifiers must be zero-padded to a three-digit (3) width (e.g., u001).

### 7.2 Naming Elements, Components, and Role Codes

| Element | Code / Term | Description |
|---|---|---|
| Barcode | `33433\d{9}` | The 14-digit unique identifier supplied by the Library. |
| Component (Negatives Only) | `negative`<br><br>`positive` | Used strictly for negative media to differentiate the raw un-inverted capture (negative) from the digitally inverted track (positive). Omitted for standard reflective and natively positive items. |
| Unit Modifier (Split Reels Only) | `u001` to `u999` | Appended only when a single barcode contains multiple distinct bibliographic units requiring independent digital separation. |
| Side or Sequence | `r`<br><br>`v`<br><br>`00001` to `99999` | Recto (front side) or Verso (back side) for physical flat objects or photographic prints.<br><br>5-digit zero-padded index for multi-page items or sequential film/microfilm frames. |
| Role | `pres`<br><br>`serv`<br><br>`access`<br><br>`ocr` | Preservation (U-File; 16-bit lossless ZIP TIFF).<br><br>Production / Service (S-File; cropped, color-normalized TIFF or JPEG2000).<br><br>Access Derivative / Searchable Package (Lossy JPEG or Searchable PDF).<br><br>Text Derivative (ALTO XML, hOCR, or plain text coordinates). |

### 7.3 Mandatory Sidecar Metadata Requirements

The vendor shall deliver file-level metadata utilizing individual, matching JSON sidecar files for every primary digital asset produced. Standing or bulk metadata files delivered in lieu of individual sidecars do not satisfy this requirement.

**Strict 1:1 Asset Pairing:** Every single image, document, or derivative file delivered (including all preservation masters, service masters, and access files) must be accompanied by exactly one corresponding JSON file. Combining or nesting metadata for multiple files into a single master JSON array or bulk manifest is strictly prohibited under this requirement.

**Exact Character Matching:** The filename of the JSON sidecar must match the base filename of its paired asset character-for-character, shifting only the file extension to lowercase `.json`. For example, `[filename]_pres.tif` must be paired with `[filename]_pres.json`, and `[filename]_access.jpg` must be paired with `[filename]_access.json`. Any case mismatches, truncation, or spacing discrepancies between the asset file and its sidecar file will result in a mandatory batch rework.

**Directory Co-location:** Each JSON sidecar file must reside within the exact same subfolder directory as its target asset. It must be written to the internal payload `/data` directory of the associated BagIt structure, sitting directly alongside the file it describes.

**Data Ingestion and Schema Compliance:** The internal structural formatting, required fields, and data values populated within each individual JSON sidecar file must strictly adhere to the external metadata workflow and schema validation rules outlined in Section 8.

### 7.4 Delivery Examples

#### Scenario A: Standard Reflective Photo Print with Front and Back (No Component Code)

**Barcode ID:** `33433123456789`

- **Front (Recto) Preservation Master & Sidecar:** `33433123456789_r_pres.tif` `33433123456789_r_pres.json`
- **Front (Recto) Access JPEG & Sidecar:** `33433123456789_r_access.jpg` `33433123456789_r_access.json`
- **Back (Verso) Preservation Master & Sidecar:** `33433123456789_v_pres.tif` `33433123456789_v_pres.json`

#### Scenario B: Complex Dual-Track Transmissive Negative (Component Required)

**Barcode ID:** `33433987654321`

- **Raw Negative Preservation Master & Sidecar:** `33433987654321_negative_00001_pres.tif` `33433987654321_negative_00001_pres.json`
- **Inverted Positive Preservation Master & Sidecar:** `33433987654321_positive_00001_pres.tif` `33433987654321_positive_00001_pres.json`

#### Scenario C: Microfilm Reel Split into Multiple Distinct Bibliographic Units (Pamphlets)

**Barcode ID:** `33433555554444` (Reel contains Pamphlet 1 and Pamphlet 2)

- **Pamphlet 1, Frame 1 Service Master & Sidecar:** `33433555554444_u001_00001_serv.tif` `33433555554444_u001_00001_serv.json`
- **Pamphlet 1, Frame 1 Access Searchable PDF & Sidecar:** `33433555554444_u001_00001_access.pdf` `33433555554444_u001_00001_access.json`
- **Pamphlet 2, Frame 1 Service Master & Sidecar:** `33433555554444_u002_00001_serv.tif` `33433555554444_u002_00001_serv.json`

### 7.5 Directory Structure: BagIt Packaging Rules

**Standard / Negative Items:** Each unique barcode identifier shall be delivered as an independent, self-contained, BagIt-compliant directory named exactly by its barcode (e.g., folder `33433987654321/`).

**Split Multi-Unit Items:** When a barcode is split into distinct intellectual units, each unit must be packaged as its own independent bag. To prevent folder collisions, the root folder name must include the unit modifier suffix (e.g., `33433555554444_u001/` and `33433555554444_u002/`).

#### Example 1: Basic Reflective Directory Layout Example (Photo Print with Front & Back)

```text
33433123456789/                                  <-- Root Folder (Named by Barcode + Unit Suffix)
├── bagit.txt                              <-- BagIt declaration
├── manifest-md5.txt                       <-- Cryptographic checksums for everything in /data
├── bag-info.txt                           <-- Bag administrative metadata
└── data/                                  <-- Payload directory
    ├── 33433123456789_r_pres.tif         <-- Front/Recto Preservation Master Image
    ├── 33433123456789_r_pres.json         <-- 1:1 Matching Sidecar JSON Metadata
    ├── 33433123456789_r_serv.tif         <-- Front/Recto Service Master Image
    ├── 33433123456789_r_serv.json         <-- 1:1 Matching Sidecar JSON Metadata
    ├── 33433123456789_r_access.jpg         <-- Front/Recto Access Image File
    ├── 33433123456789_r_access.json         <-- 1:1 Matching Sidecar JSON Metadata
    ├── 33433123456789_v_pres.tif         <-- Back/Verso Preservation Master Image
    ├── 33433123456789_v_pres.json         <-- 1:1 Matching Sidecar JSON Metadata
    ├── 33433123456789_v_serv.tif         <-- Back/Verso Service Master Image
    ├── 33433123456789_v_serv.json         <-- 1:1 Matching Sidecar JSON Metadata
    ├── 33433123456789_v_access.jpg         <-- Back/Verso Access Image File
    └── 33433123456789_v_access.json         <-- 1:1 Matching Sidecar JSON Metadata
```

#### Example 2: Complex Dual-Track Negative Directory Layout (Frame 1 of Roll)

```text
33433987654321/                                  <-- Root Folder (Named by Barcode)
├── bagit.txt                                    <-- BagIt declaration
├── manifest-md5.txt                             <-- Cryptographic checksums for everything in /data
├── bag-info.txt                                 <-- Bag administrative metadata
└── data/                                        <-- Payload directory
    ├── 33433987654321_negative_00001_pres.tif   <-- Frame 1 Raw Negative Preservation Master Image
    ├── 33433987654321_negative_00001_pres.json  <-- 1:1 Matching Sidecar JSON Metadata
    ├── 33433987654321_positive_00001_pres.tif   <-- Frame 1 Inverted Positive Preservation Master Image
    ├── 33433987654321_positive_00001_pres.json  <-- 1:1 Matching Sidecar JSON Metadata
    ├── 33433987654321_negative_00001_serv.tif   <-- Frame 1 Raw Negative Service Master Image
    ├── 33433987654321_negative_00001_serv.json  <-- 1:1 Matching Sidecar JSON Metadata
    ├── 33433987654321_positive_00001_serv.tif   <-- Frame 1 Inverted Positive Service Master Image
    ├── 33433987654321_positive_00001_serv.json  <-- 1:1 Matching Sidecar JSON Metadata
    ├── 33433987654321_negative_00001_access.jpg <-- Frame 1 Raw Negative Access Image File
    ├── 33433987654321_negative_00001_access.json<-- 1:1 Matching Sidecar JSON Metadata
    ├── 33433987654321_positive_00001_access.jpg <-- Frame 1 Inverted Positive Access Image File
    └── 33433987654321_positive_00001_access.json    <-- 1:1 Matching Sidecar JSON Metadata
```

#### Example 3: Split Microfilm Directory Layout (Pamphlet 1 of a Split Reel)

```text
33433555554444_u001/                             <-- Root Folder (Named by Barcode + Unit Suffix)
├── bagit.txt                                    <-- BagIt declaration
├── manifest-md5.txt                             <-- Cryptographic checksums for everything in /data
├── bag-info.txt                                 <-- Bag administrative metadata
└── data/                                        <-- Payload directory
    ├── 33433555554444_u001_00001_pres.tif       <-- Frame 1 Preservation Master Image
    ├── 33433555554444_u001_00001_pres.json      <-- 1:1 Matching Sidecar JSON Metadata
    ├── 33433555554444_u001_00001_serv.tif       <-- Frame 1 Service Master Image
    ├── 33433555554444_u001_00001_serv.json      <-- 1:1 Matching Sidecar JSON Metadata
    ├── 33433555554444_u001_00001_access.pdf     <-- Frame 1 Searchable PDF Access File
    ├── 33433555554444_u001_00001_access.json    <-- 1:1 Matching Sidecar JSON Metadata
    └── 33433555554444_u001_00001_ocr.xml        <-- Frame 1 Coordinate OCR data
```

## 8. Embedded Metadata and External Metadata

### 8.1 General Approach

The Library utilizes a multi-tiered metadata strategy to maintain digital object lineage. Technical and administrative metadata are captured at two distinct levels: minimal metadata embedded directly within file headers, and robust, file-level external metadata delivered via the JSON sidecar files specified in Section 7.3. External metadata files serve as the primary descriptive and validation mechanism for repository ingestion.

### 8.2 Embedded Metadata Requirements

The vendor shall embed baseline technical and administrative metadata directly into the headers of all TIFF and derivative files where supported by the file format. Embedded metadata fields must be populated programmatically during capture and processing, and may include:

- Unique identifier / Barcode
- File title or document name
- Library/institution name and credit line
- Copyright or rights statement (if supplied by the Library)
- Source collection name (if supplied by the Library)
- Capture date and timestamp
- Digitization vendor name
- Capture hardware metrics (Camera/scanner make, model, and lens information)
- Capture software name and version number
- Resolution (Sampling frequency) and bit depth
- Assigned color space profile (ICC Profile)
- Image pixel dimensions and orientation
- Standard technical EXIF, XMP, IPTC, and TIFF header fields

### 8.3 Checksums and Fixity

Cryptographic checksums used for file fixity validation must be delivered via the external BagIt manifests (`manifest-md5.txt`) as outlined in Section 7.5, rather than embedded as the primary fixity mechanism inside image headers or duplicated inside item sidecars. The mandatory algorithm for all project delivery manifests is MD5.

### 8.4 External Metadata Workflow and JSON Schema Validation

To generate the mandatory 1:1 file-level JSON sidecars required by Section 7.4, the vendor shall execute a three-phase metadata aggregation and synthesis workflow:

#### Phase 1: Library-Supplied Source Baseline

Prior to production or upon shipment delivery, the Library will provide the vendor with a standardized project inventory spreadsheet in CSV or XLSX format (as specified in the **[Inventory Spreadsheet Specification]({{< ref "inventory_spreadsheet-spec.md" >}})**). This file acts as the authoritative intake data source for the project and provides item-level baseline data, including:

- **Administrative Tracking:** `schema_version` and `project_code`
- **Primary Identifiers:** Library barcode (`barcode` matching `^33433\d{9}$`), `division_code`, `bnumber`, `classmark`, `aspace_component_id`, `collection_id`, and `item_title`
- **Physical Object Classification:** Controlled vocabulary pairings for `object_type` and `object_format`, alongside any `physical_condition_notes` observed at selection
- **Multi-Unit Structure:** `unit_index` and `unit_title` for single cataloged items spanning multiple carriers (e.g., split microfilm reels or multi-box sets)

#### Phase 2: Vendor-Generated JSON Synthesis

The vendor must programmatically extract the item-level fields from the Library's intake spreadsheet and map them into their corresponding schema objects (`administrative`, `identifiers`, `source`). The vendor's processing scripts must then synthesize this baseline data with file-level operational metadata captured dynamically during production to generate individual 1:1 JSON sidecar files. 

Per the **[JSON Sidecar Schema Specification]({{< ref "json-schema-sidecar.md" >}})**, the capture-specific properties the vendor must inject into each sidecar include:

- **Asset Metadata (`asset`):** The exact `referenceFilename` (strictly validated against the project naming regex pattern) and the designated `fileRole` (`pres`, `serv`, `access`, or `ocr`).
- **Sequential Capture Tracking (`source.sequence`):** The zero-padded integer `sequenceNumber` (e.g., `24`), two-sided object `side` indicator (`r` for recto, `v` for verso), and human-readable `sequenceLabel` depicting physical reality (e.g., `"Recto"`, `"Page 42"`, `"Front Cover"`).
- **Digitization Process Audit (`digitizationProcess`):** Granular hardware and software audit trails, including `captureDevice` (`manufacturer`, `model`, `lens`, `serialNumber`), `captureSoftware` (`manufacturer`, `productName`, `version`), and the specific optical `calibrationTarget` utilized during the capture session.
- **Operator & Organization Tracking (`digitizer`):** Vendor administrative data, including `operator` (`firstName`, `lastName`) and `organization` (`name`).

*(Note: To maintain separation of concerns, file sizes, pixel dimensions, and ICC profiles remain embedded within image headers per Section 8.2, while MD5 cryptographic checksums remain strictly within external BagIt manifests per Section 8.3).*

#### Phase 3: Schema Validation

The final structural composition, key-value pairings, nesting logic, and required fields of the delivered JSON sidecars must strictly validate against the formal JSON Schema specification provided by the Library.

**Schema Provision:** The authoritative, live JSON Schema file (`digitized_image_schema.json`) is maintained and published by the Library at the following canonical endpoint:
* **Canonical Schema URI (`$id`):** `https://nypl-research.github.io/digital-imaging-resources/schemas/digitized_image_schema.json`

**Mandatory 100% Pre-Delivery Validation:** The vendor shall implement automated command-line schema validation (using industry-standard tools such as `ajv-cli` or Python's `jsonschema`) as part of their 100% Quality Control pipeline (Section 9.1). Every single delivered JSON sidecar file must pass validation against the Library-supplied schema without error. Any files containing malformed JSON syntax, invalid data types, unmapped properties (`additionalProperties: false`), regex filename mismatches, or structural non-compliance will result in the immediate rejection of the entire delivery batch.

## 9. Quality Control Requirements

### 9.1 Vendor 100% QC

The vendor shall perform quality control before delivery. Unless otherwise specified, vendor QC shall include 100% review or automated validation for:

- File presence
- File naming
- Directory structure
- Sequence completeness
- Checksum creation
- File format validation
- ICC profile presence and correctness
- Bit depth
- Color mode
- Resolution metadata
- Pixel dimensions
- Corrupt or unreadable files
- Manifest completeness
- OCR deliverable presence, if applicable.

### 9.2 Vendor Visual QC

The vendor shall visually review files for issues including:

- Blurred focus
- Motion blur
- Incorrect exposure
- Clipped highlights or shadows
- Color imbalance
- Newton’s rings
- Dust or debris
- Reflections or glare
- Cropped text or image content
- Incorrect orientation
- Excessive skew
- Moiré or scanner artifacts
- Missing pages, frames, or sides
- Incorrect negative inversion
- Inconsistent tonal rendering
- Visible handling damage or newly discovered condition issues.

Unless a 100% manual visual review is explicitly funded in an SOW, the vendor shall conduct a manual visual inspection on a statistically valid random sample (minimum 10%) of each batch.

### 9.3 Technical Validation Tools

The vendor shall use appropriate validation and analysis tools, which may include:

- JHOVE for file format validation and characterization
- ExifTool for embedded metadata review
- OpenDICE, AutoSFR, GoldenThread, or equivalent tools for image quality conformance testing
- Checksum tools capable of generating MD5 manifests
- OCR validation or confidence reporting tools, where applicable.

### 9.4 Library Pilot Review

Before mass production, the Library may review a pilot batch. The pilot batch should be representative of the full project and may include:

- 25–50 images, or another agreed sample size
- Multiple formats and conditions
- Fronts/backs or rectos/versos
- Negative and positive versions for transmissive materials
- OCR output, if applicable
- Metadata records
- File manifests
- Checksum manifests
- QC reports
- Target images.

The Library may use the pilot to approve:

- Image quality
- Cropping
- Orientation
- Naming
- Directory structure
- Metadata structure
- Negative inversion look and tonal handling
- OCR package structure
- QC reporting format.

Full production shall not begin until the Library approves the pilot batch, unless the Library waives this requirement in writing.

### 9.5 Acceptance and Rework

Deliverables are not accepted until the Library completes its review and confirms that files, metadata, OCR, and documentation meet project requirements.

The vendor shall correct vendor-responsible errors at no additional cost. Rework may be required for:

- Missing files
- Incorrect file names
- Incorrect sequence
- Incorrect or missing checksums
- Corrupt files
- Incorrect bit depth, color profile, or file format
- Poor focus
- Cropped content
- Unauthorized image processing
- Clipped tonal values
- Incorrect negative inversion
- Incomplete metadata
- Incorrect OCR package structure
- Incomplete or inaccurate manifests
- Failure to follow approved specifications.
