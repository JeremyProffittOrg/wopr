# WOPR variants - assembly and operation

Current reinforced editions (2026-09-29): see [REINFORCED.md](REINFORCED.md) and use `output/reinforced` for new prints. The files and dimensions below describe archived pre-reinforcement editions.


Design date: 2026-09-28. Six RGB modules per side, twelve total, on both variants. The original seven-per-side source and exports remain unchanged. Dimensions are millimeters. This is a CAD-checked prototype; no physical fit, load, drop, traction, thermal or battery test has been performed.

## Files and dimensions

Replica: output/variants/replica. Print one gray-shell, one base, one tower cup, ONE of the two main cups, and two LED retainers. Optional white-text shares the shell origin; import both together without centering each part separately. Fit-coupon is the existing LCD trial piece. The body is 279.4 x 155 x 165. LED banks are 127.23 wide. All prior LCD trims and storage dividers remain.

Robot: output/variants/robot. Print one robot-shell, robot-floor, robot-lid and robot-tray; four robot-caps and two LED retainers. Optional white-text and fit-coupon are included. Body remains 279.4 x 155 x 165; wheel guards extend width to 190. Axles are 22 below the skirt; wheel bottoms are 53.5 below it, giving nominal overall height 218.5. Pod bottoms are 39 below skirt: ground clearance 14.5. Wheelbase 183, pod-track 99. The upper main lid is removable; LCD tower roof stays fixed.

The single motor is upright in each pod. Two wheels fit opposite ends of its common axle and must rotate together. Four motors produce eight driven wheels. Left and right pod rows have separate electrical control. Do not put one two-wheel axle across the full vehicle width: that would prevent left/right differential steering.

## Purchased parts

- 4 x Adafruit 3777 TT motor, 3-6 V, plastic 48:1 gearbox, nominal 70 x 22 x 18 body; manufacturer drawing includes 36.6 shaft span.
- 8 x Adafruit 3766 orange/clear wheel, 63 diameter x 29 wide, one per order. Listed out of stock when checked. Do not substitute a different wheel without checking the CAD envelope.
- 1 x Espressif ESP32-DevKitC V4 with ESP32-WROOM-32E (not WROVER). Reference envelope 55 x 28 x 10; allow header and cable height.
- 2 x Adafruit 3297 DRV8833 dual motor driver. One H-bridge channel per motor. Each board 26 x 18 before terminals/wires.
- 1 x Anker Nano A1259 10,000 mAh 30 W power bank, 104 x 52.3 x 26. Use only its 5 V output, maximum 3 A. The 30 W headline does NOT mean 6 A at 5 V. Battery fence and straps retain this size; leave cable slack under tray.
- 1 x USB-C female 5 V sink breakout rated 3 A, with separate 5.1 k CC resistors; no higher-voltage PD trigger. Connect bank built-in cable; confirm 5 V with meter before connecting electronics.
- 4 x 0.40-ohm 1% current-sense resistors, 1206, 0.25 W minimum. Replace both 0.2-ohm sense resistors on each DRV8833 to set 0.5 A per channel. This requires fine soldering. Do not bridge current-limit jumpers.
- 1 x 12 mm-panel latching motor-power switch, rated at least 3 A at 5 V DC, body under 25 deep, flange under 18 diameter; 12.3 mm bore in low end of case. Switch cuts motor branch only.
- 1 x inline 2.5 A fuse and holder on 5 V supply; 18-22 AWG power wire; 26 AWG signal wire; insulated connectors.
- 2 x 470 uF, 10 V capacitors at driver supplies; 4 x 100 nF ceramic capacitors across motor terminals; 10 k pulldown on SLP; 10 k pullup to 3.3 V on shared FLT.
- 1 x universal insulating carrier/perfboard, no larger than 90 x 65; nylon standoffs, M2 hardware and two small straps to secure it to tray. Board holes vary, so drill carrier only; do not drill live electronics.
- 2 x 10 mm hook-and-loop battery straps, approximately 230 mm long; thin battery padding and 5 mm closed-cell foam for motor clamp faces.
- Robot fasteners: 8 x M3 x 14 floor; 4 x M3 x 20 lid; 4 x M3 x 10 tray; 8 x M3 x 12 motor clamps; 8 x M2 x 6 LED retainers; 4 x M2 x 6 LCD (check safe depth with actual hardware). M3 fasteners use modeled 2.5 mm pilots: use plastic-compatible screws, hand-tighten. No heat inserts are modeled.
- Reuse 12 Seeed XIAO RGB matrix modules and the Adafruit 3315 LCD assembly from the base design. Their control electronics, interconnects and lighting program remain the existing system. The included drive firmware controls motors only.

