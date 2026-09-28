// Additional concealed-drive variants. Existing robots remain available.
// -D part="concealed" -D panels_per_side=6 -D hidden_wide=false -D W=155
// Wide eight-wheel version: hidden_wide=true, W=210.
// Variants reuse the approved shell proportions and LCD mount. Millimeters.
// Build with -D panels_per_side=6. Original wopr.scad remains unchanged.
// W.O.P.R. first draft. Millimeters. Electronics are reference geometry only.
// Export part choices: assembly, gray-shell, white-text,
// base, section, fit-coupon, cup-main-shallow-left, cup-main-shallow-right,
// cup-tower, led-retainer, rear-mounts. check-clearances is a build-only probe.
part = "concealed";
electronics = true;
main_shallow_left = true;
$fn = 32;
L=279.4; W=210; H=165; wall=3; ink=0.8;
base_inset=3.3; base_bottom=3; base_thickness=6;
base_top=base_bottom+base_thickness;
main_rim=128; shallow_depth=38.1; shallow_floor=main_rim-shallow_depth;
divider=3;
board_x=20.955; board_z=17.780; clearance=0.3;
panels_per_side=6;
led_pitch=board_x+0.3; bank_x=95;
led_centers=[for(i=[0:panels_per_side-1]) bank_x+(i-(panels_per_side-1)/2)*led_pitch]; led_z=101;
bank_w=panels_per_side*board_x+(panels_per_side-1)*0.3;
tft_x=236; tft_z=124;
tft_w=65; tft_h=53; tft_thick=9.5;
tft_inset=2; rear_clearance=25.4;
bay_end=tft_inset+tft_thick+rear_clearance; // 36.9 from external face

