# Best Practices for Digital Capture of Transmissive Materials

### Preparation and Handling

- Film should typically be photographed with the **emulsion side down**. The emulsion side is the more matte surface with a raised texture, while the base side is shiny. Any text on the film should read correctly when viewed with the emulsion side down.

- Slides and film should be resleeved in the same order they were shot, mainatining the emulsion side down orientation.

- As **dust** is a significant challenge during the digitization of transmissive media, working areas should be cleaned regularly and kept as dust-free as possible.

### Equipment Setup and Operation

#### Equipment Setup
- Lighting equipment should be powered on for at least 5 minutes before beginning a session.

- **Camera alignment** should be verified with a laser level at the beginning of any new project and/or whenever any adjustments are made, e.g. changing a lens.

#### Capture Settings
- **ISO and Aperture**: Maintain a consistent ISO of 50 and an aperture of F9 for transmissive captures.

- **Base Characteristics**:  Set camera Base Characteristics to "Photography" Mode. Initially set the **Curve** to "Linear Scientific", then switch to "Linear Response" after **LCC creation**.

-  **Sharpening and Noise Reduction**: Apply consistent **sharpening settings** (Amount=100, Radius=1, Threshold=0, Halo=0) and **noise reduction** (Luminance=0, Details=50, Color=40, Single Pixel=0).

#### Capture Workflow
- **Focusing**: Start by creating a capture of an IT8 target or a negative for initial focus. Use Live View at 100% with single incremental movements to achieve sharp focus and visible film grain. Measure PPI with the Capture Resolution Ruler to confirm resolution


- **LCC (Lens Cast Correction)**: Capture an LCC Raw File directly off the Photon light source (not Plexiglass) with the film removed, exposing for mid-gray. Alternatively, apply a pre-set LCC based on the film format.

- **White Balance**: With film removed, capture a mid-gray image and white balance off the Photon light source in the center of the frame

- **Base Exposure**: For **color positives**, set the exposure (film removed) until the Photon reading is at 243 (without exceeding in any RGB channel), with underexposure being preferred over overexposure. For **B&W negatives**, set exposure off the negative's unexposed film base to 235 (without exceeding), as Gray Gamma 2.2 displays a single grayscale value. Fine-tune with minimal "Exposure" tool adjustment.

- **Levels and HDR Adjustments**: Apply a custom Levels preset for the Atom system and specific film stocks. Adjust **Shadow** detail under the HDR (High Dynamic Range) Tool as needed. For **B&W negatives**, HDR adjustments are "reversed" (Shadow adjusts highlights, Highlight adjusts shadows). Be mindful not to overdo shadow recovery to avoid flattening the image. Kodachrome films may require more shadow recovery (15-25)

- **Next Capture Adjustments**: Set "Next Capture Adjustments" to "Copy From Last" to maintain consistency across captures

- **Batch Capture**: Once settings are finalized, capture all slides/negatives within the work order/production. Tag vertical captures (e.g., green for slides, green/yellow for negatives) for easy bulk rotation later.

#### Capture Processing and Output
- **File Formats and Bit Depth**: Create both Primary Files (U Files) and Service Files (S Files). U Files should be lossless TIFF (uncompressed) at 16-bit depth for maximum detail and long-term preservation. S Files are typically 8-bit.

- **Color Space**: U Files for **color positives** use Adobe RGB (1998). U Files for **B&W negatives**  use Gray Gamma 2.2. S Files for both generally use sRGB for optimal web display.

- **Cropping**: For 35mm slides, U and S files should have the same crop size (4300 x 6100 pixels). For B&W 35mm negatives, S files are approx. 4230 x 6330 pixels, and U files are approx. 5050 x 8500 pixels. U files should include the full film border, and for roll films, a small portion of adjacent frames. S files are generally cropped outside the image area, showing some of the dark film base or slide mount.

- **Rotation**: Rotate all vertical captures in bulk during post-processing

### Key Considerations and Challenges
 - **Dynamic Range**: Recognize that transparency films can have a very high d-max (approaching 4.0), which challenges even the best imaging sensors. Phase One digital backs are noted for their 15-stop dynamic range. Highlight/Shadow tolerance aims should be ideally within 245/10 (+/- 5) RGB values

-  **Film Type Specifics**: Be aware that Kodachrome films require specific IT-8 targets or professionally produced ICC profiles for correct digitization, as standard Ektachrome targets are insufficient. For B&W and color negatives, the tone scale is non-linear, and they may appear flatter than positive prints

- **Color Casts and Degradation**: The aim for color transparencies is to create a digital surrogate representing their current condition as viewed on a light table, not to "color correct" casts resulting from poor development or degradation over time. Dust processed into the emulsion should be captured

- **Moiré and Motion Blur**: If moiré patterns or color noise are present, rotate the material to mitigate the effect, potentially requiring a reduction in PPI to create adequate rotational space. Be wary of motion blur, especially with shutter speeds slower than 1/20s

- **Negative Inversion**: The current practice for B&W negatives is to capture them in their negative state and then invert them to create a positive, with minimal adjustments (e.g., straight invert, 100% desaturation, slight midtone pull in Curves)
The decision to save the positive inverted version as the Primary File (U) is currently under review.