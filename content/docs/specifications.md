---
title: 'Standards for Digital Images'
description: 'Broad policies and standards utilized by Digital Imaging Services photographers. Written for non-technical users.'
toc_hide: false
draft: false
weight: 20 
---

{{% pageinfo color="info" %}}
This repository is currently under construction. The document you're reading may be edited, moved, or deleted entirely. 
{{% /pageinfo %}}

Broad policies and standards utilized by Digital Imaging Services photographers. 

 ---

## Reflective Material

See [Best Practices for Reflective Material]( {{< relref "tech_documents/bestpractice_reflective" >}} ) for more detailed information by material type.

### Preservation and Service Files

 Two distinct files are created for every image captured, a **Preservation File** and a **Service File**. The Preservation File is spec'd for long-term retention and use, whereas the Service File is spec'd for ease of access and digital display. 

| File Type | Format | Bit-Depth | Color Space | Composition |
| --- | --- | --- | --- | --- |
| Preservation (u) | TIFF | 16-bit | Adobe RGB (1998) | crop includes object-level target |
| Service </br>(s) | TIFF | 8-bit | sRGB | cropped for consistent viewing experience, no object-level target |

### PPI Range by Material Type

| Material Type                                                        | PPI          |
| -------------------------------------------------------------------- | ------------ |
| **Bound Volumes:** Special Collections, Rare Books, General Collections               | 400-600ppi   |
| **Documents (Unbound):** Manuscripts, Special Materials, General Collections  | 400-600ppi   |
| **Prints and Photographs**          | 400-1000ppi  |
| **Oversize Items:** Maps, Posters, Other Materials    | 300-600ppi   |
| **Paintings and Other Two-Dimensional Art**         | 300-600ppi   |

### General Practices for Reflective Material
- **Color accuracy** should be measured against an object-level target, not the original object.
- Objects should be photographed **recto/verso** (front and back), including blank pages.
- Images should be **oriented correctly**, generally in a top-down readable fashion based on the first page or capture of the object. Subsequent pages should maintain this orientation.
- If a **backing sheet** is used, it must extend beyond the edge of the page.
- For oversized materials, **PPI** should be determined by the item's fine details, overall size, and the amount of captures that may be required to create a composite. A single capture is preferable in most cases provided that the details are legible.

 ---

## Transmissive Material

See [Best Practices for Transmissive Materials]({{< relref "tech_documents/bestpractice_transmissive" >}}) for more detailed information.

### Preservation and Service Files

 Two distinct files are created for every image captured, a **Preservation File** and a **Service File**. The Preservation File is spec'd for long-term retention and use, whereas the Service File is spec'd for ease of access and digital display. 

#### Black and White 
| File Type | Format | Bit-Depth | Color Space | Composition |
| --- | --- | --- | --- | --- |
| Preservation (u) | TIFF | 16-bit | Grey Gamma 2.2 | crop includes full film border |
| Service (s) | TIFF | 8-bit | Grey Gamma 2.2 | crop includes edge of frame |

#### Color 
| File Type | Format | Bit-Depth | Color Space | Composition |
| --- | --- | --- | --- | --- |
| Preservation (u) | TIFF | 16-bit | Adobe RGB (1998) | crop includes full film border |
| Service (s) | TIFF | 8-bit | sRGB | crop includes edge of frame |

### PPI Range by Material Dimensions
| Material Type | PPI | 
| --- | --- |
| Transmissive Media up to 4x5 | 1750-4300ppi|
| Transmissive Media larger than 4x5| 890-1255ppi |

### General Practices for Transmissive Material
- Film should typically be photographed with the **emulsion side down**. The emulsion side is the more matte surface with a raised texture, while the base side is shiny. Any text on the film should read correctly when viewed with the emulsion side down.





