# W.O.P.R. / first draft

Open `wopr.scad` in OpenSCAD. Default view is the assembled mockup. Units are millimeters.
Run `python cad/build.py` from the repository root to export meshes, 3MF, views, and PDF.
The builder uses an existing OpenSCAD executable (`OPENSCAD` environment variable overrides its Windows default).
Python dependencies already present on the design machine: Pillow, trimesh, numpy, reportlab, PyMuPDF.

## Design

- 279.4 mm (11 in) long, 155 mm wide, 165 mm high. Reference-inspired proportions, not an exact prop scan.
- Eight Seeed 6x10 boards total: four on each long side, 480 LEDs total. Board centers at X=37, 79, 121 and 163, Z=101 mm.
- Seeed pockets 21.6 x 18.4 mm. Manufacturer Eagle outline is 20.955 x 17.780 mm, larger than the rounded product-title width of 17.5 mm.
- One Adafruit #3315 V2 touchscreen over the primary logo; nominal board 65 x 53 x 9.5 mm.
- Display pocket 65.6 x 53.6 mm, front inset 2 mm, clear rear space 25.4 mm beyond the nominal hardware back at depth 11.5 mm. Bay ends at depth 36.9 mm, with an open rear for access and wiring.
- V2 mounting hole pitch 59.690 x 47.498 mm, rotated landscape; 2.7 mm clearance holes in four ears. Check real PCB-to-glass height before tightening. Use M2.5 screws, nuts and suitable insulating spacers.
- Shell nominal 3 mm wall; white text 0.8 mm deep and flush with the gray face. No paint or stickers needed for text.
- Decorative doors are engraved, not opening doors. Bottom halves provide service access. Board supports use a small rim; secure Seeed boards with removable neutral-cure electronics-safe silicone on the PCB edge. Do not glue LEDs or solder pads.

## Print and assembly

1. Print the gray display fit coupon first. Test the actual V2 board, holes, connectors and inset. This is a dimensional draft, not a completed physical fit test.
2. Open `right-shell-two-color.3mf` as one object with two material parts. Assign gray and white explicitly in the slicer. Confirm both text lines on both long sides. A plain STL cannot store material assignments.
3. The two right-shell STLs are an alternative: import together as parts of ONE object and preserve their common origin. Do not auto-arrange the white file or print the loose letters separately.
4. Print left shell, right shell, and two base halves. Each structural part fits within a 165 x 155 mm footprint when exported. A bed at least 180 x 180 mm allows a brim. Shells stand upright as supplied; use internal supports for roofs and window bridges. The open bottoms allow support removal. Start with 0.2 mm layers, 0.4 mm nozzle, 3 perimeters; adjust to the printer and material.
5. Print four copies of `splice.stl`. Dry-fit shell halves at X=140. Glue two strips across the inside wall seam below the light band; glue two across the upper surface of the base seam. No adhesive near electronics. The first-draft seam is a glued butt joint.
6. Install components through the bottom. Check the 25.4 mm rear envelope with the actual connector stack. Attach the base with eight M3 self-tapping screws (2.5 mm shell pilots, 3.3 mm base clearance). Select screw length after checking engagement; about 10 mm is a starting point. Do not force a tight pilot.

## Scope and limits

Electronics colors and screen content appear only in the mockup. All printed structural parts are gray except the white text. The eight tiny Seeed boards form four separate clusters per side, rather than a continuous LED surface. The model does not contain firmware, a controller mount, a power supply design, or an electrical/thermal validation. No physical print, slicer toolpath test, or component fit test has been performed.

## Sources (accessed 2026-09-26)

- https://www.seeedstudio.com/6x10-RGB-MATRIX-for-XIAO-p-5771.html
- https://wiki.seeedstudio.com/rgb_matrix_for_xiao/
- https://files.seeedstudio.com/wiki/xiao-rgb-matrix/EAGLE_XIAO_MATRIX.zip
- https://www.adafruit.com/product/3315
- https://github.com/adafruit/Adafruit-2.4-TFT-FeatherWing-PCB
- https://www.miniatua.com/work/wopr/ (visual reference only; no third-party mesh reused)
