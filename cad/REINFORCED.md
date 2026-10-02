# WOPR reinforced editions - current print kits

2026-10-02. BOTTOM-LOADING / LARGER WHEEL CLEARANCE / SUPPORT REDUCTION REVISION. These files replace the earlier thin-wall kits for new prints. Five editions are included: seven-module-per-side organizer, six-per-side organizer, wide low-axle eight-wheel robot, tucked four-wheel robot, and wide tucked eight-wheel robot. Earlier exports remain historical references. Do not mix old and reinforced mating parts.

## What is reinforced

Structural case walls, roof skins, lid floor and rim, cup walls/floors/dividers, LED retainer thickness, controller tray, motor retaining cheeks and wheel-cover skins are nominally 5 mm. All chassis/base plates are now 10 mm, including the organizers so their previous 6 mm base is not weakened. Robot motor top stops are 10 mm and are part of the chassis. There are no detachable motor-mount flanges or separate wheel-well covers.

Every robot chassis is one continuous printed solid: the main base, all four motor mounts and every wheel well are fused together. Motors now rise through the bottom opening and stop against an integral 10 mm ceiling. The screw version uses four removable flat 5 mm bottom retaining plates. The zip version uses two horizontal ties around each motor and a third tie beneath its gearbox and over the top stop. It has no retaining plate. The horizontal ties are now at 44 and 54 mm above the axle. Sloped shoulders support the wider upper tie pillars. Side tunnels retain 5 mm walls and 5.4 mm between levels. The third tie runs through two narrow reliefs beside the motor and through the top stop; it stays clear of the shafts and tire envelope.

The wheel wells include 6.5 mm of axial fitting travel. Raise bare motors from below, then raise each wheel through the underside opening at the service offset and slide it onto its shaft. On the eight-wheel models, the two inner tires at each end share a continuous arched chamber. This provides fitting room without a thin divider. Shaft slots open downward to admit the motor's fixed double-ended shaft. The design tire envelope radius is 39.5 mm, 8 mm larger than the physical 31.5 mm radius. The wheel cavity has a minimum 40.5 mm radius envelope. Each roof has 45-degree slopes and a 20.55 mm central bridge. Physical tire hardware remains 63 x 29 mm.

The shell has larger base bosses and thicker lid supports. Its support ledge has local recesses for the eight chassis sensor carriers. The skirt extends exactly 3 mm below the base underside: Z0 on tucked robots and Z-13 on the low-axle robot. The gray material below the recessed lettering has extra backing so the lettering does not reduce its nominal 5 mm structural section. The white inlays remain decorative material volumes, not 5 mm structural parts. Screw bores, counterbores, wire passages, windows, service openings and assembly clearances are intentional local openings. Nominal wall thickness is not a claim that every fastener edge has 5 mm of material.

## Edition dimensions

All bodies remain 279.4 mm long with their tops at Z165. Tucked bodies are 165 mm high; the low-axle body is 178 mm high after extending its skirt to Z-13. Organizers remain 155 mm wide. The four-wheel robot is 158 mm wide, giving 2.8 mm clearance between the unused inner shaft tips. BOTH eight-wheel bodies are now 220 mm wide. All robot side walls run continuously to the bottom edge; the wheel wells sit behind the 5 mm skins, with no wheel arches cut into the outer sides.

The low-axle eight-wheel chassis is 209.6 mm wide inside its 220 mm body. Its axles remain at Z-22, now 9 mm below the extended body edge. Tire projection is 40.5 mm below that edge; total nominal height remains 218.5 mm. The tucked versions keep axles 18 mm above the body edge, exposing 13.5 mm of tire and giving a nominal total height of 178.5 mm.

Bottom retention replaces the old low motor feet. Nominal ground clearance to the bottom retaining plates is about 11.5 mm on tucked robots and 11.8 mm on the low-axle robot, before screw-head height. Zip versions have approximately 15.9 mm clearance below the bottom motor tie. These values use the physical 63 mm tires. The enlarged CAD clearance envelope is not a claim that larger tires fit the shafts or body.

The LCD opening remains 50.1 x 39.6 mm with the established mounting-hole pitch. Its bezel is now 5 mm thick; the glass and PCB seat move 3 mm inward. A new LCD fit coupon is included. LED PCB dimensions and module counts stay unchanged. All robots use six modules per side.

Organizer main cups are now 166.4 x 111 x 88 mm. Five-millimeter floors/dividers retain four 38.1 mm shallow cells and four 83 mm deep cells. Print either the shallow-left or shallow-right version. The tower cup is 58.4 x 94.4 x 100 mm, with four 95 mm deep cells. Its smaller footprint leaves stronger material around the roof opening.

## Files to print

