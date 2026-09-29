# WOPR reinforced editions - current print kits

2026-09-29. These files replace the earlier thin-wall kits for new prints. Five editions are included: seven-module-per-side organizer, six-per-side organizer, exposed eight-wheel robot, tucked four-wheel robot, and wide tucked eight-wheel robot. Earlier exports remain historical references. Do not mix old and reinforced mating parts.

## What is reinforced

Structural case walls, roof skins, lid floor and rim, cup walls/floors/dividers, LED retainer thickness, controller tray, motor retaining cheeks and wheel-cover skins are nominally 5 mm. All chassis/base plates are now 10 mm, including the organizers so their previous 6 mm base is not weakened. Robot motor bearing feet are at least 10 mm; their mounting flanges are 10 mm. Additional material joins the feet and flanges where they overlap.

Motor modules use two 5 mm side cheeks, 13 mm posts and cross braces. The removable cap has a 5 mm roof and two 5 mm downward cheeks that positively retain the motor can. These cheeks sit above the wheel housings. The motor assembly bolts into the chassis with a 10 mm flange; it no longer relies on thin printed walls between a wheel and the motor.

The shell has a continuous support ledge, larger base bosses and thicker lid supports. The gray material below the recessed lettering has extra backing so the lettering does not reduce its nominal 5 mm structural section. The white inlays remain decorative material volumes, not 5 mm structural parts. Screw bores, counterbores, wire passages, windows, service openings and assembly clearances are intentional local openings. Nominal wall thickness is not a claim that every fastener edge has 5 mm of material.

## Edition dimensions

All bodies remain 279.4 mm long and nominally 165 mm high. Both organizers and the exposed/four-wheel robot bodies remain 155 mm wide. The wide tucked robot body is now 220 mm wide to accommodate the thicker housings and their attachments.

The exposed eight-wheel chassis projects to 196 mm overall width. Its axles remain 22 mm below the body edge; total nominal height is 218.5 mm. The tucked versions keep axles 18 mm above the body edge, exposing 13.5 mm of tire and giving a nominal total height of 178.5 mm.

Thicker motor bases consume clearance below the case: the tucked robots have approximately 6.5 mm minimum ground clearance beneath the motor flanges; the exposed robot has approximately 7.1 mm beneath its motor feet. These are low indoor chassis. Tire projection below the body is not the same as ground clearance beneath the motor mounts.

The LCD opening remains 50.1 x 39.6 mm with the established mounting-hole pitch. Its bezel is now 5 mm thick; the glass and PCB seat move 3 mm inward. A new LCD fit coupon is included. LED PCB dimensions and module counts stay unchanged. All robots use six modules per side.

Organizer main cups are now 166.4 x 111 x 88 mm. Five-millimeter floors/dividers retain four 38.1 mm shallow cells and four 83 mm deep cells. Print either the shallow-left or shallow-right version. The tower cup is 58.4 x 94.4 x 100 mm, with four 95 mm deep cells. Its smaller footprint leaves stronger material around the roof opening.

## Files to print

Choose one folder under output/reinforced: seven, six, exposed, four or wide. Each contains a self-contained SCAD and printable STL files. shell-two-color.3mf contains the reinforced shell and aligned white inlays as one object; assign gray and white filament explicitly. It is a geometry project, not a printer profile.

For a single-color body, print r-shell.stl; its recessed lettering has the thicker backing. For two colors, use the 3MF or import r-shell and r-white together without independently centering them.

Every edition: one r-shell, one r-frame and two r-retainers. Optional r-white supplies the inlay material. Print r-lcd-coupon before the full body.

Organizers: add ONE r-cup-left or r-cup-right, and one r-cup-tower. Robots: add one r-lid, one r-tray, four r-pods and four r-caps. The tucked four-wheel version also needs two r-hood-front and two r-hood-rear; the wide eight-wheel version needs four of each. The exposed eight-wheel version has integral wheel roofs in its chassis and needs no separate hoods.

Print one motor pod and one cap first, and test the actual motor and wheels. Wheel hub seating depth still needs a physical check. The model retains the nominal 12.5 mm distance from motor center to wheel inner face. Do not force hubs with a hammer.

## Material and orientation

Use PETG or ASA for structural parts, with the same material family for inlays. A starting point is 0.2 mm layers, five or more perimeters, six top/bottom layers and 35% gyroid infill. Use solid local infill at screw bosses, motor feet, flanges and braces. The CAD wall dimensions are real geometry; increasing slicer perimeter count alone does not create this reinforcement.

Print the shell upright. Print tray, retainers and chassis in orientations that give broad supported faces; inspect the tall chassis posts before slicing. Print motor pods with their bottom feet supported. Print motor caps with their roof on the plate and cheeks upward. Print wheel hoods on their flat opening, using support as required. Inspect and clear all motor pockets, counterbores and wheel openings.

Parts need about 280 x 155 mm, 280 x 196 mm or 280 x 220 mm of usable bed area plus brim, according to the edition. Do not scale parts to fit a smaller printer. No slicer toolpath or physical strength test has been completed for this revision.

## Fasteners