## Print and fit

Use PETG or ASA for structural parts; matching white material for lettering. Start at 0.2 mm layers, 5 perimeters, 6 top/bottom layers and 35% gyroid infill. Use local solid regions at motor clamps and screw supports. These are proposed settings, not a verified strength rating. Original shell nominal wall is 3 mm; floor 6 mm.

A printer must accept at least 280 x 190 mm plus brim for the robot floor. This exceeds a 256 mm bed in length. Print shell upright, lid exterior upward, tray flat and caps flat. Floor has downward motor cradles: inspect supports carefully in the slicer and remove all support in wheel wells, shaft bores and motor sockets. Do not scale to fit a smaller bed; that changes hardware fit.

Print one motor test pod before the full floor. Check the actual motor, both wheels, shaft engagement, wire exit and clamp. The wheel hub seating depth is not dimensioned on the wheel product page. CAD uses wheel inner faces 12.5 mm from pod center; verify both hubs seat fully without touching cradle. Do not force a wheel with a hammer or drive a screw into an unthreaded shaft. If fit differs, adjust the pod before printing the chassis.

## Mechanical assembly

1. Remove support; deburr pilots and all moving clearances. Dry-fit shell, floor, lid and tray. Verify each wheel turns without rubbing through a full revolution.
2. Insert each motor from above, gearbox/axle down, can upward. Seat it against the cradle stop and check that its shaft is centered in the bore. Pass shafts through side bores. Fit two wheels per motor; support the gearbox while pressing hubs on. Install each top cap with 2 M3 x 12 screws and a 5 mm cap foam pad that avoids terminals. Trim foam to the measured gap (nominally about 4 mm) so it compresses lightly. Do not crush the motor case.
3. Solder noise capacitors to motor terminals. Route leads upward through cap slots; add strain relief away from shafts and tires. Label LF/LR/RF/RR.
4. Install RGB modules behind the two side windows. Use one retainer per side and 4 M2 screws each. Mount LCD from rear with four screws; verify screw tips cannot reach glass. Preserve the 25.4 mm rear service space.
5. Fit battery in the central fenced pocket on thin foam. Thread both straps through floor lugs and tighten lightly. Battery remains removable; charge it outside the closed robot.
6. Mount controller and drivers on an insulating carrier with nylon standoffs. Strap carrier through tray slots. Keep solder joints clear of tray and route antenna toward open plastic. Connect wiring before fixing tray with 4 M3 x 10 screws.
7. Install latching power switch in 12.3 mm end hole, with nut/washer and strain relief inside. Confirm OFF removes driver motor power.
8. Fit body to floor; use 8 M3 x 14 screws. Fit lid using 4 M3 x 20 screws. Confirm switch and every wheel remain free. No pen cups belong in robot.

## Wiring and power budget

Bank 5 V ->2.5 A fuse -> distribution. Logic branch -> ESP32 5 V/GND (never 3 V3). Motor branch -> latching switch -> both driver VMotor/GND. All grounds common. Do not connect a PC USB cable and external 5 V simultaneously; unplug battery before programming. Place 470 uF capacitors close to each driver, respecting polarity.

