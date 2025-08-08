---
layout: default
title: Best Practices for Reflective Materials
parent: Technical Documents
permalink: /tech_documents/bestpractice_reflective/
toc: true
---

## Bound Volumes (Rare, Special Collections, and General Collections)

The goal is full cover-to-cover digitization while ensuring material safety and maintaining focus throughout the text block.

#### Glass Usage
* For **rare books and special collections**, glass may be "floated" to minimize pressure on fragile bound materials, and its use requires **prior approval** due to potential damage risks, especially for pigmented or gold leaf materials.
* Glass helps flatten pages and allows them to meet the glass consistently.
* Secondary card and/or foam supports can be used with glass to reduce pressure on fragile pages or to kick up the glass for greater downward pressure on springy gutters.
* For general collections, books can be imaged in contact with glass to flatten, but the binding **must not be stressed**.

#### Material Assessment and Support
* Thoroughly assess the **fragility of paper and stability of the binding**.
* Check for **gutter curvature, paper sheen, fold-outs, and prints/photos** that might influence lighting or PPI.
* **Foam and cardstock additions** are strategically used to help the text block lie as plumb as possible and to "kick pages out" to expose more text in the gutter. Be cautious not to use too much foam.

#### Capture Settings and Focus
* The typical aperture for books rests between **f/8.5 to f/11** to provide more focus depth and productivity. This may involve a sacrifice of PPI to boost depth of field for easier focusing and higher throughput.
* Focus aims for a **"zone of acceptable focus"** rather than absolute sharpness across the entire page, prioritizing the "meat of the text and/or image area," especially when gutter curvature is an issue.
* Focus is checked approximately every **10-20 captures** (or more), adjusting camera and target height as needed. This allows for reviewing blocks of pages (e.g., 20 pages) to catch skipped or duplicated captures efficiently.
* For books, a **Lens Cast Correction (LCC)** is typically needed **only once per book/session**, provided lighting and aperture remain constant.

#### Content Inclusion
* Full cover-to-cover digitization for bound volumes includes **covers, endpapers, and all pages (even blank ones)**, as well as the spine.
* Exceptions for not digitizing covers/endpapers may occur for General Collections if a **library binding** was added or similar alterations were made. Decisions not to shoot blank pages may be made in cases of interleaving tissue paper or large blank sections, often reviewed for curatorial preference.
* **Fold-outs** are imaged in sequence, matching the resolution/PPI to their bound counterpart whenever possible, and both recto and verso contents are imaged in their folded state.

#### Handling
* **Gloves are generally not recommended** for digitizing paper or similar materials as they can increase the possibility of damage.
* Material temperature and humidity should be maintained consistent with collection storage.

#### Moiré Mitigation
* Finding a balance between **moire mitigation and desired PPI** is crucial, potentially requiring test shots at varying heights. The Moire tool in Capture One (often amount 60-90, pattern 8) can be used, but values can deviate if not detrimental to image quality.

---

## Manuscript Materials (Loose Unbound & Flat)

The process emphasizes accurate capture of each page while maintaining the original order and orientation.

#### Material Preparation
* A **clean gray, light gray, or off-white background paper** is chosen based on the material, especially for translucent items.
* Use an **air compressor or hand rocket** to remove dust from the material.

#### Capture Protocol
* All objects are photographed **recto/verso** (front and back), including blank pages.
* The **order of materials** in their housing (box, folder) **must be retained at all times**.
* The **orientation** of each image should remain the same as the face page of the document, even if text appears upside down or vertical.

#### PPI Aims
* For **manuscripts and other rare and special materials**, the aim is typically **400-600ppi (FADGI 4-star)**, with 600ppi whenever possible.
* For **general collections or modern textual materials**, an **8-bit Primary file** may be used instead of the standard 16-bit. For modern textual records, there are **no FADGI star levels**; images either meet specifications or they don't.

#### Workstation Setup
* The camera height is determined by the size of the longest item, aiming for the **highest possible PPI (typically 550-600ppi)** unless otherwise specified.
* The **target is taped to the copy stand** to prevent movement.

#### Focus Checks
* Focus and exposure are re-checked after **50-75 shots**.
* It is crucial to verify that the number of images in the Capture One session matches the number of captures on the work order to avoid errors.

---

### Photographic Materials (Prints)

These require meticulous handling and specific techniques to manage reflections and achieve precise detail capture.

#### Handling Precautions
* **Nitrile gloves are always recommended** when handling photographic prints to prevent fingerprints and damage.
* **Dust is a significant issue**, especially in shadow areas and on target patches; use an air compressor or hand rocket and give extra attention to dusting darker tones.

#### Background and Setup
* A **black velvet shoot-through foam core** may be used to mitigate reflections and achieve richer shadow details, especially for photographic prints.
* Lights should not be so high that they impede even illumination; the full extent of the lights should be visible from the print's level.

#### Reflection Mitigation
* For issues like **curved edges and hard, pronounced folds**, the **digital back can be rotated** to mitigate highlight problems.
* **Peeling corners** can sometimes be coaxed flat using a gloved finger, bone folder, or piece of paper to mitigate hot spots.
* **Hard folds that catch highlights** may require special handling, possibly a separate capture with the back rotated vertically and a new LCC.

#### PPI Aims
* Specific "real world PPI buckets" are used based on print size, aiming to meet or exceed FADGI 3 or 4-star performance.
* **400ppi** for originals larger than 16x20” (FADGI 3-star).
* **600ppi** for originals larger than 11x14” up to 16x20” (FADGI 4-star).
* **800ppi** is the **current standard for 8x10” photographic print collections**, and for originals from 5x7” to 11x14”.
* **1000ppi** for originals smaller than 5x7”.