- Every edition: eight M3x20 base screws, with heads no taller than 3 mm.
- Robots: four M3x20 main-lid screws; four M3x14 tray screws.
- Robots: eight M3x14 screws mount the four motor pods from below, using the flange counterbores. Heads must fit the 6.5 mm diameter x 3.2 mm deep recess.
- Robots: eight M3x14 screws secure the four motor caps.
- Tucked robots: two M3x14 screws per wheel hood (eight for four wheels, sixteen for eight wheels).
- LED retainers: eight M2x10 screws. LCD: four M2x6 screws; verify actual board thickness and safe tip depth with the coupon.

M3 pilots are 2.5 mm and are intended for plastic-compatible screws. Hand-tighten; the parts do not contain modeled heat-set inserts. Confirm screw lengths on the actual prints before tightening against electronics.

## Robot assembly order

1. Dry-fit one motor in a pod. The gearbox sits on the thick foot, motor can upward. The 5 mm side cheeks guide the body. Check the new cap fits over the can and cheeks. Add a closed-cell foam pad at the nominal 4 mm top gap; trim it to compress lightly and keep it clear of motor terminals.
2. Fit one outward wheel per motor for the four-wheel version, or two wheels per motor for either eight-wheel version. Support the gearbox while pressing hubs on. Leave the top cap off for installation.
3. With the main body removed, raise each motor-and-wheel pod into the chassis FROM BELOW. The broad flange seats below the chassis plate. Fasten it with two M3x14 screws through the underside counterbores. The wheel openings and motor ports are sized for this assembly path.
4. For tucked robots, lower the matching wheel hoods over the wheels before fitting the motor caps. The hood notch faces the motor; secure each hood with two M3x14 screws. Then fit the cap with its two M3x14 screws. The exposed chassis already includes its wheel roofs; install its caps directly after bolting in the pods.
5. Check free rotation through a full turn. Route motor wires through the cap opening, add strain relief and keep wires out of the wheel spaces. Label the motors LF/LR/RF/RR.
6. Pad and strap the USB pack in the center between the printed strap anchors. Fit the controller and drivers on an insulating carrier on the 5 mm tray, using nylon standoffs and straps through its slots. Fit the tray with four M3x14 screws.
7. Fit LED modules and new retainers from inside, then the LCD using the new coupon as the fit reference. Fit the motor-power switch in the end hole. Attach the body with eight M3x20 screws and the main lid with four M3x20 screws.

Organizer assembly: install display and RGB hardware first, fit the 10 mm base, then lower the two reinforced cups onto their support ledges. The cups remain removable for access.

## Electronics and Wi-Fi

The electronics and firmware are unchanged: four Adafruit 3777 motors; Adafruit 3766 wheels; ESP32-DevKitC V4; two Adafruit 3297 DRV8833 drivers; Anker A1259 USB pack (104 x 52.3 x 26 mm). Retain the 5 V, 2.5 A fused supply and 0.5 A current limit per motor, set with four 0.40-ohm sense resistors. Use a 12 mm latching motor-power switch rated at least 3 A at 5 V DC, two 470 uF / 10 V driver capacitors and four 100 nF motor-terminal capacitors. The USB-C sink breakout must be rated 3 A and use 5.1k CC resistors; never select a higher-voltage PD trigger. Use 18-22 AWG power wiring, insulated connectors, two 10 mm battery straps and a nylon-mounted insulating controller carrier no larger than 90 x 65 mm. Reuse Adafruit 3315 LCD and the existing Seeed RGB modules.

The existing sketch in firmware/wopr-robot/wopr-robot.ino creates the WOPR access point and captive controller page. Join WOPR; use its Wi-Fi sign-in prompt, or open http://192.168.4.1. The public setup password remains wopr-car-setup and should be changed locally. Left driver: AIN1/AIN2 to GPIO25/26 (front motor), BIN1/BIN2 to GPIO27/14 (rear). Right driver: AIN1/AIN2 to GPIO32/33 (front), BIN1/BIN2 to GPIO18/19 (rear). Both SLP pins go to GPIO23 with a 10k pulldown; both open-drain FLT pins go to GPIO21 with a 10k pullup to 3.3 V. Common ground; never connect driver outputs together. The unchanged sketch was previously compiled with Espressif Arduino core 3.3.8; this task does not flash hardware.

Test direction, release-to-stop, STOP, Wi-Fi loss, driver fault and the manual switch with wheels raised. Disconnect the battery before attaching PC USB for programming. Start driving tests with RGB/LCD power disconnected. The lighting current must be measured and brightness limited so the complete system stays below 2.5 A continuous. The drive sketch does not regulate lighting.

## Verification and limits

The builder checks watertight connected structural meshes, actual exported wall/base/foot thicknesses, wheel and battery clearance, LCD/LED fit volumes, and motor/hood installation paths. White lettering consists of separate glyph solids by design.

This is a stronger CAD revision, not a certified load or drop rating. Print fit, motor torque under the heavier case, steering scrub, operating temperature, runtime and impact durability remain untested. Plastic TT gears and press-fit wheel hubs remain mechanical limits. Test the fit parts and one assembled motor pod before printing the full set.

## Component references

https://www.adafruit.com/product/3777
https://www.adafruit.com/product/3766
https://www.adafruit.com/product/3297
https://www.adafruit.com/product/3315
https://www.anker.com/nz/products/a1259-built-in-cable-power-bank-10000mah
https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32/esp32-devkitc/user_guide.html
