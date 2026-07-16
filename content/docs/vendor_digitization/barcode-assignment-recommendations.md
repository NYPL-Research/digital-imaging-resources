---
title: "Barcode Assignment and Application Recommendations"
linkTitle: "Barcode Recommendations"
weight: 40
toc_hide: false
description: "Draft recommendations for assigning, applying, recording, and validating barcodes for image-based vendor digitization projects."
---

# Barcode Assignment and Application Recommendations

> **Status:** Discussion draft  
> **Purpose:** Establish a practical, scalable barcode framework for preparing image-based collection materials for vendor digitization.  
> **Scope:** Physical collection materials selected for outsourced image-based digitization, including bound volumes, manuscripts, photographs, negatives, transparencies, glass plates, microforms, oversized materials, and mixed archival collections.

## 1. Purpose

Reliable barcode assignment is a foundational requirement for vendor digitization. A barcode provides the persistent physical identifier that connects:

- the source collection object or enclosure;
- the Library’s inventory and descriptive systems;
- vendor shipment and production tracking;
- digital filenames and JSON sidecars;
- BagIt packaging and delivery manifests;
- quality-control and rework workflows; and
- the returned physical material and resulting digital assets.

Unlike Audio and Moving Image workflows, image-based collections do not currently follow one uniform institution-wide practice for determining which physical level should receive a barcode. The appropriate level may be obvious for a single bound volume or microfilm reel, but less obvious for a manuscript box containing many folders, a box of photographic prints, or a slide box containing hundreds of individual images.

This document proposes a consistent decision framework while recognizing that barcodes may be recorded in different systems depending on the collection and material type. It focuses primarily on:

1. what a barcode should identify;
2. which physical level should be barcoded;
3. where and how a barcode should be applied;
4. how parent containers and subordinate digitization units should relate;
5. how barcodes should support vendor production and digital delivery; and
6. the minimum information that must be recorded before materials leave the Library.

## 2. Executive Recommendation

The Library should distinguish between two barcode roles.

### 2.1 Container Barcode

A **container barcode** identifies a custody, storage, or transport container such as:

- an archival box;
- a microfilm box;
- a slide box;
- a negative box;
- a portfolio;
- a map folder;
- a tray; or
- another top-level housing.

The container barcode supports:

- location and movement control;
- shipment reconciliation;
- box-level counts;
- parent-child relationships;
- return verification; and
- top-container management in systems such as ArchivesSpace.

A container barcode does **not automatically become the identifier used for digital filenames or BagIt packaging**.

### 2.2 Digitization-Unit Barcode

A **digitization-unit barcode** identifies the physical unit that is treated as one independently controlled digitization object.

The digitization-unit barcode is the identifier used for:

- the vendor inventory record;
- digital filenames;
- JSON sidecars;
- BagIt root directories;
- quality-control reports;
- exception and rework tracking; and
- repository ingest.

Examples of digitization units include:

- one bound volume;
- one manuscript folder;
- one photographic print in an individual enclosure;
- one photograph album;
- one microfilm reel;
- one roll of film negatives;
- one glass plate;
- one map in an individual folder; or
- one physically coherent group intentionally digitized as a single object.

### 2.3 Parent-Child Relationship

When a container holds multiple digitization units, both levels should be represented:

```text
Container barcode: 33433111111111
├── Folder barcode: 33433222222222
├── Folder barcode: 33433333333333
└── Folder barcode: 33433444444444
```

The container barcode supports custody and location. Each child barcode identifies a separate digitization package.

This distinction prevents one barcode from being forced to serve incompatible purposes.

## 3. Core Policy Principles

### 3.1 Barcode the Smallest Stable, Meaningful Control Unit

The digitization-unit barcode should identify the smallest physical unit that is:

- stable enough to handle independently;
- meaningful within the collection’s existing arrangement;
- practical to inventory and reconcile;
- expected to remain intact during vendor processing; and
- appropriate to represent as one digital package.

The smallest individual sheet, photograph, or frame should not automatically receive a barcode. Granularity should be driven by control, retrieval, arrangement, access, and production needs—not simply by the number of images created.

### 3.2 Do Not Barcode Every Digital Image

