// W.O.P.R. first draft. Millimeters. Electronics are reference geometry only.
// Export part choices: assembly, gray-shell, white-text,
// base, section, fit-coupon, cup-main-shallow-left, cup-main-shallow-right,
// cup-tower, led-retainer, rear-mounts. check-clearances is a build-only probe.
part = "assembly";
electronics = true;
main_shallow_left = true;
$fn = 32;
L=279.4; W=155; H=165; wall=3; ink=0.8;
base_inset=3.3; base_bottom=3; base_thickness=6;
base_top=base_bottom+base_thickness;
main_rim=128; shallow_depth=38.1; shallow_floor=main_rim-shallow_depth;
divider=3;
board_x=20.955; board_z=17.780; clearance=0.3;
panels_per_side=7;
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
