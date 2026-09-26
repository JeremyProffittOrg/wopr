# W.O.P.R. / draft 02: rear mounts and open pen wells

Open `wopr.scad` in OpenSCAD. Default view is the assembled mockup. Units are millimeters.
Run `python cad/build.py` from the repository root to export meshes, 3MF, views, and PDF.
The builder uses an existing OpenSCAD executable (`OPENSCAD` environment variable overrides its Windows default).
On Windows the builder runs OpenSCAD with `CREATE_NO_WINDOW`; it does not open a foreground console.
Python dependencies already present on the design machine: Pillow, trimesh, numpy, reportlab, PyMuPDF.

## Design

- 279.4 mm (11 in) long, 155 mm wide, 165 mm high. Reference-inspired proportions, not an exact prop scan.
- Eight Seeed 6x10 boards total: four side-by-side on each long side, 480 LEDs total. Centers X=60.1175, 81.3725, 102.6275, 123.8825; Z=101 mm. PCB edge gap is only 0.30 mm, for assembly tolerance.
- Each four-board row is 84.72 mm long. One uninterrupted front window is 83.12 x 13.78 mm; a rear-loading pocket is 85.32 x 18.38 mm. Manufacturer Eagle outline is 20.955 x 17.780 mm per board. The small front rim supports the PCB edges without masking the nominal LED grid.
- Boards load from inside against the front seat at Y=8 mm. A removable retaining frame bears against the PCB backs at Y=9.6 mm. Four rear-facing M2 screws per bank pass through 2.2 mm retainer holes into blind 1.6 mm case pilots. No front screw heads. Check component and solder-pad clearance before tightening.
- One Adafruit #3315 V2 touchscreen over the primary logo; nominal board 65 x 53 x 9.5 mm.
- Rear-loading display pocket 65.6 x 53.6 mm. The front bezel has a 55.6 x 41.6 mm window and hides the PCB and mounting holes. Glass inset is 2 mm; clear rear space is 25.4 mm beyond the nominal hardware back at depth 11.5 mm. Bay ends at depth 36.9 mm and is open behind.
- V2 mounting hole pitch 59.690 x 47.498 mm, rotated landscape. Drive M2 screws through the PCB from behind into four blind 1.8 mm pilots. The front 1 mm remains closed. Do not use a screw that reaches through the face. Check real PCB-to-glass height before tightening; the draft seat is at Y=4 mm.
- Shell nominal 3 mm wall; white text 0.8 mm deep and flush with the gray face. No paint or stickers needed for text.
- Main pen well: 163 x 105 mm clear opening, floor at Z=43, stepped rim at Z=128/137 (85-94 mm depth). Tower pen well: 63 x 95 mm, floor at Z=68, rim at Z=165 (97 mm nominal depth). Both have 3 mm walls and floors. Each cup drops into a 0.30 mm per-side clearance and rests on internal supports. The tower cup starts at Y=43, beyond the 36.9 mm display bay.
- Cups lift out for rear access and isolate pens from the electronics. The main cup is printed in two halves and glued into one removable cup. Decorative doors remain engraved. Bottom halves also provide service access.

## Print and assembly

1. Print the gray display fit coupon first. Test the actual V2 board, holes, connectors and inset. This is a dimensional draft, not a completed physical fit test.
2. Open `right-shell-two-color.3mf` as one object with two material parts. Assign gray and white explicitly in the slicer. Confirm both text lines on both long sides. A plain STL cannot store material assignments.
3. The two right-shell STLs are an alternative: import together as parts of ONE object and preserve their common origin. Do not auto-arrange the white file or print the loose letters separately.
4. Print the two shell halves, two base halves, three cup pieces, and TWO copies of `led-retainer.stl`. All files are oriented for the bed; retainers lie flat. Each structural part fits within 165 x 155 mm. A bed at least 180 x 180 mm allows a brim. Use supports for case ledges and window bridges; the open top and bottom permit removal. Start with 0.2 mm layers, a 0.4 mm nozzle and 3 perimeters; adjust to the printer and material.
5. Print SIX copies of `splice.stl`. Dry-fit shell halves at X=140. Glue two strips across the inside shell seam below the cup floor; two across the upper base seam; two under the main cup floor seam. Keep strips away from support pads and screws. Glue only the cup halves to each other; do not glue cups to the shell. Dry-fit the completed cup before final assembly.
6. Leave cups and base off. Load the eight LED boards from behind the two long windows. Fit the rear retaining frames, using eight M2 self-tapping screws total. With a 2.4 mm retainer and about 3.1 mm blind pilot depth, about 5 mm screw length is a starting point; verify actual engagement first. Leave the 0.30 mm board-edge gaps for splicing wires. Do not clamp a component or solder pad.
7. Load the TFT from behind its bezel. Fit four M2 screws from the PCB rear into the blind pilots. Measure the actual PCB and any washer/spacer stack before choosing screw length; the plastic pilot has only 3 mm usable depth. Do not pierce the front face. Check the glass inset and full 25.4 mm rear connector space.
8. Check wiring, then lower the main and tower cups into their top openings. Attach the base with eight M3 self-tapping screws (2.5 mm shell pilots, 3.3 mm base clearance). About 10 mm screw length is a starting point. Do not force a tight pilot. These cups are dry pen holders, not liquid containers.

## Scope and limits

Electronics colors and screen content appear only in the mockup. All printed structural parts are gray except the white text. Four adjacent boards form each continuous light bank; PCB margins still create small dark seams. The model does not contain firmware, a controller mount, a power supply design, or an electrical/thermal validation. No physical print, slicer toolpath test, or component fit test has been performed. The builder checks rear PCB insertion paths with cups and retainers removed, vertical cup removal, open pen volumes, the display rear clearance and closed fronts over the TFT pilots using SCAD interference probes.

## Sources (accessed 2026-09-26)

- https://www.seeedstudio.com/6x10-RGB-MATRIX-for-XIAO-p-5771.html
- https://wiki.seeedstudio.com/rgb_matrix_for_xiao/
- https://files.seeedstudio.com/wiki/xiao-rgb-matrix/EAGLE_XIAO_MATRIX.zip
- https://www.adafruit.com/product/3315
- https://github.com/adafruit/Adafruit-2.4-TFT-FeatherWing-PCB
- https://www.miniatua.com/work/wopr/ (visual reference only; no third-party mesh reused)