A barcode identifies a physical source unit, not every resulting digital file.

Pages, frames, rectos, versos, and derivatives are distinguished through:

- sequence numbers;
- side indicators;
- file-role codes;
- `negative` and `positive` components where applicable; and
- file-level JSON sidecars.

### 3.3 One Active Barcode Must Identify One Physical Control Unit

A barcode must not be reused for another item or container.

When an item is rehoused, the existing active barcode should normally remain associated with the same physical control unit. If a replacement barcode is required, the prior barcode must be retained in the record as inactive or superseded rather than silently reassigned.

### 3.4 Barcodes Must Not Encode Descriptive Meaning

The number should function as a persistent unique identifier. Collection, format, division, date, box, folder, and project meaning should be stored in metadata rather than inferred from the barcode number.

### 3.5 No Barcode Without a Record

Every barcode assigned for digitization must be logged before shipment.

At minimum, the barcode record must identify:

- what the barcode represents;
- the parent container, when applicable;
- the collection or catalog record;
- the material type;
- the responsible division;
- the current location; and
- the system or inventory in which the barcode is recorded.

### 3.6 Apply Barcodes to Housings, Not Collection Surfaces

The default practice should be to apply barcode labels to an appropriate enclosure rather than directly to original collection material.

Examples include:

- archival folders;
- envelopes;
- sleeves;
- four-flap enclosures;
- phase boxes;
- clamshell boxes;
- microfilm boxes;
- negative envelopes;
- backing cards; and
- protective wrappers.

Direct application to an original object should occur only when allowed by an established Library labeling policy and approved for that material category.

### 3.7 The Vendor Must Not Create or Reassign Library Barcodes

The Library must assign and record all authoritative barcodes before shipment.

A vendor may:

- scan and validate supplied barcodes;
- report missing, duplicated, damaged, or unreadable labels;
- use temporary internal production identifiers; and
- propose unit boundaries during a pilot.

A vendor must not:

- generate replacement Library identifiers;
- reassign a barcode;
- alter parent-child relationships;
- split or combine digitization units without authorization; or
- treat an internal vendor identifier as the Library’s authoritative barcode.

## 4. Definitions

| Term | Definition |
|---|---|
| **Physical item** | A tangible source object or carrier, such as a volume, folder, print, negative, plate, reel, or fiche. |
| **Container** | A housing that holds one or more physical items or digitization units. |
| **Container barcode** | A barcode used primarily for custody, storage, transport, and location control. |
| **Digitization unit** | The physical unit treated as one independently inventoried and packaged digitization object. |
| **Digitization-unit barcode** | The barcode used in filenames, sidecars, BagIt packaging, QC, and ingest. |
| **Intellectual unit** | A distinct body of content based on arrangement or description, such as a pamphlet, folder, issue, or report. |
| **Parent barcode** | The barcode of the container that physically holds a subordinate digitization unit. |
| **Sequence** | The ordered series of pages, frames, sides, or images produced from one digitization unit. |
| **Multi-unit physical item** | One physical carrier containing multiple intellectual units, such as a microfilm reel containing several pamphlets. |

## 5. Decision Framework

Use the following questions in order.

### Step 1: Is the material already cataloged or retrieved as an independent item?

Examples:

- a cataloged book;
- a bound manuscript volume;
- an individually described map;
- an individual photograph;
- a microfilm reel;
- a glass plate.

**Recommendation:** Assign one digitization-unit barcode to the item or its dedicated enclosure.

### Step 2: Is the material a container holding multiple independently meaningful units?

Examples:

- a manuscript box containing folders;
- a photograph box containing individually sleeved prints;
- a slide box containing separately organized groups;
- a box containing multiple volumes.

**Recommendation:** Assign:

1. one container barcode to the box or outer housing; and
2. separate digitization-unit barcodes to the subordinate units that will become independent digital packages.

### Step 3: Are the subordinate units too granular to barcode individually?

Examples:

- hundreds of individual sheets within one correspondence folder;
- individual pages in a volume;
- individual frames on one microfilm reel;
- individual exposures on one negative roll;
- individual slides that are not separately described or retrieved.

**Recommendation:** Barcode the enclosing stable unit and distinguish the subordinate images through sequence metadata.

