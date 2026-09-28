# WOPR concealed-wheel variants

2026-09-28. Two additional designs; the previous eight-wheel robot and six-per-side replica remain available unchanged. These are checked CAD prototypes, not physically tested vehicles.

## Choose a version

Four-wheel: four Adafruit 3777 motors and four Adafruit 3766 wheels, one wheel on the outward shaft of each motor. Body and overall width: 155 mm. Wheel centers are X60/219 and Y25/130. Wheelbase: 159 mm. Track: 105 mm. The unused inner shaft on each motor stays inside the enclosure.

Wide eight-wheel: four of the same motors and eight of the same wheels, two per motor. Body and overall width: 210 mm, increased from the original 155 mm body to cover every wheel. Wheel centers are X48/231 and Y25/79/131/185. Wheelbase: 183 mm. Both wheels on each motor rotate together.

Both: body length 279.4 mm; body height 165 mm; nominal total height 178.5 mm. Axles are 18 mm ABOVE the skirt edge. The 63 mm tires project only 13.5 mm below the body: about 79% of wheel diameter is tucked into the unit. Tire sidewalls stay at least 10.5 mm inside the body outline. Closed wheel tubs isolate the wheel space from the battery and electronics. The bottom is closed apart from wheel openings, fitted fasteners and motor shaft passages within the tubs.

Six RGB modules per side and the original LCD opening are retained. Main lid is removable; the LCD tower roof remains closed. The wide version centers the raised spine across its larger width. The battery pocket and removable controller tray remain in the main compartment.

## Print parts and compatibility

Use the matching folder: output/concealed/four-wheel or output/concealed/wide-eight-wheel. Print one concealed-shell, one concealed-floor, one robot-lid, one concealed-tray, four robot-caps and two LED retainers. Also print two wheel-hood-front and two wheel-hood-rear covers for the four-wheel version, or four of each cover for the eight-wheel version. Optional white-text is aligned with the shell; open shell-two-color.3mf for a single shell object with gray/white material parts. Assign filament colors in the slicer. Standard 3MF contains geometry, not a printer profile.

Each folder also includes a concealed-pod-test coupon and the LCD fit-coupon. Print one motor coupon, one cap and the matching wheel hoods first. Fit the actual motor and the appropriate one or two wheels before printing the entire floor. Manufacturer wheel hub seating depth remains unverified; the model assumes 12.5 mm from motor center to wheel inner face. Confirm full hub engagement without rubbing.

Do not mix the previous eight-wheel shell or floor with these new parts. These designs use a new eight-screw base pattern: three screws along each long side and one at each short end. The narrow lid retains its earlier geometry. The wide lid and white lettering span are wider. Motor caps, LED retainers and LCD fit geometry remain the same.

Use PETG or ASA. Initial settings: 0.2 mm layers, five walls, six top/bottom layers and 35% gyroid infill; solid local regions at clamps and screw supports. Shell upright, tray and caps flat. Inspect floor and lid support needs in the slicer; completely clear supports from motor sockets, wheel tubs and shaft bores. These settings are a starting point, not a strength rating. Full-size parts need approximately 280 x 155 mm or 280 x 210 mm plus brim. Do not scale to fit a small bed.

## Parts list

- Four Adafruit 3777 TT motors (3-6 V). Four or eight Adafruit 3766 wheels (63 x 29 mm), according to the chosen variant.
- One ESP32-DevKitC V4 with ESP32-WROOM-32E and two Adafruit 3297 DRV8833 dual motor drivers. One driver channel per motor.
- One Anker A1259 USB power bank, 104 x 52.3 x 26 mm. Use its 5 V / 3 A output only. No higher-voltage PD trigger.
- One USB-C 5 V sink breakout rated 3 A with 5.1k CC resistors; one 2.5 A fuse; one 12 mm latching motor-power switch rated at least 3 A at 5 V DC.
- Four 0.40-ohm, 1%, 1206 sense resistors rated at least 0.25 W. Replace the two 0.2-ohm resistors on each driver to limit each motor to 0.5 A. Do not disable current limiting.
- Two 470 uF / 10 V capacitors at the drivers; four 100 nF capacitors across motor terminals; 10k SLP pulldown and 10k FLT pullup to 3.3 V. Insulated connectors, 18-22 AWG power wire and 26 AWG signal wire.
- One insulating carrier/perfboard no larger than 90 x 65 mm, nylon standoffs, board screws and small straps to secure it through the tray slots.
- Two 10 mm battery straps, about 230 mm long; thin battery padding; 5 mm closed-cell foam for motor clamp faces, trimmed to measured fit.
- Eight M3x14 floor screws, four M3x20 lid screws, four M3x10 tray screws and eight M3x12 motor-cap screws. Add two M3x12 screws per wheel hood: eight more for four wheels, or sixteen more for eight wheels. Use plastic-compatible screws with the modeled 2.5 mm pilots; hand-tighten.
- Eight M2x6 LED-retainer screws and four M2x6 LCD screws; confirm safe insertion depth on actual boards. Reuse twelve Seeed RGB modules and the Adafruit 3315 LCD assembly.

