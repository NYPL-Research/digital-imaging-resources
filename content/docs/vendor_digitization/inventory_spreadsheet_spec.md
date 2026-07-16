---
title: "Vendor Digitization Inventory Spreadsheet"
linkTitle: "Inventory Spreadsheet"
weight: 20
toc: true
description: "Schema specification, required fields, operational guidelines, and controlled vocabulary for vendor digitization inventory spreadsheets."
---

## 1. Overview and Workflow

When initiating an external digitization project, the Library provides vendors with a standardized metadata inventory spreadsheet. This document serves as the foundational tracking manifest for physical materials selected for digitization, establishes the baseline data required for item identification, and directly informs vendor scoping, equipment preparation, and cost estimates.

* **Download Template:** [NYPL_Vendor_Digital_Imaging_Inventory_Template.xlsx](/digital-imaging-resources/templates/NYPL_Vendor_Digital_Imaging_Inventory_Template.xlsx)

### 1.1 Completeness & Internal Tracking Fields
This spreadsheet is a shared tool between curatorial staff, the Vendor Digitization Services team, and external vendors. When filling out this sheet, staff must adhere to the following division of responsibilities:

* **Fill Out to the Best of Your Ability:** Not every field in the spreadsheet is mandatory. Some archival inventory items may not be fully cataloged, described in a finding aid, or possess formalized collection IDs. However, **because this inventory is used to calculate vendor estimates and resource allocation, it is vital that it be filled out as completely and accurately as possible.** If descriptive metadata exists, include it.
* **Internal Tracking Fields:** Users preparing inventories do not need to fill out `schema_version` (Column A) or `project_code` (Column B). These are internal administrative tracking fields; the Vendor Digitization Services team will complete and verify them before submitting the final sheet to a vendor.

### 1.2 How Vendors Must Use This Data
This spreadsheet represents the **initial selection and inventory stage** of the digitization workflow. The data provided here must be ingested by the vendor and used as the root source for generating item-level metadata during capture.

When delivering digitized assets back to the Library, the vendor is responsible for generating individual JSON sidecar files for each asset. To build valid sidecars, the vendor must:
1. **Map Library Metadata:** Parse the item-level fields from this spreadsheet (such as `barcode`, `division_code`, `object_type`, and `object_format`) directly into their corresponding schema paths in the final JSON sidecar.
2. **Append Capture Metadata:** Generate and populate all capture-specific technical and administrative fields that occur during digitization (e.g., `digitizationDate`, capture device specifications, capture software, and operator details).
3. **Append Asset-Level Metadata:** Generate individual file-level tracking data for every image captured (e.g., `fileRole`, `referenceFilename`, `frameNumber`, `sequenceNumber`, `side`, and `sequenceLabel`).

> **Scope Limitation:** Because technical capture fields and asset-level file specifications are generated dynamically during the digitization process, they are strictly excluded from this initial inventory spreadsheet.

---

## 2. Row Granularity and Barcode Requirements

The spreadsheet must be populated according to the physical structure of the materials being shipped. **It is critical that each physical item being digitized gets its own dedicated row.**

* **One Row per Physical Carrier:** Whether an item is a bound volume, folder, reel, glass plate, or individual photograph, it must be logged on its own row. If multiple physical items are associated with a single catalog record (`bnumber`) or finding aid component, create a separate row for each physical item and reuse/repeat that `bnumber` or `classmark` across those rows.
* **Mandatory Barcodes:** **Every item scheduled for digitization requires a valid barcode (`barcode`), or the project cannot be initiated.** If physical materials lack barcodes or if staff require assistance with barcoding workflows prior to vendor shipment, contact the Vendor Digitization Services team immediately.
* **Multi-Unit Objects:** Create one row per physical carrier when a single cataloged item spans multiple containers (e.g., a manuscript split across two microfilm reels). Repeat the primary `barcode` across every row associated with the item and increment the `unit_index` field sequentially (`1`, `2`, `3`, etc.).

---

## 3. Column Specification (A–P)

