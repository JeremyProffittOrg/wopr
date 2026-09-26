// W.O.P.R. first draft. Millimeters. Electronics are reference geometry only.
// Export part choices: assembly, gray-left, gray-right, white-right,
// base-left, base-right, splice, section, fit-coupon.
part = "assembly";
electronics = true;
$fn = 32;
L=279.4; W=155; H=165; split=140; wall=3; ink=0.8;
board_x=21; board_z=17.8; clearance=0.3;
led_centers=[37,79,121,163]; led_z=101;
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
    for(back=[false,true]) side(back) for(cx=led_centers) {
        // Full board aperture. The board drops onto ledges from the outside.
        translate([cx-board_x/2-clearance,3.8,led_z-board_z/2-clearance])
            cube([board_x+2*clearance,12,board_z+2*clearance]);
    }
}
module light_mounts() {
    for(back=[false,true]) side(back) for(cx=led_centers)
        difference() {
            translate([cx-board_x/2-2.3,5,led_z-board_z/2-2.3]) cube([board_x+4.6,7,board_z+4.6]);
            translate([cx-board_x/2-clearance,3,led_z-board_z/2-clearance]) cube([board_x+2*clearance,6.5,board_z+2*clearance]);
            // Rear opening leaves a 1 mm seat at depth 9.5 mm.
            translate([cx-board_x/2+1,9.49,led_z-board_z/2+1]) cube([board_x-2,5,board_z-2]);
        }
}
module display_bay() {
    difference() {
        translate([tft_x-35,0,tft_z-29]) cube([70,bay_end,58]);
        translate([tft_x-32.8,-1,tft_z-26.8]) cube([65.6,bay_end+2,53.6]);
    }
    // Four front support ears. Mount from inside using M2.5 bolts and nuts.
    // Hole pitch 59.69 x 47.498 from manufacturer V2 Eagle file, rotated landscape.
    for(dx=[-29.845,29.845],dz=[-23.749,23.749])
        translate([tft_x+dx,2,tft_z+dz]) rotate([-90,0,0])
            difference(){ cylinder(h=2,r=3.8); translate([0,0,-1]) cylinder(h=4,d=2.7); }
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
            difference(){ outline(); inside(); light_cuts();
                translate([tft_x-32.8,-1,tft_z-26.8]) cube([65.6,40,53.6]);
            }
            light_mounts(); display_bay(); base_bosses();
        }
        white(); door_grooves();
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
        color([0.09,0.10,0.11]) translate([cx-10.5,7.9,led_z-8.9]) cube([21,1.6,17.8]);
        for(i=[0:9],j=[0:5])
            color((i*7+j*3)%5<2 ? [1,0.23,0.04] : [0.36,0.12,0.06])
                translate([cx-9+i*2,6.85,led_z-5+j*2]) cube([1,1.05,1]);
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
    if(electronics) reference_parts();
}
if(part=="assembly") assembly();
else if(part=="gray-left") half(false) gray();
else if(part=="gray-right") half(true) gray();
else if(part=="white-right") half(true) white();
else if(part=="base-left") half(false) base();
else if(part=="base-right") half(true) base();
else if(part=="splice") cube([25,12,3]);
else if(part=="section") color([0.40,0.43,0.46]) intersection(){ assembly(); translate([tft_x,-1,-1]) cube([0.5,W+2,H+2]); }
else if(part=="fit-coupon") color([0.40,0.43,0.46]) intersection(){ gray(); translate([tft_x-37,-1,tft_z-31]) cube([74,39,62]); }