#### Moiré Mitigation
* If moiré patterns are present, the **material can be rotated in-camera** to mitigate the effect. This may necessitate reducing the PPI to create adequate rotational space around the print. Higher resolution digital backs limit moiré, but it can still occur.

---

### Oversized Materials (Maps, Posters, and Artworks Requiring Stitching)

These often require multi-capture approaches to achieve sufficient resolution and manage physical dimensions.

#### Stitching Requirement
* **Stitching may be required** for oversized items if they cannot meet the resolution aim as a single capture. Sections are digitally composited and reassembled to represent the material as a whole without distortion or misrepresentation.
* **Component images** that make up the final stitched file are saved as preservation files (U files) but are **suppressed** in the Metadata Management System (MMS) for public display; the final stitched image becomes the production preservation file.
* An overlap of **around 20% is ideal** for images requiring stitching when no canvas break is present.
* Stitching can be done using **Photoshop Photomerge** (generally using the 'collage' method) or **manual methods**, the latter sometimes being less time-consuming for maps with worn seams.
* For stitched images, **only one color target** should remain in the final composite image.

#### PPI Determination
* PPI is determined by the item's fine details, overall size, and the number of captures required for a composite. A single capture is preferable if details are legible.
* For **maps, posters, and other materials**, the aim is generally **400ppi or 600ppi**, adjusting based on fine details and compositing needs.
* **Newspapers** generally target **400ppi** (FADGI 3-star).

#### Handling and Setup
* Many maps are printed on thin paper and require an **off-white mat board underneath**; only the image area needs to be covered.
* For **encapsulated items (e.g., in Mylar)**, special care is needed to mitigate reflections. This can involve using **black shoot-through cards** to eliminate reflections from the camera and environment, covering the TTI column with black paper, or using black flags on light stands. When using a foot pedal near encapsulated items, tripping the shutter from the keyboard can prevent reflections from clothing/skin.
* When using glass for encapsulated items, a **slip of Mylar over the color target** is recommended.

#### Lighting
* Lights are typically between **64” and 80” high** (floor to top of pin) and pointed **20 degrees down**.
* Some coated maps may require lights to be raised to avoid glare. For encapsulated items, lights may need to be lowered all the way and pointed at each other from table corners to lessen edge reflections.

#### Focus Challenges
* Maps often fill the frame, which demands high performance from the lens and an extremely level copy stand. Balancing sharpness between corners and the center can be challenging. It may be helpful to check **nine points of focus**.

#### Moiré Mitigation
* Moiré is very common with maps due to fine parallel ink lines and halftone printing. While higher resolution backs limit it, it still occurs.
* The moiré tool in Capture One can be used (e.g., amount 45, pattern 8), and may need to be boosted to 100 in certain areas. It's crucial to **avoid color smearing** by removing moiré adjustment from map edges and canvas seams.

---

### Three-Dimensional Items
3D items are explicitly **not included in FADGI guidelines**, meaning imaging practices for them are developed in-house based on best judgment and specific item needs.

#### Lighting and Setup
* The setup is highly variable due to wide variations in item shape, size, and material. A **safe off-set area** for the item and an **adequate background paper sweep** are essential.
* Focus on how light might fall across the item to **best describe its volume and surface detail**. A primary light source entering from the left often works well for Western text.
* A **two-light setup** is typically used, with lights adjusted for height, distance, and angle to ensure even illumination.
* Explore using a **key light** (dominant), **fill light** (to diminish shadows, possibly with a fill card), **kickers/accent lights** (behind and to sides for highlights and separation, especially for dark items), and optional **background lights** or a **boom light**.
* **Beware of lens flare**; flagging off the lens may be necessary.
* Flagging off the background paper can create a **gradated effect** that visually isolates the item and increases perceived dimensionality.
* Alternative lighting modifiers beyond standard softboxes, such as reflectors, beauty dishes, diffusion paper, silks, and scrims, may be used.

#### LCC Application
* A unique point for 3D items is that there is **no need to make or use an LCC** (Lens Cast Correction).

#### Camera and Focus
* The camera's angle and height are critical for defining the item in space and avoiding distortion. Perform a **through-the-lens handheld assessment** to quickly determine orientation and angle.
* Focus aims to utilize the **plane of focus** which travels outward parallel to the lens at its angle, allowing it to match the item's shape. Pulling back camera distance can increase depth of field.
* **Focus stacking** has been tested and may be employed on a case-by-case basis depending on the item's depth and time constraints.

#### Representational Views
* A successful 3D capture describes the item's purpose/story, physical attributes, presence in space, and center of gravity.
* Often, **multiple views** are needed (e.g., ¾ front and ¾ back, or front/back, side/side, top/bottom) to adequately describe the item.
* Be aware of **visual tangent points** which can be distracting and flatten perceived volume; aim to create separation of object elements.

#### Post-processing
* Final capture may benefit from an **overall sharpening bump** and **local adjustments for shadow/highlight recovery**.
* **ISO is kept at 200 or under** for in-situ items.
* **PPI is unspecified**, based on the item's finest details that need to be resolved and balancing depth-of-field in a single capture.

In essence, while flat materials prioritize a perfectly "flat" digital reproduction achieved through precise alignment and exposure, imaging 3D objects is more akin to a portrait artist capturing the essence and form of their subject. The challenges shift from mitigating surface irregularities to orchestrating light and camera angles to define volume, texture, and spatial relationships, where the "truth" of the image lies in its comprehensive portrayal from multiple perspectives rather than a single, perfectly planar shot.

