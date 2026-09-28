// Variants reuse the approved shell proportions and LCD mount. Millimeters.
// Build with -D panels_per_side=6. Original wopr.scad remains unchanged.
include <wopr.scad>
robot_axle=-22; motor_xs=[48,231]; motor_ys=[28,127];
module pods() { for(x=motor_xs,y=motor_ys) translate([x,y,0]) children(); }
module axle_cylinder(r,h) { rotate([90,0,0]) cylinder(r=r,h=h,center=true,$fn=64); }
module wheel_voids(clear=0) { pods() for(s=[-1,1]) translate([0,s*27,robot_axle]) axle_cylinder(31.5+clear,29+2*clear); }
module motor_void() {
    translate([-11.7,-9.7,-36.4]) cube([23.4,19.4,38.4]);
    translate([-11.7,-11.7,2]) cube([23.4,23.4,32.6]);
    translate([0,0,robot_axle]) axle_cylinder(3.5,32);
}
module cradle() {
    difference() {
        union() {
            translate([-15,-11.9,-39]) cube([30,23.8,42]);
            translate([-15,-15,1]) cube([30,30,37]);
            for(x=[-20,20]) translate([x-4,-6,3]) cube([8,12,35]);
        }
        motor_void();
        // Open top; foam under removable cap bears on motor rear, not terminals.
        translate([-11.7,-11.7,34]) cube([23.4,23.4,8]);
        for(x=[-20,20]) translate([x,0,25]) cylinder(d=2.5,h=20);
    }
}
module motor_cap() { difference() {
    translate([-24,-15,38.3]) cube([48,30,4]);
    for(x=[-20,20]) translate([x,0,37]) cylinder(d=3.3,h=8);
    translate([-6,-8,37]) cube([12,16,8]); // terminals and wire exit
} }
module robot_floor() { difference() {
    union() {
        translate([base_inset,base_inset,base_bottom]) linear_extrude(6) offset(r=3) translate([3,3]) square([L-2*base_inset-6,W-2*base_inset-6]);
        // Wheel wells are closed above and on their sides, open only toward ground.
        intersection() {
            pods() for(s=[-1,1]) translate([0,s*27,robot_axle]) axle_cylinder(37.5,37);
            translate([-10,-30,3]) cube([L+20,W+60,20]);
        }
        pods() cradle();
        // Battery fence, 108 x64 usable; straps cross the pack at X112 and165.
        for(y=[42,110]) translate([83,y,9]) cube([116,3,12]);
        for(x=[83,196]) translate([x,42,9]) cube([3,71,12]);
        for(x=[110,163],y=[38,114]) translate([x,y,9]) cube([12,6,8]);
        // Upper removable electronics tray supports, away from wheels and LCD.
        for(x=[92,178],y=[39,116]) translate([x-5,y-5,9]) cylinder(d=10,h=58);
    }
    wheel_voids(2);
    pods() motor_void();
    for(x=[12,128,151,L-12],y=[13,W-13]) translate([x,y,2]) cylinder(d=3.3,h=10);
    for(x=[92,178],y=[39,116]) translate([x-5,y-5,55]) cylinder(d=2.5,h=15);
    for(x=[110,163],y=[37,113]) translate([x+2,y,11]) cube([8,8,3]);
} }
module hatch_cut() { translate([9,15,116]) cube([178,125,70]); }
module lid_screws(d=3.3) { for(x=[15,181],y=[21,134]) translate([x,y,108]) cylinder(d=d,h=50); }
module robot_raw_shell() { difference() {
    union() {
        difference() { outline(); inside(); light_cuts();
            translate([tft_x-32.8,-1,tft_z-26.8]) cube([65.6,40,53.6]); }
        light_mounts(); display_bay(); base_bosses();
        // Main lid ledges attached to the existing side wall.
        for(x=[9,175],y=[5,130]) translate([x,y,107]) cube([12,20,9]);
    }
    white();
    translate([-1,77.5,55]) rotate([0,90,0]) cylinder(d=12.3,h=7); // filled by latching motor-power switch
    for(dx=[-29.845,29.845],dz=[-23.749,23.749]) translate([tft_x+dx,1,tft_z+dz]) rotate([-90,0,0]) cylinder(h=4,d=1.8);
    translate([-1,-1,-7]) cube([L+2,W+2,7]);
    // No pen apertures, cable slot, vents or exposed bottom openings.
    wheel_voids(2.4);
} }
module robot_shell() { difference() { robot_raw_shell(); hatch_cut(); lid_screws(2.5);
    // Floor wheel guards seat outside shell with a running assembly gap.
    pods() for(s=[-1,1]) translate([0,s*27,robot_axle]) axle_cylinder(37.9,37.8);
} }
module robot_lid() { difference() {
    union() {
        intersection() { robot_raw_shell(); translate([9.3,15.3,116.3]) cube([177.4,124.4,70]); }
        // Flat inner lid closes the hollow center below the original raised spine.
        translate([9.3,15.3,116.3]) cube([177.4,124.4,4]);
        intersection() { outline(); difference() { translate([9.3,15.3,119]) cube([177.4,124.4,12]); translate([12.3,18.3,118]) cube([171.4,118.4,15]); } }
    } lid_screws();
} }
module electronics_tray() { difference() {
    translate([81,28,67.3]) cube([102,88,3]);
    for(x=[92,178],y=[39,116]) translate([x-5,y-5,66]) cylinder(d=3.3,h=6);
    // Universal strap slots; nylon standoffs on carrier board avoid unknown board holes.
    for(x=[96,120,144,168],y=[36,64,94]) translate([x,y,66]) cube([3,14,6]);
} }
module drive_reference() { pods() {
    color([0.95,0.67,0.07]) translate([-11.2,-9.3,-36]) cube([22.4,18.6,38]);
    color([0.55,0.57,0.59]) translate([-10,-11.2,2]) cube([20,22.4,32]);
    color([0.8,0.8,0.8]) translate([0,0,robot_axle]) axle_cylinder(2.7,36.6);
    for(s=[-1,1]) {
        color([0.98,0.40,0.08]) translate([0,s*27,robot_axle]) axle_cylinder(31.5,29);
        color([0.82,0.83,0.80]) translate([0,s*42,robot_axle]) axle_cylinder(20,1);
    }
} }
module onboard_reference() {
    color([0.12,0.15,0.19]) translate([87,47,10]) cube([104,52.3,26]);
    color([0.08,0.40,0.26]) translate([91,40,74]) cube([55,28,10]);
    color([0.1,0.35,0.65]) for(y=[77,99]) translate([105,y,74]) cube([26,18,9]);
}
module robot_assembly(open=false,explode=false) {
    color([0.40,0.43,0.46]) translate(explode?[0,0,70]:[0,0,0]) robot_shell();
    color([0.98,0.98,0.96]) translate(explode?[0,0,70]:[0,0,0]) white();
    color([0.31,0.34,0.37]) robot_floor();
    color([0.40,0.43,0.46]) if(!open) translate(explode?[0,0,140]:[0,0,0]) robot_lid();
    color([0.65,0.68,0.70]) translate(explode?[0,0,35]:[0,0,0]) electronics_tray();
    color([0.50,0.53,0.56]) pods() motor_cap();
    if(electronics) { drive_reference(); onboard_reference(); if(!explode) reference_parts(); }
}
module robot_checks() {
    translate([-100,-100,-100]) cube(1);
    intersection() { union(){robot_shell();robot_floor();robot_lid();electronics_tray();pods() motor_cap();} wheel_voids(0.2); }
    intersection(){robot_shell();robot_lid();}
    intersection(){robot_shell();robot_floor();translate([-10,-30,9.01]) cube([L+20,W+60,200]);}
    intersection(){robot_floor();electronics_tray();}
    intersection(){union(){robot_shell();robot_floor();electronics_tray();} translate([87,47,10]) cube([105,54,30]);}
}
if(part=="robot") robot_assembly();
else if(part=="robot-open") robot_assembly(true);
else if(part=="robot-exploded") robot_assembly(false,true);
else if(part=="robot-shell") robot_shell();
else if(part=="robot-floor") robot_floor();
else if(part=="robot-lid") robot_lid();
else if(part=="robot-tray") electronics_tray();
else if(part=="robot-cap") motor_cap();
else if(part=="robot-check") robot_checks();
else if(part=="robot-drive") {color([0.4,0.43,0.46]) robot_floor();drive_reference();}

if(part=="robot-pod-test") intersection(){robot_floor();translate([8,-20,-45]) cube([80,98,95]);}