module rounded_box(p,s,r=5) {
    translate(p) hull()
        for(x=[r,s[0]-r],y=[r,s[1]-r],z=[r,s[2]-r])
            translate([x,y,z]) sphere(r=r);
}
module outline() {
    // Extend the skirt into the old base footprint, then trim it flat at Z=0.
    rounded_box([0,0,-6],[L,W,90],6);
    rounded_box([0,5,72],[199,W-10,56],8);
    rounded_box([0,(W-47)/2,75],[204,47,62],10);
    rounded_box([190,0,6],[L-190,W,H-6],10);
}
module inside() {
    translate([3,3,-1]) cube([L-6,W-6,82]);
    rounded_box([3,8,72],[193,W-16,53],5);
    rounded_box([3,(W-41)/2,76],[198,41,58],7);
    rounded_box([193,3,70],[L-196,W-6,H-73],7);
}
// Coordinates on either long side, with local depth pointing inward.
module side(back=false) {
    if(back) translate([0,W,0]) mirror([0,1,0]) children();
    else children();
}
module lettering(back=false) {
    side(back) translate([tft_x,ink,72]) rotate([90,0,0]) {
        // Reverse local X on the far side so the outside reader sees correct text.
        scale([back?-1:1,1,1]) {
            linear_extrude(ink) text("W.O.P.R.",size=12,font="Liberation Sans:style=Bold",halign="center");
            translate([0,-9,0]) linear_extrude(ink)
                text("War Operation Plan Response",size=3.55,font="Liberation Sans:style=Bold",halign="center");
        }
    }
}
module white() { lettering(); lettering(true); }
// Small face-up print test using the production lettering at its actual scale.
module wording_test_white() {
    translate([45,16.2,3]) rotate([-90,0,0]) translate([-tft_x,0,-72]) lettering(false);
}
module wording_test_blank() {
    linear_extrude(3) offset(r=2) translate([2,2]) square([86,30]);
}
module wording_test_gray() {
    difference() { wording_test_blank(); wording_test_white(); }
}
module light_cuts() {
    for(back=[false,true]) side(back)
        translate([bank_x-bank_w/2-5.8,4,led_z-board_z/2-2.8])
            cube([bank_w+11.6,13,board_z+5.6]);
}
module light_mounts() {
    for(back=[false,true]) side(back) translate([bank_x,0,led_z])
        difference() {
            translate([-bank_w/2-6,5,-board_z/2-3]) cube([bank_w+12,4.6,board_z+6]);
            // A continuous front window and a full-size rear-loading PCB pocket.
            translate([-bank_w/2+0.8,4,-board_z/2+2]) cube([bank_w-1.6,5,board_z-4]);
            translate([-bank_w/2-clearance,8,-board_z/2-clearance]) cube([bank_w+2*clearance,5,board_z+2*clearance]);
            for(x=[-bank_w/2-3,bank_w/2+3],z=[-5,5])
                translate([x,6.5,z]) rotate([-90,0,0]) cylinder(h=4,d=1.6);
        }
}
module led_retainer() {
    // One removable frame per bank. All screw heads are inside the case.
    difference() {
        translate([-bank_w/2-6,9.6,-board_z/2-3]) cube([bank_w+12,2.4,board_z+6]);
        translate([-bank_w/2+1,9,-board_z/2+1]) cube([bank_w-2,4,board_z-2]);
        for(x=[-bank_w/2-3,bank_w/2+3],z=[-5,5])
            translate([x,9,z]) rotate([-90,0,0]) cylinder(h=4,d=2.2);
    }
}
module display_bay() {
    difference() {
        translate([tft_x-35,0,tft_z-29]) cube([70,bay_end,58]);
        // Front view: left edge +4.5 mm, right edge -1 mm, top edge -2 mm.
        // The bottom edge and the rear hardware seat remain fixed.
        translate([tft_x-27.8+4.5,-1,tft_z-20.8]) cube([55.6-4.5-1,6,41.6-2]);
        // Preserve glass clearance behind the 2 mm front lip.
        translate([tft_x-27.8,2,tft_z-20.8]) cube([55.6,3,41.6]);
        translate([tft_x-32.8,4,tft_z-26.8]) cube([65.6,bay_end,53.6]);
    }
    // Hidden front supports with blind pilots. Drive M2 screws from the rear.
    // Hole pitch 59.69 x 47.498 from manufacturer V2 Eagle file, rotated landscape.
    for(dx=[-29.845,29.845],dz=[-23.749,23.749])
        translate([tft_x+dx,0,tft_z+dz]) rotate([-90,0,0])
            cylinder(h=4,r=3.8);
}
module cup_cutouts() {
    translate([13.7,21.7,39.7]) cube([169.6,111.6,140]);
    translate([198.7,42.7,64.7]) cube([69.6,101.6,115]);
}
module pen_cup(tower=false,shallow_left=true) {
    if(!tower && !shallow_left) translate([197,0,0]) mirror([1,0,0]) pen_cup(false,true);
    else if(tower) union() {
        difference() {
            intersection() { outline(); translate([199,43,65]) cube([69,101,110]); }
            translate([202,46,68]) cube([63,95,110]);
        }
        intersection() {
            outline();
            union() {
                translate([232,46,68]) cube([divider,95,H-68]);
                translate([202,92,68]) cube([63,divider,H-68]);
            }
        }
    } else difference() {
        union() {
            // A level rim gives the shallow half an exact 38.1 mm depth.
            difference() {
                translate([14,22,40]) cube([169,111,main_rim-40]);
                translate([17,25,43]) cube([163,105,main_rim]);
            }
            translate([17,25,shallow_floor-wall]) cube([83,105,wall]);
            translate([97,25,43]) cube([divider,105,main_rim-43]);
            // Three transverse dividers make four shallow compartments.
            for(y=[49,76,103]) translate([17,y,shallow_floor])
                cube([80,divider,shallow_depth]);
            // Crossed dividers make four deep compartments in the other half.
            translate([138.5,25,43]) cube([divider,105,main_rim-43]);
            translate([100,76,43]) cube([80,divider,main_rim-43]);
        }
        // Keep the raised tray underside accessible for support removal.
        translate([17,25,39]) cube([80,105,4]);
    }
}
module cup_supports() {
    for(x=[20,166],back=[false,true]) side(back)
        translate([x,0,37]) cube([10,28,3]);
    for(x=[205,259]) {
        translate([x,0,62]) cube([8,49,3]);
        translate([x,140,62]) cube([8,15,3]);
    }
}
module door_grooves() {
    for(back=[false,true]) side(back) {
        for(x=[22,104,202]) {
            wide=x==202?65:70;
            translate([x,-0.1,18]) cube([wide,0.7,0.65]);
            translate([x,-0.1,18]) cube([0.65,0.7,39]);
            translate([x+wide-0.65,-0.1,18]) cube([0.65,0.7,39]);
            translate([x,-0.1,56.35]) cube([wide,0.7,0.65]);
            translate([x+wide/2,0,49]) rotate([-90,0,0]) cylinder(h=0.65,d=3.6);
        }
        // Shallow decorative strip defines the long light band.
        translate([16,4.8,89]) cube([166,0.7,0.6]);
        translate([16,4.8,112.4]) cube([166,0.7,0.6]);
    }
    for(z=[141:3:153]) translate([202,W-0.6,z]) cube([62,1,1]);
    // Rear cable access, low and clear of display keepout.
    translate([232,W-5,20]) cube([12,8,7]);
}
module base_bosses() {
    for(x=[12,128,151,L-12],back=[false,true]) side(back)
        difference() {
            translate([x-5,0,base_top]) cube([10,19,10]);
            translate([x,13,base_top-1]) cylinder(h=12,d=2.5);
        }
}
module gray() {
    difference() {
        union() {
            difference(){ outline(); inside(); light_cuts(); cup_cutouts();
                translate([tft_x-32.8,-1,tft_z-26.8]) cube([65.6,40,53.6]);
            }
            light_mounts(); display_bay(); base_bosses(); cup_supports();
        }
        white(); door_grooves();
        for(dx=[-29.845,29.845],dz=[-23.749,23.749])
            translate([tft_x+dx,1,tft_z+dz]) rotate([-90,0,0]) cylinder(h=4,d=1.8);
        translate([-1,-1,-7]) cube([L+2,W+2,7]);
    }
}
module base() {
    difference() {
        translate([base_inset,base_inset,base_bottom])
            linear_extrude(base_thickness) offset(r=3) translate([3,3])
                square([L-2*base_inset-6,W-2*base_inset-6]);
        for(x=[12,128,151,L-12],y=[13,W-13]) {
            translate([x,y,base_bottom-1]) cylinder(h=base_thickness+2,d=3.3);
        }
        // Bottom vent slots. No provision for high-power electronics in this draft.
        for(x=[35:10:115],y=[50,92]) translate([x,y,base_bottom-1]) cube([3,20,base_thickness+2]);
    }
}
module reference_parts() {
    for(back=[false,true]) side(back) for(cx=led_centers) {
        color([0.09,0.10,0.11]) translate([cx-board_x/2,8,led_z-board_z/2]) cube([board_x,1.6,board_z]);
        for(i=[0:9],j=[0:5])
            color((i*7+j*3)%5<2 ? [1,0.23,0.04] : [0.36,0.12,0.06])
                translate([cx-9+i*2,6.95,led_z-5+j*2]) cube([1,1.05,1]);
    }
    // Screen face inset 2 mm; hardware envelope extends another 9.5 mm inward.
    color([0.08,0.09,0.10]) translate([tft_x-32.5,4.01,tft_z-26.5]) cube([65,7.49,53]);
    color([0.06,0.1,0.12]) translate([tft_x-27.5,2,tft_z-20.5]) cube([55,2.01,41]);
    color([0.25,0.85,0.65]) translate([tft_x,1.98,tft_z]) rotate([90,0,0])
        linear_extrude(0.02) text("SHALL WE PLAY",size=2.7,font="Liberation Mono",halign="center");
    color([0.25,0.85,0.65]) translate([tft_x,1.98,tft_z-5]) rotate([90,0,0])
        linear_extrude(0.02) text("A GAME?",size=2.7,font="Liberation Mono",halign="center");
}
module assembly() {
    color([0.40,0.43,0.46]) gray();
    color([0.98,0.98,0.96]) white();
    color([0.31,0.34,0.37]) base();
    color([0.40,0.43,0.46]) {
        pen_cup(false,main_shallow_left); pen_cup(true);
        for(back=[false,true]) side(back) translate([bank_x,0,led_z]) led_retainer();
    }
    if(electronics) reference_parts();
}
module clearance_checks() {
    // A successful check exports only this 1 mm cube; any interference adds volume.
    translate([-20,-20,-20]) cube(1);
    intersection() {
        gray();
        union() {
            for(back=[false,true]) side(back) for(cx=led_centers)
                translate([cx-board_x/2,8.01,led_z-board_z/2]) cube([board_x,27,board_z]);
            translate([tft_x-32.5,4.01,tft_z-26.5]) cube([65,61,53]);
            translate([212.71,0.01,103.21]) cube([50.08,1.98,39.58]);
            translate([208.51,2.01,103.51]) cube([54.98,1.98,40.98]);
            // Cups must lift straight out after removing electronics fasteners.
            translate([14,22,40.01]) cube([169,111,140]);
            translate([199,43,65.01]) cube([69,101,115]);
        }
    }
    intersection() {
        union() { gray(); pen_cup(); pen_cup(true); }
        union() {
            translate([tft_x-32.5,11.51,tft_z-26.5]) cube([65,25.38,53]);
            for(y=[25,52,79,106]) translate([17.01,y+0.01,shallow_floor+0.01]) cube([79.98,23.98,100]);
            for(x=[100,141.5],y=[25,79]) translate([x+0.01,y+0.01,43.01]) cube([38.48,50.98,140]);
            for(x=[202,235],y=[46,95]) translate([x+0.01,y+0.01,68.01]) cube([29.98,45.98,110]);
        }
    }
    // The inset plate, its insertion path and the 3 mm screw-head space stay clear.
    // Exclude the intended zero-volume contact at the screw-boss seating face.
    intersection() {
        gray(); base();
        translate([-1,-1,base_bottom+0.01]) cube([L+2,W+2,base_thickness-0.02]);
    }
    intersection() {
        gray();
        translate([base_inset,base_inset,-1]) cube([L-2*base_inset,W-2*base_inset,base_top+0.99]);
    }
    intersection() {
        union() { gray(); base(); }
        for(x=[12,128,151,L-12],y=[13,W-13]) translate([x,y,0.01]) cylinder(h=2.98,d=6.4);
    }
    // Require solid dividers rather than merely checking that the cells are empty.
    difference() {
        union() {
            for(y=[49,76,103]) translate([17.1,y+0.1,shallow_floor+0.1]) cube([79.8,2.8,shallow_depth-0.2]);
            translate([97.1,25.1,43.1]) cube([2.8,104.8,main_rim-43.2]);
            translate([138.6,25.1,43.1]) cube([2.8,104.8,main_rim-43.2]);
            translate([100.1,76.1,43.1]) cube([79.8,2.8,main_rim-43.2]);
        }
        pen_cup();
    }
    difference() {
        union() {
            translate([232.1,46.1,68.1]) cube([2.8,94.8,96.7]);
            translate([202.1,92.1,68.1]) cube([62.8,2.8,96.7]);
        }
        pen_cup(true);
    }
    // Blind TFT screws must leave solid plastic over the front of every hole.
    difference() {
        union() for(dx=[-29.845,29.845],dz=[-23.749,23.749])
            translate([tft_x+dx-0.5,0.2,tft_z+dz-0.5]) cube([1,0.5,1]);
        gray();
    }
}
if(part=="assembly") assembly();
else if(part=="wording-gray") wording_test_gray();
else if(part=="wording-white") wording_test_white();
else if(part=="wording-solid") wording_test_blank();
else if(part=="wording-preview") {
    color([0.40,0.43,0.46]) wording_test_gray();
    color([0.98,0.98,0.96]) wording_test_white();
}
else if(part=="check-clearances") clearance_checks();
else if(part=="gray-shell") gray();
else if(part=="white-text") white();
else if(part=="base") base();
else if(part=="cup-main-shallow-left") color([0.40,0.43,0.46]) pen_cup(false,true);
else if(part=="cup-main-shallow-right") color([0.40,0.43,0.46]) pen_cup(false,false);
else if(part=="cup-tower") color([0.40,0.43,0.46]) pen_cup(true);
else if(part=="cup-plan-left") color([0.40,0.43,0.46]) projection(cut=true) translate([0,0,-127]) pen_cup(false,true);
else if(part=="cup-plan-right") color([0.40,0.43,0.46]) projection(cut=true) translate([0,0,-127]) pen_cup(false,false);
else if(part=="plan-section") color([0.40,0.43,0.46]) projection(cut=true) translate([0,0,-127]) assembly();
else if(part=="cup-main-section") color([0.40,0.43,0.46]) intersection(){pen_cup(false,main_shallow_left);translate([0,60,-1]) cube([L,0.5,H+2]);}
else if(part=="base-section") {
    color([0.40,0.43,0.46]) intersection(){gray();translate([11.75,-1,-1]) cube([0.5,33,29]);}
    color([0.72,0.74,0.77]) intersection(){base();translate([11.75,-1,-1]) cube([0.5,33,29]);}
}
else if(part=="led-retainer") rotate([90,0,0]) led_retainer();
else if(part=="rear-mounts") {
    color([0.4,0.43,0.46]) gray();
    color([0.98,0.98,0.96]) white();
    reference_parts();
    color([0.65,0.68,0.7]) for(back=[false,true]) side(back)
        translate([bank_x,0,led_z]) led_retainer();
}
else if(part=="section") color([0.40,0.43,0.46]) intersection(){ assembly(); translate([tft_x,-1,-1]) cube([0.5,W+2,H+2]); }
else if(part=="fit-coupon") color([0.40,0.43,0.46]) intersection(){ gray(); translate([tft_x-37,-1,tft_z-31]) cube([74,39,62]); }

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
module hatch_cut() { translate([9,15,116]) cube([178,W-30,70]); }
module lid_screws(d=3.3) { for(x=[15,181],y=[21,W-21]) translate([x,y,108]) cylinder(d=d,h=50); }
module robot_raw_shell(wheel_cuts=true, bottom_bosses=true) { difference() {
    union() {
        difference() { outline(); inside(); light_cuts();
            translate([tft_x-32.8,-1,tft_z-26.8]) cube([65.6,40,53.6]); }
        light_mounts(); display_bay(); if(bottom_bosses) base_bosses();
        // Main lid ledges attached to the existing side wall.
        for(x=[9,175],y=[5,W-25]) translate([x,y,107]) cube([12,20,9]);
    }
    white();
    translate([-1,W/2,55]) rotate([0,90,0]) cylinder(d=12.3,h=7); // filled by latching motor-power switch
    for(dx=[-29.845,29.845],dz=[-23.749,23.749]) translate([tft_x+dx,1,tft_z+dz]) rotate([-90,0,0]) cylinder(h=4,d=1.8);
    translate([-1,-1,-7]) cube([L+2,W+2,7]);
    // No pen apertures, cable slot, vents or exposed bottom openings.
    if(wheel_cuts) wheel_voids(2.4);
} }
module robot_shell() { difference() { robot_raw_shell(); hatch_cut(); lid_screws(2.5);
    // Floor wheel guards seat outside shell with a running assembly gap.
    pods() for(s=[-1,1]) translate([0,s*27,robot_axle]) axle_cylinder(37.9,37.8);
} }
module robot_lid() { difference() {
    union() {
        intersection() { robot_raw_shell(); translate([9.3,15.3,116.3]) cube([177.4,W-30.6,70]); }
        // Flat inner lid closes the hollow center below the original raised spine.
        translate([9.3,15.3,116.3]) cube([177.4,W-30.6,4]);
        intersection() { outline(); difference() { translate([9.3,15.3,119]) cube([177.4,W-30.6,12]); translate([12.3,18.3,118]) cube([171.4,W-36.6,15]); } }
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

hidden_wide=true;
hidden_xs=hidden_wide?[48,231]:[60,219];
hidden_ys=[52,W-52];
hidden_axle=18; lift=hidden_axle-robot_axle;
hidden_wheels=[for(x=hidden_xs,y=hidden_ys,s=(hidden_wide?[-1,1]:[y<W/2?-1:1])) [x,y+s*27,hidden_axle]];
tray_holes=[for(x=[104,176],y=[W/2-37.5,W/2+37.5]) [x,y]];
base_holes=concat([for(x=[106,139.7,173],y=[13,W-13]) [x,y]],[[13,W/2],[L-13,W/2]]);
module hidden_pods() { for(x=hidden_xs,y=hidden_ys) translate([x,y,lift]) children(); }
module hidden_wheel_voids(gap=0, insertion=false) { for(p=hidden_wheels){
    translate(p) axle_cylinder(31.5+gap,29+2*gap);
    if(insertion) translate([p[0]-31.5-gap,p[1]-14.5-gap,18]) cube([63+2*gap,29+2*gap,130]);
} }
function hood_front(p)=p[1]==25 || p[1]==W-79;
module wheel_hood(front=true){
    if(!front) mirror([0,1,0]) wheel_hood(true);
    else difference(){
        union(){
            intersection(){translate([0,0,18]) axle_cylinder(37.5,37);translate([-40,-20,18.3]) cube([80,40,40]);}
            for(x=[-35.5,35.5]) translate([x-3,-5,18.3]) cube([6,10,4]);
        }
        translate([0,0,18]) axle_cylinder(32.5,31);
        // Fit down over the unclamped cradle/can; caps are fitted afterward.
        translate([-15.3,15.2,17]) cube([30.6,40,70]);
        for(x=[-35.5,35.5]) translate([x,0,17]) cylinder(d=3.3,h=10);
    }
}
module hidden_hoods(){for(p=hidden_wheels) translate([p[0],p[1],0]) wheel_hood(hood_front(p));}
module hidden_bosses() { difference() {
    union() {
        for(x=[106,139.7,173],y=[0,W-19]) translate([x-5,y,9]) cube([10,19,10]);
        for(x=[0,L-19]) translate([x,W/2-5,9]) cube([19,10,10]);
    }
    for(p=base_holes) translate([p[0],p[1],8]) cylinder(d=2.5,h=12);
} }
module hidden_shell() { difference() {
    union(){robot_raw_shell(false,false);hidden_bosses();}
    hatch_cut();lid_screws(2.5);
} }
module hidden_cradle(){
    cradle();
    // Raised clamp posts must reach the floor and brace into the cradle.
    for(x=[-20,20]) translate([x-4,-6,-31.5]) cube([8,12,34.6]);
    translate([-24,-6,1]) cube([48,12,6]);
}
module hidden_floor() { difference() {
    union() {
        translate([base_inset,base_inset,3]) linear_extrude(6) offset(r=3) translate([3,3]) square([L-2*base_inset-6,W-2*base_inset-6]);
        // Closed wheel tubs; their only exterior opening is toward the ground.
        intersection(){
            for(p=hidden_wheels) translate(p) axle_cylinder(37.5,37);
            translate([0,0,3]) cube([L,W,15]);
        }
        hidden_pods() hidden_cradle();
        for(p=hidden_wheels,x=[-35.5,35.5]) translate([p[0]+x-3,p[1]-5,8.5]) cube([6,10,9.5]);
        for(y=[W/2-35,W/2+32]) translate([83,y,9]) cube([112,3,9]);
        for(x=[83,192]) translate([x,W/2-35,9]) cube([3,70,9]);
        for(x=[110,160],y=[W/2-40,W/2+36]) translate([x,y,9]) cube([12,6,8]);
        for(p=tray_holes) translate([p[0],p[1],9]) cylinder(d=10,h=58);
    }
    hidden_wheel_voids(1,true);hidden_pods() motor_void();
    // The fixed double shaft drops through these U-slots during top insertion.
    for(x=hidden_xs,y=hidden_ys) translate([x-3.5,y-18.5,18]) cube([7,37,70]);
    for(p=hidden_wheels,x=[-35.5,35.5]){
        translate([p[0]+x,p[1],8.5]) cylinder(d=2.5,h=11);
        translate([p[0]+x-3.3,p[1]-5.3,18]) cube([6.6,10.6,7]);
    }
    for(p=base_holes) translate([p[0],p[1],2]) cylinder(d=3.3,h=10);
    for(p=tray_holes) translate([p[0],p[1],55]) cylinder(d=2.5,h=15);
    for(x=[110,160],y=[W/2-41,W/2+35]) translate([x+2,y,11]) cube([8,8,3]);
} }
module hidden_tray() { difference() {
    translate([87,W/2-44,67.3]) cube([102,88,3]);
    for(p=tray_holes) translate([p[0],p[1],66]) cylinder(d=3.3,h=6);
    for(x=[102,126,150,174],y=[W/2-36,W/2-8,W/2+22]) translate([x,y,66]) cube([3,14,6]);
} }
module hidden_hardware() {
    hidden_pods(){
        color([.95,.67,.07]) translate([-11.2,-9.3,-36]) cube([22.4,18.6,38]);
        color([.55,.57,.59]) translate([-10,-11.2,2]) cube([20,22.4,32]);
        color([.8,.8,.8]) translate([0,0,robot_axle]) axle_cylinder(2.7,36.6);
    }
    for(p=hidden_wheels){
        color([.98,.40,.08]) translate(p) axle_cylinder(31.5,29);
        color([.82,.83,.80]) translate([p[0],p[1]+((p[1]==25 || p[1]==W-79)?-15:15),p[2]]) axle_cylinder(20,1);
    }
    color([.12,.15,.19]) translate([87,W/2-26.15,10]) cube([104,52.3,26]);
    color([.08,.40,.26]) translate([97,W/2-35,74]) cube([55,28,10]);
    color([.1,.35,.65]) for(x=[100,132]) translate([x,W/2+5,74]) cube([26,18,9]);
}
module hidden_assembly(exploded=false,interior=false){
    if(!interior){
        color([.40,.43,.46]) translate([0,0,exploded?100:0]) hidden_shell();
        color([.98,.98,.96]) translate([0,0,exploded?100:0]) white();
        color([.40,.43,.46]) translate([0,0,exploded?170:0]) robot_lid();
    }
    color([.31,.34,.37]) hidden_floor();
    color([.47,.50,.53]) hidden_hoods();
    color([.65,.68,.70]) translate([0,0,exploded||interior?60:0]) hidden_tray();
    color([.5,.53,.56]) hidden_pods() motor_cap();
    if(electronics){hidden_hardware();if(!exploded&&!interior) reference_parts();}
}
module hidden_checks(){
    assert(len(hidden_wheels)==(hidden_wide?8:4));
    assert(len(hidden_xs)*len(hidden_ys)==4);
    for(p=hidden_wheels) assert(p[1]-14.5>3 && p[1]+14.5<W-3);
    assert(hidden_axle-31.5==-13.5);
    translate([-100,-100,-100]) cube(1);
    intersection(){union(){hidden_shell();hidden_floor();hidden_hoods();robot_lid();hidden_tray();hidden_pods() motor_cap();} hidden_wheel_voids(.2);}
    intersection(){hidden_shell();robot_lid();}
    intersection(){hidden_floor();hidden_wheel_voids(.2,true);}
    intersection(){hidden_floor();for(x=hidden_xs,y=hidden_ys) union(){
        translate([x-3,y-18.4,18]) cube([6,36.8,130]);
        translate([x-11.2,y-9.3,4]) cube([22.4,18.6,140]);
        // Exclude the intentional motor shoulder contact at Z42.
        translate([x-10,y-11.2,42.01]) cube([20,22.4,110]);
    }}
    for(dz=[0,10,30,60,90]) intersection(){hidden_floor();translate([0,0,dz]) hidden_hoods();}
    intersection(){hidden_hoods();hidden_floor();}
    intersection(){hidden_hoods();union(){hidden_shell();hidden_tray();hidden_pods() motor_cap();}}
    intersection(){hidden_shell();hidden_floor();translate([-1,-1,9.01]) cube([L+2,W+2,180]);}
    intersection(){hidden_tray();union(){hidden_floor();hidden_pods() motor_cap();}}
    intersection(){union(){hidden_shell();hidden_floor();hidden_hoods();robot_lid();hidden_tray();hidden_pods() motor_cap();} translate([87,W/2-26.65,10]) cube([104.98,53.3,30]);}
    // All four shafts, including the unused inner shafts on the four-wheel model.
    intersection(){union(){hidden_shell();hidden_floor();hidden_tray();} hidden_pods() translate([0,0,robot_axle]) axle_cylinder(2.9,36.8);}
    // Preserve the original LED insertion and LCD glass/service space.
    intersection(){union(){hidden_shell();hidden_floor();hidden_tray();hidden_pods() motor_cap();}
        union(){
            for(back=[false,true]) side(back) for(cx=led_centers) translate([cx-board_x/2,8.01,led_z-board_z/2]) cube([board_x,27,board_z]);
            translate([tft_x-32.5,4.01,tft_z-26.5]) cube([65,32.88,53]);
        }
    }
}
if(part=="concealed") hidden_assembly();
else if(part=="concealed-exploded") hidden_assembly(true);
else if(part=="concealed-interior") hidden_assembly(false,true);
else if(part=="concealed-shell") hidden_shell();
else if(part=="concealed-floor") hidden_floor();
else if(part=="concealed-tray") hidden_tray();
else if(part=="concealed-check") hidden_checks();
else if(part=="concealed-pod-test") intersection(){hidden_floor();translate([hidden_xs[0]-38.8,3.3,0]) cube([77.6,96,86]);}

if(part=="wheel-hood-front") wheel_hood(true);
else if(part=="wheel-hood-rear") wheel_hood(false);