### Step 4: Does one physical carrier contain multiple intellectual works?

Examples:

- one microfilm reel containing several pamphlets;
- one bound volume containing several separately titled works;
- one scrapbook containing multiple sections.

**Recommendation:** Retain one digitization-unit barcode for the physical carrier unless the contents are physically separated and independently controlled.

Represent internal intellectual divisions using:

- `unitIndex`;
- `unitTitle`;
- `u###` directories inside the BagIt `data/` directory; and
- an uninterrupted absolute sequence across the complete physical item.

### Step 5: Would the proposed barcode level create an unmanageably large or ambiguous digital object?

Consider:

- number of folders;
- expected image count;
- independent descriptive records;
- restrictions or rights differences;
- format changes;
- expected retrieval;
- likelihood of partial rework;
- vendor production routing; and
- repository ingest requirements.

**Recommendation:** Move the digitization-unit barcode down one meaningful physical level, normally from box to folder or from folder to individually enclosed item.

## 6. Recommended Barcode Levels by Material Type

| Material type | Container barcode | Default digitization-unit barcode | Generally do not barcode | Notes |
|---|---|---|---|---|
| Cataloged book or bound volume | Optional housing barcode | Each volume | Individual pages | Multi-volume works receive one barcode per physical volume. |
| Manuscript box with correspondence or records | Box | Each folder | Individual sheets | Folder-level barcoding is the recommended default. |
| Single loose manuscript item | Folder or enclosure | Individual item or dedicated enclosure | Recto and verso separately | Use one barcode; represent sides in filenames. |
| Scrapbook or album | Optional housing barcode | Each bound scrapbook or album | Individual leaves, photographs, or inserts | Sequence all component images under the volume barcode. |
| Box of individually described photographic prints | Box | Each individually enclosed print | Front and back separately | Use `r` and `v` for front/back captures. |
| Box of grouped photographic prints | Box | Folder, envelope, or coherent packet | Each print unless independently described | Project-specific item-level barcoding may be appropriate. |
| Mounted photograph, cabinet card, or carte de visite | Box or folder | Each individually enclosed object | Front, back, and mount separately | Associated views share the same barcode. |
| Photograph album | Optional housing barcode | Each album | Individual photographs | Sequence pages and details beneath the album barcode. |
| Sheet-film negative | Box | Each individually enclosed negative | Positive derivative separately | `negative` and `positive` filename components share one source barcode. |
| Glass plate negative | Box | Each plate enclosure | The glass surface | Never place the barcode directly on the glass or emulsion. |
| Roll-film negative | Can, box, or roll enclosure | Each physical roll or strip selected as the control unit | Individual exposures | Frames remain in absolute sequence. |
| Mounted slide | Slide box or page | Project-specific: individual slide, slide page, tray, or coherent group | Individual slide when not separately described | Granularity must be determined during project planning. |
| Color transparency | Box or enclosure | Each individually controlled transparency or coherent sheet/packet | Positive component in filename | Natively positive materials do not use the `positive` filename component. |
| Microfilm reel | Reel box | Each reel | Individual frames or internal works | Internal works may use `u###` directories under the reel barcode. |
| Microfiche | Fiche box | Each fiche or explicitly approved fiche set | Individual frames | Project scope must define whether a set is treated together. |
| Aperture cards | Box or tray | Each card when independently controlled; otherwise approved tray or batch unit | Image area separately | Large homogeneous sets may require a documented batch exception. |
| Map, poster, broadside, or oversized sheet | Drawer, portfolio, or folder | Each individually enclosed object | Recto and verso separately | Apply label to the folder, sleeve, or portfolio. |
| Rolled item | Tube or outer container | Each independently controlled roll or item enclosure | Sections created during capture | Rehousing may be required before labeling. |
| Framed or mounted work | Shipping case or wrapper | Frame backing, protective wrapper, or dedicated enclosure | Image or decorative mount surface | Placement requires collection-management or conservation approval. |
| Mixed-format archival box | Box | Folder, envelope, volume, or format-specific enclosure | Individual sheets by default | Use child units that support safe routing and vendor handling. |

## 7. Detailed Recommendations for Common Scenarios

