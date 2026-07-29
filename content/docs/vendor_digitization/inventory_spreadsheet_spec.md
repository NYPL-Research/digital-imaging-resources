---
title: "Vendor Digitization Inventory Spreadsheet"
linkTitle: "Inventory Spreadsheet"
weight: 20
toc: true
description: "Schema specification, required fields, operational guidelines, and controlled vocabulary for vendor digitization inventory spreadsheets."
---

## 1. Overview and Workflow

When initiating an external digitization project, the Library provides vendors with a standardized metadata inventory spreadsheet. This document serves as the foundational tracking manifest for physical materials selected for digitization, establishes the baseline data required for item identification, and directly informs vendor scoping, equipment preparation, and cost estimates.

### 1.1 Downloads & Sample Files
* **Inventory Spreadsheet Template:** [NYPL_Vendor_Digital_Imaging_Inventory_Template.xlsx](/digital-imaging-resources/templates/NYPL_Vendor_Digital_Imaging_Inventory_Template.xlsx)
* **Sample Photograph Sidecar (Single-Unit):** [sample_photograph_sidecar.json](/digital-imaging-resources/templates/sample_photograph_sidecar.json)
* **Sample Split Microfilm Sidecar (Multi-Unit):** [sample_split_microfilm_sidecar.json](/digital-imaging-resources/templates/sample_split_microfilm_sidecar.json)

### 1.2 Completeness & Internal Tracking Fields
This spreadsheet is a shared tool between curatorial staff, the Vendor Digitization Services team, and external vendors. When filling out this sheet, staff must adhere to the following division of responsibilities:

* **Fill Out to the Best of Your Ability:** Not every field in the spreadsheet is mandatory. Some archival inventory items may not be fully cataloged, described in a finding aid, or possess formalized collection IDs. However, **because this inventory is used to calculate vendor estimates and resource allocation, it is vital that it be filled out as completely and accurately as possible.** If descriptive metadata exists, include it.
* **Internal Tracking Fields:** Users preparing inventories do not need to fill out `project_code` (Column C) if it is unassigned. The Vendor Digitization Services team will complete and verify administrative tracking codes before submitting the final sheet to a vendor.

### 1.3 How Vendors Must Use This Data
This spreadsheet represents the **initial selection and inventory stage** of the digitization workflow. The data provided here must be ingested by the vendor and used as the root source for generating item-level metadata during capture.

When delivering digitized assets back to the Library, the vendor is responsible for generating individual JSON sidecar files for each asset. To build valid sidecars, the vendor must:
1. **Map Library Metadata:** Parse the item-level fields from this spreadsheet (such as `barcode`, `division_code`, `object_type`, and `object_format`) directly into their corresponding schema paths in the final JSON sidecar.
2. **Append Capture Metadata:** Generate and populate all capture-specific technical and administrative fields that occur during digitization (e.g., `digitizationDate`, capture device specifications, capture software, and operator details).
3. **Append Asset-Level Metadata:** Generate individual file-level tracking data for every image captured (e.g., `fileRole`, `referenceFilename`, `frameNumber`, `sequenceNumber`, `side`, and `sequenceLabel`).

> **Scope Limitation:** Because technical capture fields, `schemaVersion`, and asset-level file specifications are generated dynamically during the digitization process, they are strictly excluded from this initial inventory spreadsheet.

---

## 2. Row Granularity: Physical vs. Intellectual Content

The spreadsheet must be populated according to the physical and intellectual structure of the materials being shipped. **Every item scheduled for digitization requires a valid barcode (`barcode`), or the project cannot be initiated.**

### 2.1 Standard Physical Granularity (One Row per Item)
As a baseline rule, each physical item being digitized (e.g., each bound volume, box, folder, reel, or photograph) must get its own dedicated row. If multiple physical items belong to a single catalog record (`bnumber`) or finding aid component, create a separate row for each physical carrier and reuse/repeat that `bnumber` or `shelf_locator` across those rows.

### 2.2 Intellectual Splitting on a Single Physical Item (Multi-Unit Objects)
Frequently, a single physical carrier (such as a volume of bound pamphlets or a microfilm reel) contains **multiple distinct intellectual works** that require the vendor to build separate digital packages/sidecars. Because splitting intellectual units impacts vendor pricing and capture workflows, staff must capture known complexities upfront:

* **Known Intellectual Units:** If staff know at the inventory stage that a single physical item must be split into multiple digital packages, create **one row per intellectual unit**. Repeat the physical `barcode` across every row associated with the item, increment the `unit_index` field sequentially (`1`, `2`, `3`, etc.), and provide descriptive titles in `unit_title`.
* **Unknown/Unscoped Splits:** If staff know a physical carrier contains multiple works but do not yet know the specific unit boundaries or titles, log **one row for the physical item**, leave `unit_index` and `unit_title` blank, and explicitly note the complexity in `physical_condition_notes` (e.g., *"Contains multiple titles; vendor scoping required to determine digital package splits"*).

