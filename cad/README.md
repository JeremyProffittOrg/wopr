# W.O.P.R. / draft 05: one-piece shell, base and main cup

Open `wopr.scad` in OpenSCAD. Default view is the assembled mockup. Units are millimeters.
Run `python cad/build.py` from the repository root to export meshes, 3MF, views, and PDF.
The builder uses an existing OpenSCAD executable (`OPENSCAD` environment variable overrides its Windows default).
On Windows the builder requests `CREATE_NO_WINDOW`, but that flag did not establish that the entire launch chain was hidden. Agents must obey the repository console-visibility rule before any build.
Python dependencies already present on the design machine: Pillow, trimesh, numpy, reportlab, PyMuPDF.

## Design

- 279.4 mm (11 in) long, 155 mm wide, 165 mm high. Reference-inspired proportions, not an exact prop scan.
- Fourteen Seeed 6x10 boards total: seven side-by-side on each long side, 840 LEDs total. Centers X=31.235 + i*21.255 for i=0 through 6; Z=101 mm. PCB edge gap is only 0.30 mm, for assembly tolerance.
- Each seven-board row is 148.485 mm long. One uninterrupted front window is 146.885 x 13.78 mm; a rear-loading pocket is 149.085 x 18.38 mm. Manufacturer Eagle outline is 20.955 x 17.780 mm per board. The small front rim supports the PCB edges without masking the nominal LED grid.
- Boards load from inside against the front seat at Y=8 mm. A removable retaining frame bears against the PCB backs at Y=9.6 mm. Four rear-facing M2 screws per bank pass through 2.2 mm retainer holes into blind 1.6 mm case pilots. No front screw heads. Check component and solder-pad clearance before tightening.
- One Adafruit #3315 V2 touchscreen over the primary logo; nominal board 65 x 53 x 9.5 mm.
- Rear-loading display pocket 65.6 x 53.6 mm. The front bezel has a 55.6 x 41.6 mm window and hides the PCB and mounting holes. Glass inset is 2 mm; clear rear space is 25.4 mm beyond the nominal hardware back at depth 11.5 mm. Bay ends at depth 36.9 mm and is open behind.
- V2 mounting hole pitch 59.690 x 47.498 mm, rotated landscape. Drive M2 screws through the PCB from behind into four blind 1.8 mm pilots. The front 1 mm remains closed. Do not use a screw that reaches through the face. Check real PCB-to-glass height before tightening; the draft seat is at Y=4 mm.
- Shell nominal 3 mm wall; white text 0.8 mm deep and flush with the gray face. No paint or stickers needed for text.
- Main pen well: 163 x 105 mm clear opening, floor at Z=43, stepped rim at Z=128/137 (85-94 mm depth). Tower pen well: 63 x 95 mm, floor at Z=68, rim at Z=165 (97 mm nominal depth). Both have 3 mm walls and floors. Each cup drops into a 0.30 mm per-side clearance and rests on internal supports. The tower cup starts at Y=43, beyond the 36.9 mm display bay.
- Cups lift out for rear access and isolate pens from the electronics. The main cup is printed as one piece. The tower cup stays separate and removable. The shell and base each print as one continuous part; there is no center seam or glue joint. Decorative doors remain engraved.

## Print and assembly

Open `output/model/wopr-parts.3mf` by itself in Bambu Studio. It contains the complete
parts set, with the gray/white shell grouped and the other parts separated in the workspace.
Do not pass `.3mf` and `.stl` files together in one GUI import batch: Bambu rejects mixed
suffixes. The project carries geometry only, not printer presets or G-code. Select the
correct printer and arrange parts onto suitable plates before slicing. Two retainers are included.
If Bambu displays "load geometry data only", confirm that option. This preserves the
printer settings already selected in Bambu Studio.

1. Print the gray display fit coupon first. Test the actual V2 board, holes, connectors and inset. This is a dimensional draft, not a completed physical fit test.
2. Open `shell-two-color.3mf` as one object with two material parts. Assign gray and white explicitly in the slicer. Confirm both text lines on both long sides. A plain STL cannot store material assignments.
3. `gray-shell.stl` plus `white-text.stl` are the alternative: import together as parts of ONE object and preserve their common origin. Do not auto-arrange the white file or print the loose letters separately.
4. Print `gray-shell`, `base`, `cup-main`, `cup-tower`, and TWO copies of `led-retainer`. Each is a single structural solid. The retainer is 160.485 x 23.78 x 2.4 mm. The shell and base require a 279.4 x 155 mm footprint; use at least 280 x 155 mm of usable bed area plus brim clearance. A standard 256 x 256 mm Bambu plate cannot hold this full-size shell. Do not scale the model to fit, since the electronics would no longer fit. Use supports for case ledges and window bridges; the open top and bottom permit removal. Start with 0.2 mm layers, a 0.4 mm nozzle and 3 perimeters.
5. No splice strips or glue joints are needed. Dry-fit both removable cups and the one-piece base before installing electronics. Keep the base and cups separate from the shell for service access.
6. Leave cups and base off. Load the fourteen LED boards from behind the two long windows. Fit the rear retaining frames, using eight M2 self-tapping screws total. With a 2.4 mm retainer and about 3.1 mm blind pilot depth, about 5 mm screw length is a starting point; verify actual engagement first. Leave the 0.30 mm board-edge gaps for splicing wires. Do not clamp a component or solder pad.
7. Load the TFT from behind its bezel. Fit four M2 screws from the PCB rear into the blind pilots. Measure the actual PCB and any washer/spacer stack before choosing screw length; the plastic pilot has only 3 mm usable depth. Do not pierce the front face. Check the glass inset and full 25.4 mm rear connector space.
8. Check wiring, then lower the main and tower cups into their top openings. Attach the base with eight M3 self-tapping screws (2.5 mm shell pilots, 3.3 mm base clearance). About 10 mm screw length is a starting point. Do not force a tight pilot. These cups are dry pen holders, not liquid containers.

## Scope and limits

All printed structural parts are gray except the white text. Seven adjacent boards form each continuous light bank; PCB margins still create small dark seams. The model does not contain firmware, a controller mount, a power supply design, or an electrical/thermal validation. The builder checks watertight meshes, single connected structural solids, overall dimensions and mechanical clearances. Physical printing, hardware fit and slicer toolpaths remain untested.

## Sources (accessed 2026-09-26)

- https://www.seeedstudio.com/6x10-RGB-MATRIX-for-XIAO-p-5771.html
- https://wiki.seeedstudio.com/rgb_matrix_for_xiao/
- https://files.seeedstudio.com/wiki/xiao-rgb-matrix/EAGLE_XIAO_MATRIX.zip
- https://www.adafruit.com/product/3315
- https://github.com/adafruit/Adafruit-2.4-TFT-FeatherWing-PCB
- https://www.miniatua.com/work/wopr/ (visual reference only; no third-party mesh reused)