Choose one folder under output/reinforced: seven, six, exposed, four or wide. Each contains a self-contained SCAD and printable STL files. shell-two-color.3mf contains the reinforced shell and aligned white inlays as one object; assign gray and white filament explicitly. It is a geometry project, not a printer profile.

For a single-color body, print r-shell.stl; its recessed lettering has the thicker backing. For two colors, use the 3MF or import r-shell and r-white together without independently centering them.

Every edition: one r-shell and two r-retainers. Organizers use r-frame. Robots use ONE base: r-frame for screw-cap retention, or r-frame-zip for zip-tie retention. Do not print both bases for one robot. Optional r-white supplies the inlay material. Print r-lcd-coupon before the full body.

Organizers: add ONE r-cup-left or r-cup-right, and one r-cup-tower. Robots: add one r-lid and one r-tray. The screw-cap base needs four r-caps. The zip-tie base needs no r-caps; supply eight 3.6 mm wide side ties (at least 250 mm long, at most 1.2 mm thick) and four 2.5 mm wide top ties (at least 250 mm long, at most 1.0 mm thick). There are no r-pod or r-hood parts in this revision.

Use the updated native Bambu project matching the robot and retention method. For the fastest four-wheel zip print, open wopr-four-one-piece-zip-single-color.3mf: every part uses filament 1 and no prime tower. The original two-color choices remain available. Its part list contains one complete chassis. The previous Bambu projects with separate motor pods or wheel hoods are superseded.

Wheel hub seating depth still needs a physical check. The nominal wheel inner face is 12.5 mm from the motor center; the service position moves it 6.5 mm away from the motor, providing 0.7 mm clearance beyond the nominal 18.3 mm shaft tip. Support the gearbox and never hammer a wheel onto a shaft.

## Material and orientation

The supplied native projects use Generic PETG, the Bambu Lab H2D 0.4 mm nozzle, a Textured PEI Plate and the existing 0.24 mm Standard process. Five perimeters, six top/bottom layers and 35% rectilinear infill preserve the existing reinforcement choices. The two eight-wheel battery blocks retain 100% rectilinear modifiers. Supports use the measured faster snug automatic style where needed. Short bridges up to 30 mm are excluded from support generation; inspect their first print for sag. Do not use this profile for ASA without selecting a matching filament profile.

Print the shell upright. Print the tucked chassis bottom down, retainers and tray flat, and the new flat motor plates on their broad faces. Wheel roofs use 45-degree slopes with a 20.55 mm central bridge. Zip-pillar shoulders and organizer raised-floor undersides also use 45-degree slopes. Organizer floor bridges span 25.7 mm. The low-axle chassis still projects below its main base and may need support there. Inspect all pockets and tie tunnels before assembly.

Parts need about 280 x 155 mm, 280 x 158 mm or 280 x 220 mm of usable bed area plus brim. Do not scale parts to fit a smaller printer. The current measured comparison and complete-kit times are in print-review.json. Comparisons of chassis plus single-color shell cover those two parts, not the complete kit. Bambu estimates and support deposition for the four-wheel print are recorded in output/reinforced/bambu-projects/print-review.json. These are slicer estimates. Actual time, strength and bridge quality need a physical print.

## Fasteners

- Every edition: eight M3x20 base screws, with heads no taller than 3 mm.
- Robots: four M3x20 main-lid screws; four 3.6 mm tray ties at least 150 mm long. The tray no longer uses screws.
- Screw-cap robots only: eight M3x14 screws secure the four motor caps.
- Zip-tie robots only: eight 3.6 mm side ties and four 2.5 mm bottom-to-top ties, at least 250 mm long.
- Eight-wheel battery shelves: four 3.6 mm ties, at least 300 mm long.
- Center battery: two straps up to 10 mm wide and 2 mm thick, at least 350 mm long.
- Sensors: thirty-two M2x4 screws, four per board; verify actual screw penetration before tightening.
- LED retainers: eight M2x10 screws. LCD: four M2x6 screws; verify actual board thickness and safe tip depth with the coupon.

M3 pilots are 2.5 mm and are intended for plastic-compatible screws. Hand-tighten; the parts do not contain modeled heat-set inserts. Confirm screw lengths on the actual prints before tightening against electronics.

## Robot assembly order