## Mechanical assembly

1. Test the coupon with its cap and wheel hoods. With the motor outside the cradle, press one outward wheel onto its shaft for the narrow model, or two wheels for the wide model. Support the gearbox. Never hammer a hub or cut off the unused inner shaft.
2. Lower the complete motor-and-wheel assembly into the open cradle from above. The shafts enter open U-slots, and the wheels enter the open lower tubs. Motor can points upward. Check that the motor seats fully and both shafts align.
3. Before installing the motor cap, lower the matching removable hoods over the wheels. Each hood's notch faces its motor; its small external screw ears seat on two floor posts. Use two M3x12 screws per hood. Then fit the motor cap with two M3x12 screws and a 5 mm foam pad, trimmed to compress lightly in the nominal 4 mm gap. Check the 1 mm nominal tire clearance through a full turn. Repeat for all four motors, then route and strain-relieve the leads through cap slots.
4. Mount RGB panels with one retainer per side, four M2 screws each. Mount the LCD from the rear with four M2 screws. The front opening and rear clearance are unchanged.
5. Pad and strap the Anker pack inside the center fence. Keep its cable above the battery and below the tray, away from wheel wells and motor shafts. Charge the pack outside the closed case.
6. Mount the ESP32 and drivers on the insulating carrier. Place both drivers side by side below the controller on the tray. Secure the carrier using nylon hardware and tray straps. Fit the tray with four M3x10 screws at its revised mounting positions.
7. Install the motor-power switch in the 12.3 mm end hole. Wire and check polarity before closing the case. Verify OFF removes power from both motor drivers.
8. Fit the matching shell with eight M3x14 screws. Fit the main lid with four M3x20 screws. Check every wheel by hand and confirm no cable enters a wheel tub.

## Wiring and Wi-Fi control

The existing firmware is unchanged: firmware/wopr-robot/wopr-robot.ino. It already drives four motors. Use Espressif Arduino core 3.3.8 and ESP32 Dev Module. Disconnect battery and turn motor power OFF before programming over USB. Never power the ESP32 from a PC USB cable and the battery 5 V feed at the same time.

Bank 5 V -> 2.5 A fuse -> distribution. Logic branch to ESP32 5V/GND. Motor branch through the latching switch to both driver VMotor inputs. All grounds common. Place the electrolytic capacitors near the drivers and observe polarity.

Left driver: AIN1/AIN2 to GPIO25/26 (front motor), BIN1/BIN2 to GPIO27/14 (rear). Right driver: AIN1/AIN2 to GPIO32/33 (front), BIN1/BIN2 to GPIO18/19 (rear). Both SLP pins to GPIO23 with 10k to ground. Both open-drain FLT pins to GPIO21 with 10k to 3.3 V. Never connect driver outputs together.

Join the WOPR access point. Public setup password: wopr-car-setup; change it locally before use. DNS and DHCP support the Wi-Fi sign-in popup, which contains the controller. If the phone does not open it, use http://192.168.4.1 while connected. Press Arm and hold a direction; release stops and requires re-arming. Lost messages, disconnected Wi-Fi and driver fault stop motor commands. Phone popup behavior still needs testing on the actual hardware.

Keep the 0.5 A current limit on each channel (0.2 V / 0.40 ohm). Four motor channels allow about 2 A plus controller consumption. Begin with RGB/LCD power disconnected. Enable lighting only after measuring total demand and enforcing a brightness limit below the 2.5 A continuous system budget. The drive firmware does not control RGB brightness.

## Commissioning and limits

Start with wheels raised. Check each motor direction, release-to-stop, STOP, Wi-Fi disconnect, page close, driver fault and the manual motor-power switch. Swap that motor's two leads with power OFF if a wheel turns backward.

Test gentle arcs on smooth indoor flooring before using the closed case. The 13.5 mm ground clearance is low: this is not a curb or rough-ground chassis. Eight tires cause more steering scrub than four. Plastic TT gears and press-fit hubs still limit impact durability. No payload, drop, water-resistance or runtime rating has been measured.

CAD verification checks solid meshes; four motors and correct wheel counts; wheels inside the body width; 13.5 mm tire projection; wheel/shaft/battery/tray/LCD/LED clearances and motor/wheel top-insertion paths; and preservation of the previous eight-wheel shell and lid. Physical printing, fit, torque, temperature, traction and durability remain untested.

## Component references

https://www.adafruit.com/product/3777
https://cdn-shop.adafruit.com/product-files/3777/3777_diagram.jpg
https://www.adafruit.com/product/3766
https://www.adafruit.com/product/3297
https://learn.adafruit.com/adafruit-drv8833-dc-stepper-motor-driver-breakout-board/pinouts
https://www.anker.com/nz/products/a1259-built-in-cable-power-bank-10000mah
https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32/esp32-devkitc/user_guide.html