| Col | Column Header | Schema Path | Required | Allowed Values / Format | Notes |
|---|---|---|---|---|---|
| A | `schema_version` | `administrative.schemaVersion` | **Yes** | String, e.g., `1.0.0` | Completed by Vendor Digitization team |
| B | `project_code` | `administrative.projectCode` | No | String | Completed by Vendor Digitization team |
| C | `barcode` | `source.identifiers.barcode` | **Yes** | `33433` + 9 digits | Primary item key; **mandatory to initiate** |
| D | `division_code` | `source.identifiers.divisionCode` | **Yes** | String, e.g., `mic`, `pho` | Curatorial division code |
| E | `bnumber` | `source.identifiers.bnumber` | No | String | Sierra / catalog record number |
| F | `classmark` | `source.identifiers.classmark` | No | String | Call number / shelfmark |
| G | `aspace_component_id` | `source.identifiers.aspaceComponentId` | No | String | ArchivesSpace component ref |
| H | `collection_id` | `source.identifiers.collectionId` | No | String | Archival collection identifier |
| I | `item_title` | `source.identifiers.title` | No | String | Item-level bibliographic title |
| J | `object_type` | `source.object.type` | **Yes** | See controlled list below | Broad material category; use dropdown |
| K | `object_format` | `source.object.format` | **Yes** | See controlled list below | Must match valid `object_type`; use dropdown |
| L | `physical_condition_notes` | `source.notes.physicalConditionNotes` | No | Free text | Condition observed at selection |
| M | `unit_index` | `unit.unitIndex` | No | Integer ≥ 1 | Multi-unit items only (e.g., `2` for u002) |
| N | `unit_title` | `unit.title` | No | Free text | Multi-unit items only |
| O | `[INFO] estimated_page_count` | *(None)* | No | Integer | Logistics & estimates; strip before sidecar creation |
| P | `[INFO] is_oversized` | *(None)* | No | Boolean / String | Logistics & estimates; strip before sidecar creation |

---

### 3.1 Non-Schema Tracking Columns (`[INFO]`)

Columns O and P (`[INFO] estimated_page_count` and `[INFO] is_oversized`) are explicitly differentiated in the template with a **yellow header background**. They are color-coded differently because **this data will not be retained in final digital archival packages or sidecars**. 

However, **these fields are critical for calculating vendor cost estimates, timeline sizing, and capture equipment allocation.** Staff should make every effort to fill out these yellow columns whenever possible.

**Vendors must ignore and strip all `[INFO]` columns** when parsing the spreadsheet into automated production pipelines. These columns do not map to the metadata schema and must never appear in generated JSON sidecar files.

---

## 4. Controlled Vocabulary — Material Types

To ensure data consistency and schema compliance across all projects, **users must use the built-in drop-down menus in the Excel template for `object_type` and `object_format`** rather than typing manual entries. 

The template features dependent data validation: selecting an `object_type` in Column J will automatically filter the allowed values in Column K (`object_format`) to only show legal pairings. Any unrecognized string or mismatched pair will fail schema validation.

| `object_type` (Column J Dropdown) | Valid `object_format` Values (Column K Dependent Dropdown) |
|---|---|
| `reflective textual and graphic` | `bound volume`, `loose paper` |
| `reflective photographic` | `photographic print` |
| `transmissive photographic` | `black-and-white negative`, `color negative`, `color transparency`, `mounted slide` |
| `glass substrate` | `glass plate negative`, `lantern slide` |
| `microform` | `16mm roll microfilm`, `35mm roll microfilm`, `microfiche`, `aperture card` |

---

## 5. Worked Examples

### 5.1 Single-Unit Item (Photographic Print)
For standard single-unit materials, leave the unit index and unit title fields blank.

| Field | Value |
|---|---|
| `schema_version` | `1.0.0` |
| `project_code` | `NEH-2024-001` |
| `barcode` | `33433087654321` |
| `division_code` | `pho` |
| `bnumber` | `b10293847` |
| `item_title` | `Portrait of unidentified woman, ca. 1910` |
| `object_type` | `reflective photographic` |
| `object_format` | `photographic print` |
| `unit_index` | *(blank)* |
| `unit_title` | *(blank)* |
| `[INFO] estimated_page_count` | `1` |
| `[INFO] is_oversized` | `FALSE` |

### 5.2 Multi-Unit Item (Split Microfilm Reel)
When a single cataloged item spans multiple physical carriers, repeat the metadata across rows while incrementing the unit index.

| `barcode` | `unit_index` | `unit_title` | `object_type` | `object_format` | `[INFO] estimated_page_count` |
|---|---|---|---|---|---|
| `33433555554444` | `1` | `Vol. 1, Jan–Jun 1920` | `microform` | `35mm roll microfilm` | `850` |
| `33433555554444` | `2` | `Vol. 1, Jul–Dec 1920` | `microform` | `35mm roll microfilm` | `820` |

---

## 6. Implementation & Validation Rules

* **Root Filename Generation:** The `barcode` value (Column C) serves as the primary identifier for the physical asset and must form the root prefix for all generated digital files. In the JSON sidecar, the `referenceFilename` attribute must always begin with this string.
* **Multi-Unit Naming Syntax:** For multi-unit items, the integer in `unit_index` (Column M) dictates the unit segment of the final filename. Vendors must zero-pad this integer to three digits using the `u00N` naming convention (e.g., `unit_index: 2` maps to filename segment `u002`).
* **Internal Field Verification:** Prior to vendor distribution, the Vendor Digitization Services team is responsible for verifying and locking the `schema_version` (Column A) and `project_code` (Column B) fields for the entire batch.
* **Template Dropdown Enforcement:** The Excel template provided by the Library contains pre-configured dependent data validation rules for columns J (`object_type`) and K (`object_format`). Staff must not overwrite or paste plain text over these cells to prevent validation failures during ingest.