1. Remove all support material from the one-piece chassis. Fit the eight ToF boards in the low chassis recesses with M2x4 screws before fitting motors and wheels. Each board rotates 90 degrees, with its connectors facing up/down. Route leads upward and keep them clear of the ground and tires. Check the motor pockets, shaft slots, fixed wheel chambers and screw or zip-tie passages. Do not try to assemble the earlier loose motor-mount or wheel-cover parts onto this chassis.
2. For the zip-tie version, each tie makes a complete horizontal loop around the motor and both side supports. Feed it front-to-back through the LEFT support tunnel, across the back of the motor, then back-to-front through the RIGHT support tunnel. Close the head across the front of the motor. Repeat at the second height. The 1.8 x 4.6 mm tunnels run beside the motor, never through its pocket. Leave the loops loose until the motor is seated. Put the side-tie heads toward the nearest outer side of the case, away from the battery shelves. Pre-thread the third tie beneath the gearbox and through the two vertical reliefs and top-stop slots; this path is offset 6 mm from the shaft centerline.
3. Raise each BARE motor from below, motor can upward. Its fixed double shaft enters the downward-open slots. Raise it until the motor can reaches the integral top stop, with 0.4 mm nominal clearance for a thin pad. Do not install wheels before this step.
4. Insert each wheel from below at its service position: 6.5 mm farther away from the motor than its running position. Raise it until the hub aligns with the shaft, then slide it inward and press it fully onto the shaft while supporting the gearbox. Repeat for one outward wheel per motor on the four-wheel model, or both shaft ends on either eight-wheel model.
5. Verify every wheel turns freely. For screw retention, fit a thin foam pad between the gearbox and bottom retaining plate, then drive two M3x14 screws upward into the chassis. Nominal plate-to-gearbox gap is about 1.0 mm on tucked models and 0.7 mm on the low-axle model. For zip retention, tighten the two horizontal ties against the motor faces. Tighten the third tie beneath the gearbox and over the integral top stop to prevent downward removal. Keep bands away from terminals and insulate solder joints. Trim tails and confirm that the motor cannot move or rock. Do not add a retaining plate to the zip base.
6. Route motor wires clear of tires and tie tails. Turn the selected USB pack across the case: its 104 mm dimension runs across the width, and its 52.3 mm dimension runs lengthwise. Seat it on the 8 mm rails above the LED leads and strap it through the base slots. Mount the controller and drivers on the insulating carrier. Secure the 5 mm tray with four ties: down one tray slot, through the horizontal tunnel below the post, up the paired tray slot, then over the tray.
7. Fit LED modules with the reinforced retainers, then the LCD using the new fit coupon. Fit the motor-power switch. Attach the body with eight M3x20 screws and the lid with four M3x20 screws.

For wheel service, remove the body and loosen the motor cap or ties as needed. Slide the wheel away from the motor into the service space before lowering it through the underside opening.

Organizer assembly: install display and RGB hardware first, fit the 10 mm base, then lower the two reinforced cups onto their support ledges. The cups remain removable for access.

## Level battery shelves and tray

The tray and both eight-wheel shelves have top surfaces at Z72.3 mm. Each platform is 56 x 53.12 mm: its across-case width is reduced by 20%. It is a continuous solid CAD block from the angled wheel-well roof to the platform top. Two 4.6 x 1.8 mm tunnels run horizontally through each block, beneath a 5 mm top skin. Feed each tie straight through a tunnel, then wrap it around the pack; keep its head on the upper outside face above the motor supports. Verified pack envelope per platform is 54 x 49.12 x 40 mm, including any padding; use protected battery packs. The native Bambu projects include two 100% rectilinear infill modifiers for the battery blocks. Keep these modifiers enabled to print the blocks densely. Other parts retain their existing settings. The blocks supplement the original central USB pack bay. The four-wheel model has no center wheel cavities and therefore no added wheel-cavity shelves. Do not connect separate packs together without a suitable power circuit.

## Lighting holes

All robot models now have 22 holes for 5 mm LEDs: eight at the OUTER wheel positions, six between the wheels (three per side), and eight below the tray in a 4 x 2 grid. The inner wheel wells have no LED holders or LED holes. All three also have FOUR 8 mm LED holes, at their existing body positions Y40/W-40, Z44; they do not move with the sensors. These counts exclude the existing RGB modules.

The 5 mm holes are nominal lens bores. Wheel-roof bosses include 6 mm flange seats, 1 mm deep, so the lens stays recessed from the tire space. Use LED lens bodies no longer than 8.7 mm below the flange and flanges no wider than 6 mm; check actual parts before printing. Seven millimeters of lead-routing space is reserved above the base and wheel bosses. The 8 mm holes reserve a 9 mm diameter, 8 mm deep internal LED/wire space. Fit and insulate the leads, add strain relief, and confirm all lenses stay clear of rotating tires. Add appropriate current limiting; this revision adds mounting provisions, not LED control firmware.

## Eight distance-sensor mounts

Mount eight Adafruit 3967 VL53L1X boards on the chassis around the wheel-housing bases, rather than on the main body. There are two front, two rear and two per long side. Their centers are 14 mm above the base underside: Z17 on tucked models and Z4 on the low-axle model. Front/rear boards line up with the motor rows at Y59.3 and W-59.3. Side boards line up with the wheel/axle stations. All boards rotate 90 degrees, giving a 12.70 mm horizontal and 20.32 mm vertical mounting pitch.