### 7.1 Bound Books and Volumes

Assign one digitization-unit barcode per physical volume.

The barcode should be applied according to the following preference order:

1. a dedicated preservation enclosure;
2. a removable barcode flag, wrapper, or book band;
3. an approved location on a modern or general-collection binding; or
4. another location approved by Collection Management or Conservation.

Do not:

- place a barcode over original labels, inscriptions, stamps, or decorative elements;
- treat separate pages as separate barcode units;
- use one barcode for an entire multi-volume set; or
- apply an adhesive label directly to a rare or vulnerable binding without approval.

For a multi-volume work:

```text
Volume 1 → one barcode and one BagIt bag
Volume 2 → one barcode and one BagIt bag
Volume 3 → one barcode and one BagIt bag
```

### 7.2 Boxes of Correspondence and Other Foldered Records

The recommended default is:

- one container barcode for the archival box; and
- one digitization-unit barcode for each folder selected for digitization.

Do not barcode every letter or sheet unless the collection is already arranged, described, and retrieved at item level or the project explicitly requires item-level digital objects.

Example:

```text
Box barcode: 33433111111111
├── Folder 1 barcode: 33433222222222
│   └── 126 page images
├── Folder 2 barcode: 33433333333333
│   └── 83 page images
└── Folder 3 barcode: 33433444444444
    └── 211 page images
```

The folder barcode—not the box barcode—is used for the filenames and BagIt root of each folder-level delivery.

The box barcode is retained in the inventory as `parentBarcode`.

A folder may contain many pieces without requiring sub-item barcodes. The vendor should preserve physical order and assign page-level sequence numbers beneath the folder barcode.

#### When to split a folder into multiple barcode units

A folder should be divided into multiple barcode units only when:

- it already contains clearly established subfolders or packets;
- the units are separately described;
- separate rights or restrictions apply;
- the physical volume cannot be safely handled as one unit;
- different formats require separate production workflows;
- the units are expected to become separate access objects; or
- Collection Management or archival processing approves a physical subdivision.

Digitization staff or vendors should not independently reorganize archival folders solely to reduce image counts.

### 7.3 Photographic Prints

For individually described or independently retrieved photographs, assign one barcode per photograph and apply it to the photograph’s enclosure.

One barcode may govern multiple captures of the same object, including:

- recto;
- verso;
- mount;
- sleeve;
- enclosure;
- caption;
- label; and
- associated detail views.

For photographic groups that are not item-level described, use the folder, envelope, packet, or other coherent housing as the digitization unit.

The project plan should state whether access and repository objects will be created:

- per photograph;
- per folder;
- per packet; or
- per box.

### 7.4 Negatives, Transparencies, and Slides

#### Sheet-film and glass negatives

Assign one barcode per individually controlled negative or plate enclosure.

The same barcode governs both delivery tracks:

```text
[barcode]_negative_00001_pres.tif
[barcode]_positive_00001_pres.tif
```

Do not assign separate barcodes to the negative and positive renderings. They are digital representations of the same physical source.

#### Roll film

Assign one barcode per physical roll or stable strip unit defined by the project.

Individual exposures are represented through sequence numbers rather than barcodes.

#### Slides and transparencies

Natively positive slides and transparencies do not use the word `positive` in the filename.

For large slide collections, the digitization unit may be:

- an individual slide;
- a slide page;
- a tray;
- a box;
- a photographer-defined group; or
- another stable arrangement unit.

The project must define the selected level before barcoding begins. Item-level barcoding should be used when individual slides are already described, retrieved, or expected to become separate repository objects. Group-level barcoding may be more practical for large, minimally processed collections.

### 7.5 Microfilm

Assign one digitization-unit barcode per physical microfilm reel.

Do not assign new physical barcodes to pamphlets, issues, volumes, or other intellectual units contained within the same reel unless they are physically separated carriers.

When a reel contains several intellectual works:

```text
33433555554444/
└── data/
    ├── u001/
    ├── u002/
    └── u003/
```

The reel retains one barcode and one BagIt bag.

Internal unit membership is represented through:

- `unitIndex`;
- `unitTitle`;
- `u###` directories; and
- absolute sequence numbers that never reset across the reel.

