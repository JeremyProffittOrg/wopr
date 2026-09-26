// W.O.P.R. first draft. Millimeters. Electronics are reference geometry only.
// Export part choices: assembly, gray-left, gray-right, white-right,
// base-left, base-right, splice, section, fit-coupon, cup-left, cup-right,
// cup-tower, led-retainer, rear-mounts. check-clearances is a build-only probe.
part = "assembly";
electronics = true;
$fn = 32;
L=279.4; W=155; H=165; split=140; wall=3; ink=0.8;
board_x=20.955; board_z=17.780; clearance=0.3;
led_pitch=board_x+0.3; bank_x=92;
led_centers=[for(i=[0:3]) bank_x+(i-1.5)*led_pitch]; led_z=101;
bank_w=4*board_x+3*0.3;
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
    rounded_box([0,0,0],[L,W,84],6);
    rounded_box([0,5,72],[199,W-10,56],8);
    rounded_box([0,54,75],[204,47,62],10);
    rounded_box([190,0,6],[L-190,W,H-6],10);
}
module inside() {
    translate([3,3,-1]) cube([L-6,W-6,82]);
    rounded_box([3,8,72],[193,W-16,53],5);
    rounded_box([3,57,76],[198,41,58],7);
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
        translate([tft_x-27.8,-1,tft_z-20.8]) cube([55.6,6,41.6]);
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
module pen_cup(tower=false) {
    difference() {
        intersection() {
            outline();
            if(tower) translate([199,43,65]) cube([69,101,110]);
            else translate([14,22,40]) cube([169,111,110]);
        }
        if(tower) translate([202,46,68]) cube([63,95,110]);
        else translate([17,25,43]) cube([163,105,140]);
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
            translate([x-5,0,6]) cube([10,19,10]);
            translate([x,13,5]) cylinder(h=12,d=2.5);
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
        translate([-1,-1,-1]) cube([L+2,W+2,7]);
    }
}
module base() {
    difference() {
        linear_extrude(6) offset(r=5) translate([5,5]) square([L-10,W-10]);
        for(x=[12,128,151,L-12],y=[13,W-13]) {
            translate([x,y,-1]) cylinder(h=8,d=3.3);
            translate([x,y,-0.1]) cylinder(h=2.1,d=6.4);
        }
        // Bottom vent slots. No provision for high-power electronics in this draft.
        for(x=[35:10:115],y=[50,92]) translate([x,y,-1]) cube([3,20,8]);
    }
}
module half(right=false) {
    intersection() {
        children();
        translate([right?split:-1,-1,-2]) cube([right?L-split+2:split+1,W+2,H+5]);
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
        pen_cup(); pen_cup(true);
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
            // Cups must lift straight out after removing electronics fasteners.
            translate([14,22,40.01]) cube([169,111,140]);
            translate([199,43,65.01]) cube([69,101,115]);
        }
    }
    intersection() {
        union() { gray(); pen_cup(); pen_cup(true); }
        union() {
            translate([tft_x-32.5,11.51,tft_z-26.5]) cube([65,25.38,53]);
            translate([17.01,25.01,43.01]) cube([162.98,104.98,140]);
            translate([202.01,46.01,68.01]) cube([62.98,94.98,110]);
        }
    }
    // Blind TFT screws must leave solid plastic over the front of every hole.
    difference() {
        union() for(dx=[-29.845,29.845],dz=[-23.749,23.749])
            translate([tft_x+dx-0.5,0.2,tft_z+dz-0.5]) cube([1,0.5,1]);
        gray();
    }
}
if(part=="assembly") assembly();
else if(part=="check-clearances") clearance_checks();
else if(part=="gray-left") half(false) gray();
else if(part=="gray-right") half(true) gray();
else if(part=="white-right") half(true) white();
else if(part=="base-left") half(false) base();
else if(part=="base-right") half(true) base();
else if(part=="splice") cube([25,12,3]);
else if(part=="cup-left") half(false) pen_cup();
else if(part=="cup-right") half(true) pen_cup();
else if(part=="cup-tower") pen_cup(true);
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