---

## 3. Column Specification (A–P)

The spreadsheet follows an ordered curatorial citation structure, grouping `division_code`, `shelf_locator`, and `bnumber` together.

| Col | Column Header | Schema Path | Required | Allowed Values / Format | Notes |
|---|---|---|---|---|---|
| A | `barcode` | `source.identifiers.barcode` | **Yes** | `33433` + 9 digits | Primary item key; **mandatory to initiate** |
| B | `item_title` | `source.identifiers.title` | No | String | Plain text, no formatting |
| C | `project_code` | `administrative.projectCode` | **Yes** | String | Assigned by VDS team |
| D | `collection_id` | `source.identifiers.collectionId` | **Yes** | String | 3–7 digit code, not classmark |
| E | `division_code` | `source.identifiers.divisionCode` | **Yes** | Controlled vocabulary | Curatorial division code; use dropdown |
| F | `shelf_locator` | `source.identifiers.classmark` | No | String | Also known as classmark / call number |
| G | `bnumber` | `source.identifiers.bnumber` | No | String | Sierra / catalog record number |
| H | `object_type` | `source.object.type` | **Yes** | Controlled vocabulary | Broad material category; use dropdown |
| I | `object_format` | `source.object.format` | **Yes** | Controlled vocabulary | Must match valid `object_type`; use dropdown |
| J | `aspace_component_id` | `source.identifiers.aspaceComponentId` | No | String | ArchivesSpace component ref |
| K | `physical_condition_notes` | `source.notes.physicalConditionNotes` | No | Free text | Condition observed at selection / split notes |
| L | `unit_index` | `unit.unitIndex` | No | Integer ≥ 1 | For composite items like microfilm (e.g., `2` for u002) |
| M | `unit_title` | `unit.title` | No | Free text | For composite items like microfilm |
| N | `[INFO] estimated_page_count` | *(None)* | No | Integer | Logistics & estimates; strip before sidecar creation |
| O | `[INFO] is_oversized` | *(None)* | No | `TRUE`, `FALSE` | Use dropdown; strip before sidecar creation |
| P | `[INFO] needs_cataloging` | *(None)* | No | `TRUE`, `FALSE` | Use dropdown; strip before sidecar creation |

---

### 3.1 Non-Schema Tracking Columns (`[INFO]`)

Columns N, O, and P (`[INFO] estimated_page_count`, `[INFO] is_oversized`, and `[INFO] needs_cataloging`) are explicitly differentiated in the template with a **yellow header background**. They are color-coded differently because **this data will not be retained in final digital archival packages or sidecars**. 

However, **these fields are critical for calculating vendor cost estimates, timeline sizing, capture equipment allocation, and curatorial remediation.** Staff should make every effort to fill out these yellow columns whenever possible.

**Vendors must ignore and strip all `[INFO]` columns** when parsing the spreadsheet into automated production pipelines. These columns do not map to the metadata schema and must never appear in generated JSON sidecar files.

---

## 4. Controlled Vocabulary

### 4.1 Material Types (`object_type` & `object_format`)
To ensure data consistency and schema compliance across all projects, **users must use the built-in drop-down menus in the Excel template for `object_type` (Col H) and `object_format` (Col I)** rather than typing manual entries. 

The template features dependent data validation: selecting an `object_type` in Column H will automatically filter the allowed values in Column I (`object_format`) to only show legal pairings. Any unrecognized string or mismatched pair will fail schema validation.

| `object_type` (Column H Dropdown) | Valid `object_format` Values (Column I Dependent Dropdown) |
|---|---|
| `reflective textual and graphic` | `bound volume`, `loose paper` |
| `reflective photographic` | `photographic print` |
| `transmissive photographic` | `black-and-white negative`, `color negative`, `color transparency`, `mounted slide` |
| `glass substrate` | `glass plate negative`, `lantern slide` |
| `microform` | `16mm roll microfilm`, `35mm roll microfilm`, `microfiche`, `aperture card` |

### 4.2 Curatorial Division Codes (`division_code`)
Column E (`division_code`) requires a standardized administrative code selected from the built-in dropdown menu. Do not enter full division names.