### 7.6 Oversized and Flat Materials

Assign one digitization-unit barcode per independently controlled map, poster, broadside, drawing, or other oversized object.

Apply the barcode to:

- the object’s folder;
- a polyester sleeve;
- a portfolio;
- a wrapper; or
- another approved enclosure.

A flat-file drawer, portfolio, or transport folder may also receive a separate container barcode.

Do not apply the barcode directly to the image surface, verso, mount, or backing unless specifically approved.

### 7.7 Mixed-Format Boxes

Mixed-format boxes should receive a container barcode. Subordinate digitization units should be assigned based on the smallest stable, meaningful housing.

Examples:

```text
Box barcode
├── Folder barcode: correspondence
├── Envelope barcode: photographic negatives
├── Volume barcode: ledger
└── Folder barcode: maps and diagrams
```

Separate child barcodes can support different vendor routing and technical specifications while preserving the parent box relationship.

## 8. Barcode Placement and Labeling

### 8.1 General Placement Rules

Barcode labels should:

- remain visible without disturbing the collection object;
- be placed consistently across a project;
- include the human-readable 14-digit number;
- avoid seams, folds, fasteners, edges, and curved surfaces;
- avoid existing descriptive labels and annotations;
- remain scannable when the unit is packed normally;
- be applied to the enclosure body rather than a removable lid when practical; and
- be tested with the intended scanner after application.

### 8.2 Recommended Placement Zones

These zones are proposed starting points and require confirmation from Collection Management and Conservation.

| Housing | Recommended placement |
|---|---|
| Archival record box | Short end of box body, upper-right area, clear of existing box label |
| Manuscript folder | Exterior front, upper-right area, below or beside the descriptive label |
| Envelope | Exterior front, upper-right area |
| Four-flap enclosure | Exterior front panel, away from folds |
| Photograph sleeve | On a separate backing card, envelope, or approved label area—not over the image |
| Book box or phase box | Exterior front or spine-facing panel |
| Microfilm box | Exterior face visible during normal handling |
| Glass-plate enclosure | Exterior of four-flap enclosure or box |
| Map folder or portfolio | Exterior upper-right area, clear of title and call-number information |
| Slide page or tray | Stable label area on the page, tray, or associated divider |

### 8.3 Label Materials

The Library should adopt approved label stock for at least three application categories:

1. folders and box-board;
2. approved book covers or book enclosures; and
3. plastic, metal, or other non-paper housings.

One adhesive and label stock should not be assumed safe or effective for every surface.

Final material specifications should be reviewed by Conservation and Collection Management before implementation.

### 8.4 Temporary Barcode Control Sheets

For vendor digitization, each digitization unit should also receive a removable **barcode control sheet** or lead card when practical.

The control sheet may include:

- scannable barcode;
- human-readable barcode;
- collection title;
- box and folder number;
- item or unit title;
- expected sides or sequence;
- special handling notes;
- restriction flags; and
- project code.

The control sheet should be placed at the beginning of the digitization unit and used by the vendor to initialize production tracking.

Unless specifically required as documentation, the control sheet should not be delivered as a preservation or access image.

## 9. Recording Barcodes and System Responsibilities

The final institution-wide system of record may vary by collection type. This policy should therefore establish a minimum cross-system model without requiring one application to solve every use case immediately.

### 9.1 Cataloged Items in Sierra

For cataloged books and other item-level materials, the digitization-unit barcode should be recorded in the applicable Sierra item record when Sierra is the authoritative physical-item system.

The project inventory should also include:

- Sierra bibliographic identifier;
- item record identifier, where available;
- call number;
- division;
- title; and
- current location.

### 9.2 Archival Containers in ArchivesSpace

ArchivesSpace should be used for top-container barcodes where boxes, reels, trays, portfolios, or similar containers are represented as top containers.

A local decision is still required for recording folder-level or item-level digitization barcodes when those units do not correspond to ArchivesSpace top containers.

Possible implementation options for review include:

- a local structured field;
- a user-defined field;
- an external identifier;
- a linked digital-preparation record;
- a controlled project registry keyed to the ArchivesSpace component URI; or
- a future collections-management integration.

### 9.3 SPEC