Left driver AIN1/AIN2 -> GPIO25/26 (front); BIN1/BIN2 -> GPIO27/14 (rear). Right driver AIN1/AIN2 -> GPIO32/33 (front); BIN1/BIN2 -> GPIO18/19 (rear). Both SLP -> GPIO23 plus 10 k to ground. Both open-drain FLT -> GPIO21 plus 10 k to 3.3 V. Each motor goes to its own A or B output pair. Never tie driver outputs together.

0.2 V /0.40 ohm =0.5 A motor limit. Four channels total at most approximately 2 A; allow 0.5 A for controller and losses, leaving limited margin below 3 A. Do initial driving tests with RGB/LCD power disconnected. Twelve RGB matrices cannot run full-white from this pack. Enable existing lighting only after measuring total worst-case current and staying below 2.5 A continuous; set and enforce brightness accordingly. The drive sketch does not enforce RGB current. If this leaves inadequate torque or lighting, this pack is not sufficient; do not disable motor current limits.

## Phone control

Install/enable the Espressif Arduino 3.3.8 board package (already used for this build). Build firmware/wopr-robot/wopr-robot.ino for ESP32 Dev Module. The supplied public setup password is wopr-car-setup; change it locally before use. Program over USB with motor power OFF and battery disconnected.

Join WOPR on the phone. Its captive portal (the Wi-Fi sign-in page) shows the controller. Wildcard DNS points local names to the ESP32; DHCP advertises the portal, and HTTP connectivity probes redirect to /portal. Tap the phone's sign-in notification if needed. If the page does not open, stay connected and open http://192.168.4.1 manually. HTTPS pages are not intercepted. Press Arm, then hold a direction. Release stops and requires re-arming. Forward left/right use gentle arcs, not stationary spin turns. One Wi-Fi client is accepted. Stop and driver fault disable SLP. The control loop stops after nominal 500 ms without drive messages, on lost Wi-Fi client or driver fault. This is not a certified safety controller.

## Commissioning and durability

First power with wheels raised. Check 5 V polarity and 0.5 A limits before driving. Test each pod direction; if reversed, switch that motor's two wires with power OFF. Confirm that joining WOPR offers the controller in the Wi-Fi sign-in page. Then test release, STOP, phone Wi-Fi OFF, page close and driver fault; all must stop motors. Confirm the manual switch independently removes motor power.

Start on smooth hard flooring at low speed. Eight wide tires create steering scrub; plastic TT gears and press-fit hubs are the limiting parts. This design protects them with cradles/guards but does not make them impact-proof. Verify gentle turning, no wheel rub, no brownout and acceptable measured driver/motor temperature with lid closed. Stop for stalls or warm battery. Do not use on stairs, outdoors in water, or near a drop during commissioning.

No payload rating, drop rating, runtime or waterproof claim is supported. Shell, lid and screw joints need real print/fit testing. Establish acceptable payload and surface with measured tests before calling the vehicle highly durable.

## Verification record

OpenSCAD Manifold exports: all 17 STL files are watertight; each structural part is one connected solid. Assembly probes check wheel movement envelopes, shell/floor/lid/tray separation and the selected battery envelope. Six boards per side are verified by bank and retainer dimensions.

Firmware compile passed for esp32:esp32:esp32 with installed Espressif core 3.3.8. Program storage 960,055 bytes (73%); global variables 47,252 bytes (14%). This proves compilation only. No controller was flashed and no driving or phone captive-popup test was performed.

## Sources

https://www.adafruit.com/product/3777
https://cdn-shop.adafruit.com/product-files/3777/3777_diagram.jpg
https://www.adafruit.com/product/3766
https://www.adafruit.com/product/3297
https://learn.adafruit.com/adafruit-drv 8833-dc-stepper-motor-driver-breakout-board/pinouts
https://www.anker.com/nz/products/a 1259-built-in-cable-power-bank-10000mah
https://docs.espressif.com/projects/esp-dev-kits/en/latest/esp32/esp32-devkitc/user_guide.html
https://docs.espressif.com/projects/arduino-esp32/en/latest/api/ledc.html

https://github.com/espressif/arduino-esp32/blob/3.3.8/libraries/DNSServer/examples/CaptivePortal/CaptivePortal.ino