| Code | Curatorial Division Name |
|---|---|
| `THE` | Billy Rose Theatre Division |
| `DAN` | Jerome Robbins Dance Division |
| `MUS` | Music Division |
| `RHA` | Rodgers and Hammerstein Archives of Recorded Sound |
| `TOFT` | Theatre on Film and Tape Archive |
| `BRG` | Berg Collection |
| `JWS` | Dorot Jewish Division |
| `GRD` | General Research Division |
| `ARN` | George Arents Collection |
| `MSS` | Manuscripts and Archives Division |
| `MAP` | Map Division |
| `LHG` | Milstein Division |
| `NYPLA` | NYPL Archives |
| `CPS` | Pforzheimer Collection |
| `RBK` | Rare Book Division |
| `ART` | Wallach Division: Art & Architecture Collection |
| `PHG` | Wallach Division: Photography Collection |
| `MMPC` | Wallach Division: Picture Collection |
| `PRN` | Wallach Division: Print Collection |
| `SPN` | Wallach Division: Spencer Collection |
| `SCF` | Schomburg Art and Artifacts Division |
| `SCR` | Schomburg Jean Blackwell Hutson Research and Reference Division |
| `SCM` | Schomburg Manuscripts, Archives and Rare Books Division |
| `SCL` | Schomburg Moving Image and Recorded Sound Division |
| `SCG` | Schomburg Photographs and Prints Division |

---

## 5. Worked Examples

### 5.1 Standard Single-Unit Item (Photographic Print)
For standard materials containing a single intellectual work on a single physical carrier, leave the unit index and unit title fields blank.

* **View Output Sample:** [sample_photograph_sidecar.json](/digital-imaging-resources/templates/sample_photograph_sidecar.json)

| Field | Value |
|---|---|
| `barcode` | `33433087654321` |
| `item_title` | `Portrait of unidentified woman, ca. 1910` |
| `project_code` | `NEH-2024-001` |
| `collection_id` | `col_4567` |
| `division_code` | `PHG` |
| `shelf_locator` | `MFZ (Photo) 99-12` |
| `bnumber` | `b10293847` |
| `object_type` | `reflective photographic` |
| `object_format` | `photographic print` |
| `aspace_component_id` | `aspace_c_00123` |
| `unit_index` | *(blank)* |
| `unit_title` | *(blank)* |
| `[INFO] estimated_page_count` | `1` |
| `[INFO] is_oversized` | `FALSE` |
| `[INFO] needs_cataloging` | `FALSE` |

### 5.2 Single Physical Item Containing Multiple Intellectual Works (Bound Pamphlets)
When staff know upfront that a single physical volume contains multiple distinct works that must be delivered as separate digital packages, repeat the physical barcode across rows while assigning sequential unit indexes and titles to estimate the scope of each digital package.

* **View Output Sample:** [sample_split_microfilm_sidecar.json](/digital-imaging-resources/templates/sample_split_microfilm_sidecar.json) *(Illustrates multi-unit sidecar packaging syntax)*

| `barcode` | `unit_index` | `unit_title` | `object_type` | `object_format` | `[INFO] estimated_page_count` |
|---|---|---|---|---|---|
| `33433999888777` | `1` | `An Essay on the Harbor of New York (1820)` | `reflective textual and graphic` | `bound volume` | `45` |
| `33433999888777` | `2` | `Regulations of the Port of New York (1822)` | `reflective textual and graphic` | `bound volume` | `30` |
| `33433999888777` | `3` | `Report of the Waterfront Commission (1825)` | `reflective textual and graphic` | `bound volume` | `60` |

---

## 6. Implementation & Validation Rules

* **Root Filename Generation:** The `barcode` value (Column A) serves as the primary identifier for the physical asset and must form the root prefix for all generated digital files. In the JSON sidecar, the `referenceFilename` attribute must always begin with this string.
* **Multi-Unit Naming Syntax:** For multi-unit items, the integer in `unit_index` (Column L) dictates the unit segment of the final filename. Vendors must zero-pad this integer to three digits using the `u00N` naming convention (e.g., `unit_index: 2` maps to filename segment `u002`).
* **Scoping Multi-Unit Packages:** When vendors ingest inventory rows where identical barcodes share multiple sequential `unit_index` numbers, they must configure their capture pipelines to generate distinct structural digital packages and sidecars for each unit segment, rather than combining them into a single asset package.
* **Internal Field Verification:** Prior to vendor distribution, the Vendor Digitization Services team is responsible for verifying and locking the `project_code` (Column C) field for the entire batch.
* **Template Dropdown Enforcement:** The Excel template provided by the Library contains pre-configured data validation rules for columns E (`division_code`), H (`object_type`), I (`object_format`), O (`is_oversized`), and P (`needs_cataloging`). Staff must not overwrite or paste plain text over these cells to prevent validation failures during ingestion.