Because SPEC is expected to be deprecated, new barcode policy should not depend on SPEC as the sole authoritative system.

Existing SPEC identifiers and records may be retained and crosswalked where needed, but the future workflow should remain functional without new SPEC development.

### 9.4 Interim Barcode Registry

Until a durable institution-wide system is selected, the Library should maintain a controlled barcode registry for image digitization.

The registry may initially be a governed table, database, or standardized project spreadsheet, provided that:

- barcode issuance is controlled;
- duplicate values are prevented;
- changes are auditable;
- parent-child relationships are retained;
- system record identifiers are included; and
- the registry can export the vendor inventory format.

The project inventory sent to the vendor is a production manifest, not necessarily the permanent system of record.

## 10. Minimum Barcode Metadata

Each barcode record should include the following fields.

| Field | Requirement | Description |
|---|---|---|
| `barcode` | Required | Unique 14-digit Library barcode |
| `barcodeRole` | Required | `container` or `digitizationUnit` |
| `parentBarcode` | Conditional | Barcode of the containing box, tray, portfolio, or other parent |
| `divisionCode` | Required | Responsible Library division |
| `collectionId` | When available | Collection-level identifier |
| `bnumber` | When applicable | Sierra bibliographic identifier |
| `classmark` | When applicable | Call number or classmark |
| `aspaceComponentId` | When applicable | ArchivesSpace component or record identifier |
| `title` | Required | Human-readable title or unit description |
| `containerType` | Required for containers | Box, tray, portfolio, reel box, etc. |
| `unitType` | Required for digitization units | Volume, folder, print, reel, negative, plate, fiche, etc. |
| `boxNumber` | When applicable | Existing collection box number |
| `folderNumber` | When applicable | Existing folder number |
| `location` | Required | Current physical location |
| `systemOfRecord` | Required | Sierra, ArchivesSpace, SPEC, barcode registry, or approved alternative |
| `systemRecordId` | When available | Persistent system identifier or URI |
| `projectCode` | Required for project work | Digitization project identifier |
| `barcodeStatus` | Required | Active, replaced, missing, damaged, cancelled, or other controlled status |
| `dateAssigned` | Required | Date barcode was assigned |
| `assignedBy` | Required | Staff member or unit responsible |
| `notes` | Optional | Exceptions, restrictions, condition, or handling notes |

## 11. Vendor Inventory Requirements

Before shipment, the Library must provide the vendor with an inventory that:

- includes every digitization-unit barcode;
- identifies parent container barcodes;
- distinguishes container records from digitization-unit records;
- states the expected digitization granularity;
- records box, folder, volume, reel, or item designations;
- provides titles and collection identifiers;
- identifies known multi-unit physical items;
- flags restricted or fragile materials;
- identifies expected file roles;
- defines expected sequence behavior; and
- includes any approved exceptions.

The vendor must reconcile the physical shipment against the inventory before production begins.

## 12. Quality-Control Requirements

### 12.1 Pre-Shipment QC

The Library should verify 100% of assigned barcodes for:

- uniqueness;
- correct number length and format;
- scan readability;
- correct placement;
- correct physical association;
- correct barcode role;
- parent-child relationship;
- system or registry entry;
- inventory inclusion;
- consistency between human-readable and encoded values; and
- absence of duplicate or conflicting active barcodes.

### 12.2 Vendor Intake QC

At intake, the vendor should verify:

- every expected container was received;
- every expected digitization unit was received;
- each barcode scans successfully;
- barcode values match the inventory;
- parent-child relationships match the physical packing;
- no unit contains an unexpected duplicate barcode;
- no expected barcode is missing; and
- any discrepancy is reported before production.

### 12.3 Production QC

The vendor should validate that:

- filenames begin with the digitization-unit barcode;
- the barcode in each JSON sidecar matches the source unit;
- file roles and naming structures are correct;
- unit boundaries have not caused sequence resets;
- no container barcode was mistakenly used in place of a child digitization barcode;
- no temporary vendor identifier appears as the Library barcode; and
- all assets remain associated with the correct physical unit.

### 12.4 Return QC

Upon return, the Library should confirm:

- all containers and digitization units were returned;
- the physical hierarchy matches the outgoing inventory;
- barcode labels remain present and legible;
- no barcodes were altered or replaced without authorization;
- rehousing or unit changes are documented;
- the digital packages correspond to the expected digitization-unit barcodes; and
- all exceptions and rework items are resolved or tracked.

## 13. Exceptions

Any departure from these recommendations should be documented in the project scope or barcode plan.

Common exceptions may include:

- extremely high-volume slide or aperture-card collections;
- unprocessed collections lacking stable folder structure;
- materials that cannot safely receive or retain an enclosure;
- objects with pre-existing identifiers that cannot be replaced;
- externally owned or borrowed materials;
- items requiring conservation before labeling;
- one physical carrier containing unusually complex intellectual structure; and
- projects where repository constraints require a different digital-object level.

An exception record should state:

- the affected collection or project;
- the standard rule being modified;
- the approved alternative;
- the responsible approver;
- the metadata and packaging implications; and
- the duration of the exception.

## 14. Roles and Responsibilities

| Role | Proposed responsibility |
|---|---|
| Curatorial or collection owner | Confirms intellectual units, titles, restrictions, and access expectations |
| Archival processing or cataloging | Confirms descriptive hierarchy and system-record relationships |
| Collection Management | Approves housing, physical handling, and label placement |
| Conservation | Approves label stock, adhesives, direct application, and fragile-material procedures |
| Digitization program | Defines digitization units, file/package implications, inventory requirements, and vendor instructions |
| Barcode assignment staff | Issues, applies, scans, and records barcodes |
| Metadata or systems staff | Defines registry fields, system mappings, validation rules, and exports |
| Vendor | Reconciles barcodes at intake and preserves identity throughout production |
| Repository or DAMS staff | Confirms barcode use supports ingest and digital-object relationships |

## 15. Required Project-Level Barcode Plan

Every image-digitization project should complete a barcode plan before large-scale preparation begins.

The plan should identify:

1. the physical material types included;
2. the proposed container level;
3. the proposed digitization-unit level;
4. whether any child barcodes are required;
5. where each barcode role will be recorded;
6. who will issue, apply, and quality-check the labels;
7. the approved label stock and placement;
8. any material requiring Conservation review;
9. the expected relationship between barcodes and digital packages;
10. treatment of internal intellectual units;
11. expected shipment and return reconciliation;
12. known exceptions; and
13. the pilot sample used to test the approach.

## 16. Pilot and Approval Process

Before barcoding an entire collection, the project team should test the proposed model on a representative sample.

The pilot should include, where applicable:

- one simple item, such as a bound volume;
- one foldered archival box;
- one photographic group;
- one negative or transparency format;
- one multi-unit microfilm reel;
- one oversized or fragile object; and
- one mixed-format container.

The pilot should test:

- barcode level;
- label placement;
- scan readability;
- inventory structure;
- parent-child relationships;
- vendor intake;
- filename and BagIt generation;
- JSON-sidecar mapping;
- QC reporting; and
- physical return reconciliation.

The barcode plan should be revised after the pilot and approved before full production.

## 17. Implementation Roadmap

### Phase 1: Policy Review

Circulate this draft to:

- Collection Management;
- Conservation;
- Archival  Processing;
- Cataloging;
- Sierra stakeholders;
- ArchivesSpace stakeholders;
- Digital Imaging Services;
- Metadata Services Unit;
- curatorial divisions; and
- Procurement or vendor-management staff.

The review should focus on gaps, unacceptable risks, system constraints, and format-specific exceptions.

### Phase 2: Establish Barcode Governance

Define:

- who controls barcode issuance;
- which barcode ranges are approved;
- whether container and digitization-unit barcodes use the same number pool;
- how duplicate prevention is enforced;
- how replacements are handled;
- how cancelled numbers are retained; and
- who owns the interim registry.

### Phase 3: Define System Mappings

Document how the minimum barcode metadata maps to:

- Sierra;
- ArchivesSpace;
- SPEC during transition;
- the interim barcode registry;
- the vendor inventory spreadsheet;
- the JSON sidecar; and
- the preservation or access repository.

### Phase 4: Approve Physical Application Standards

Conservation and Collection Management should approve:

- label stock;
- adhesives;
- label dimensions;
- print quality;
- placement zones;
- direct-application exceptions;
- barcode-control sheets; and
- rehousing requirements.

### Phase 5: Pilot

Select one or more representative projects and test the full workflow from barcode assignment through digital delivery and physical return.

### Phase 6: Publish Operational Instructions

Convert the approved policy into:

- a concise staff decision tree;
- illustrated placement instructions;
- a barcode-registry data dictionary;
- a pre-shipment QC checklist;
- a vendor intake checklist; and
- project-specific barcode-plan templates.

## 18. Questions Requiring Institutional Decision

The following issues should be resolved during stakeholder review.

1. **System of record:** Where should folder-level and item-level digitization barcodes be permanently recorded when Sierra and ArchivesSpace do not provide a natural item record?
2. **Barcode issuance:** Which team owns the barcode number pool and prevents duplication?
3. **Folder-level policy:** Should folder-level digitization barcoding be the default for all fully digitized archival boxes, or only for vendor projects?
4. **Pre-existing barcodes:** When may an existing container or item barcode be reused as the digitization-unit barcode?
5. **ArchivesSpace representation:** Should folder-level barcode relationships be stored in ArchivesSpace, in an external registry, or both?
6. **Repository object level:** Does the future DAMS or repository expect one object per barcode, and can it support parent-child relationships?
7. **High-volume exceptions:** What is the threshold at which individual barcoding becomes impractical for slides, aperture cards, photographs, or negatives?
8. **Label application:** Which surfaces and label materials are approved by Conservation?
9. **Staffing:** Which staff group will barcode, scan, record, and quality-check materials before shipment?
10. **Backlog:** Will this policy apply only to new vendor projects or also guide retrospective normalization?
11. **Barcode control sheets:** Should lead sheets be mandatory for every digitization unit or only for selected formats?
12. **Vendor discovery:** What should happen when a vendor finds previously unidentified intellectual units or physical subdivisions?
13. **Mixed-format routing:** When should one folder be split into multiple digitization units because its contents require different capture workflows?
14. **Restricted content:** Can one barcode package contain both restricted and unrestricted content, or must those units be separated?
15. **Replacement policy:** How should missing, damaged, or duplicated barcode labels be replaced and documented?

## 19. Proposed Default Rules for Initial Adoption

Pending broader review, the following rules are recommended as an initial institutional baseline:

1. Use one digitization-unit barcode per physical volume, reel, folder, individually enclosed photograph, negative, plate, map, or comparable stable unit.
2. Use a separate container barcode for boxes, trays, portfolios, and other housings that contain multiple digitization units.
3. For manuscript and correspondence collections, barcode the box and each folder selected for digitization; do not barcode every sheet.
4. Use the digitization-unit barcode—not the parent container barcode—for filenames, JSON sidecars, BagIt roots, QC, and ingest.
5. Maintain parent-child relationships in the barcode registry and vendor inventory.
6. Apply labels to housings rather than directly to original materials.
7. Do not create separate barcodes for rectos, versos, pages, frames, access derivatives, or negative/positive digital tracks.
8. Retain one barcode for a multi-unit physical carrier such as a microfilm reel; express internal units through metadata and subdirectories.
9. Require all authoritative barcodes to be assigned and recorded by the Library before shipment.
10. Pilot and document exceptions before large-scale production.

## 20. Recommended Supporting Documents

This policy should ultimately be accompanied by:

- **Barcode Decision Tree:** One-page staff guide for choosing the barcode level.
- **Barcode Placement Guide:** Illustrated format-by-format placement instructions.
- **Barcode Registry Data Dictionary:** Required fields, controlled values, and validation rules.
- **Project Barcode Plan Template:** Project-level decisions, responsibilities, and exceptions.
- **Pre-Shipment Barcode QC Checklist:** 100% validation steps before packing.
- **Vendor Barcode Intake Checklist:** Reconciliation and discrepancy-reporting requirements.
- **Replacement and Exception Procedure:** Rules for damaged, missing, duplicate, or superseded labels.
- **System Mapping Appendix:** Sierra, ArchivesSpace, SPEC, registry, inventory, and repository crosswalks.