Each carrier has four blind 1.6 mm pilots, 2.5 mm deep, for M2x4 screws. The recessed board seats 3.5 mm behind the chassis face. This local sensor pocket leaves a 3.5 mm face skin, except at the optical window and blind pilots. PCB/connector envelopes clear both the enlarged running tire space and the complete bottom-insertion paths. The removable skirt covers the boards and screw heads; only 10 mm optical windows remain visible. The former Z64 main-body sensor holes and mounts are removed. The four 8 mm end LEDs remain on the body at their previous positions.

Eight-wheel axle stations shift 5 mm inward to X51.3 and X228.1 so the enlarged wells stay behind 5 mm end skins. Four-wheel stations remain X54 and X225.4. Sensor mounts are integral with either screw-retention or zip-retention chassis. A physical fit and optical-range test is still required.

Dimensions come from Adafruit's Eagle board: outline 25.4 x 17.78 mm; four 2.5 mm board holes at X2.54/22.86 and Y2.54/15.24; sensor centered at X12.7,Y8.89. The supplied firmware does not yet read these added sensors. Their common default I2C address is 0x29, so eight boards need separate address initialization via XSHUT or an I2C multiplexer before shared-bus use.

## Electronics and Wi-Fi

The original drive electronics and firmware remain unchanged: four Adafruit 3777 motors; Adafruit 3766 wheels; ESP32-DevKitC V4; two Adafruit 3297 DRV8833 drivers; Anker A1259 USB pack (104 x 52.3 x 26 mm). Retain the 5 V, 2.5 A fused supply and 0.5 A current limit per motor, set with four 0.40-ohm sense resistors. Use a 12 mm latching motor-power switch rated at least 3 A at 5 V DC, two 470 uF / 10 V driver capacitors and four 100 nF motor-terminal capacitors. The USB-C sink breakout must be rated 3 A and use 5.1k CC resistors; never select a higher-voltage PD trigger. Use 18-22 AWG power wiring, insulated connectors, two 10 mm battery straps at least 350 mm long and a nylon-mounted insulating controller carrier no larger than 90 x 65 mm. Reuse Adafruit 3315 LCD and the existing Seeed RGB modules.

The existing sketch in firmware/wopr-robot/wopr-robot.ino creates the WOPR access point and captive controller page. Join WOPR; use its Wi-Fi sign-in prompt, or open http://192.168.4.1. The public setup password remains wopr-car-setup and should be changed locally. Left driver: AIN1/AIN2 to GPIO25/26 (front motor), BIN1/BIN2 to GPIO27/14 (rear). Right driver: AIN1/AIN2 to GPIO32/33 (front), BIN1/BIN2 to GPIO18/19 (rear). Both SLP pins go to GPIO23 with a 10k pulldown; both open-drain FLT pins go to GPIO21 with a 10k pullup to 3.3 V. Common ground; never connect driver outputs together. The unchanged sketch was previously compiled with Espressif Arduino core 3.3.8; this task does not flash hardware.

Test direction, release-to-stop, STOP, Wi-Fi loss, driver fault and the manual switch with wheels raised. Disconnect the battery before attaching PC USB for programming. Start driving tests with RGB/LCD power disconnected. The lighting current must be measured and brightness limited so the complete system stays below 2.5 A continuous. The drive sketch does not regulate lighting.

## Verification and limits

The builder checks watertight connected structural meshes, actual exported wall/base/top-stop thicknesses, tray tie paths, shelf pack volumes, sensor/connector envelopes and LED lead space, wheel and battery clearance, LCD/LED fit volumes, and bare-motor insertion, wheel lifting and axial fitting paths. The zip-tie check now includes the complete external belt and lock head against the motor, chassis, wheels and enclosure. The prior straight-through slots are superseded; their earlier empty-slot check did not prove a usable loop. White lettering consists of separate glyph solids by design.

This is a stronger CAD revision, not a certified load or drop rating. Print fit, motor torque under the heavier case, steering scrub, operating temperature, runtime and impact durability remain untested. Plastic TT gears and press-fit wheel hubs remain mechanical limits. Check an actual motor and wheel against the fit geometry before relying on the full set. Zip-tie retention also needs a physical pull/rocking test and inspection after driving.

## Component references

https://www.adafruit.com/product/3777
https://www.adafruit.com/product/3766
https://www.adafruit.com/product/3297
https://www.adafruit.com/product/3315
https://www.anker.com/nz/products/a1259-built-in-cable-power-bank-10000mah
https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32/esp32-devkitc/user_guide.html

https://www.adafruit.com/product/3967
https://github.com/adafruit/Adafruit-VL53L1X-PCB
