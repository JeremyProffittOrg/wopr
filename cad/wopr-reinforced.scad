// Current reinforced editions. Dimensions in mm.
// Use -D part="r-assembly", -D edition="four" (seven,six,exposed,four,wide).
include <wopr.scad>
edition="four";
r_robot=edition!="seven" && edition!="six";
r_exposed=edition=="exposed"; r_wide=edition=="wide";
r_wall=5; r_base=10; r_bottom=r_exposed?-10:3; r_top=r_bottom+r_base;
r_axle=r_exposed?-22:18; r_mbottom=r_axle-14.4; r_mtop=r_axle+56;
r_tire_radius=31.5+8; // Enlarged design envelope; physical Adafruit tire remains 63mm.
r_well_radius=r_tire_radius+1;
r_well_peak=r_well_radius+6.5;
r_motor_stop=r_axle+56.4;
r_cap_top=min(r_mbottom-.31,r_bottom-.01);
r_shell_bottom=r_robot?r_bottom-3:0;
r_sensor_z=r_bottom+14;
r_xs=edition=="four"?[54,L-54]:[51.3,L-51.3];
r_ys=[59.3,W-59.3];
r_wheels=[for(x=r_xs,y=r_ys,s=(edition=="four"?[y<W/2?-1:1]:[-1,1])) [x,y+s*27,r_axle]];
r_holes=[for(x=[104,128,151,175],y=[15,W-15]) [x,y]];
r_tray_holes=[for(x=[103,177],y=[W/2-37.5,W/2+37.5]) [x,y]];
module r_inside(){
    rounded_box([5,5,-6],[L-10,W-10,85],1);
    rounded_box([5,10,72],[189,W-20,51],3);
    rounded_box([5,(W-37)/2,76],[194,37,56],5);
    rounded_box([195,5,70],[L-200,W-10,H-75],5);
}
module r_lights(){
    for(back=[false,true]) side(back) translate([bank_x,0,led_z]) difference(){
        translate([-bank_w/2-10,5,-board_z/2-5.3]) cube([bank_w+20,6.6,board_z+10.6]);
        translate([-bank_w/2+.8,4,-board_z/2+2]) cube([bank_w-1.6,7,board_z-4]);
        translate([-bank_w/2-.3,10,-board_z/2-.3]) cube([bank_w+.6,4,board_z+.6]);
        for(x=[-bank_w/2-5.8,bank_w/2+5.8],z=[-5,5]) translate([x,6.5,z]) rotate([-90,0,0]) cylinder(d=1.6,h=6);
    }
}
module r_retainer(){difference(){
    translate([-bank_w/2-10,11.6,-board_z/2-5.3]) cube([bank_w+20,5,board_z+10.6]);
    translate([-bank_w/2+1,11,-board_z/2+1]) cube([bank_w-2,7,board_z-2]);
    for(x=[-bank_w/2-5.8,bank_w/2+5.8],z=[-5,5]) translate([x,11,z]) rotate([-90,0,0]) cylinder(d=2.2,h=7);
}}
module r_display(){difference(){
    union(){
        translate([tft_x-37.8,0,tft_z-31.8]) cube([75.6,39.9,63.6]);
        for(dx=[-29.845,29.845],dz=[-23.749,23.749]) translate([tft_x+dx,0,tft_z+dz]) rotate([-90,0,0]) cylinder(d=12,h=7);
    }
    translate([212.7,-1,103.2]) cube([50.1,7,39.6]);
    translate([208.2,5,103.2]) cube([55.6,3,41.6]);
    translate([tft_x-32.8,7,tft_z-26.8]) cube([65.6,35,53.6]);
    for(dx=[-29.845,29.845],dz=[-23.749,23.749]) translate([tft_x+dx,2,tft_z+dz]) rotate([-90,0,0]) cylinder(d=1.8,h=7);
}}
module r_bosses(){difference(){
    union(){
        for(x=[104,128,151,175],y=[0,W-22]) translate([x-6.5,y,r_top]) cube([13,22,15]);
        difference(){translate([0,0,r_top]) cube([L,W,5]);translate([10,10,r_top-1]) cube([L-20,W-20,7]);}
    }
    for(p=r_holes) translate([p[0],p[1],r_top-.1]) cylinder(d=2.5,h=12);
}}
module r_hatch(){translate([9,15,116]) cube([178,W-30,70]);}
module r_lid_holes(d=3.3){for(x=[16,180],y=[23,W-23]) translate([x,y,105]) cylinder(d=d,h=50);}
module r_cup_cuts(){
    translate([15,21.7,40]) cube([167,111.6,150]);
    translate([205,45,65]) cube([59,95,115]);
}
module r_cup_supports(){
    for(x=[25,160],y=[0,W-27]) translate([x,y,35]) cube([12,27,5]);
    for(x=[212,251]){translate([x,0,60]) cube([10,50.3,5]);translate([x,134.7,60]) cube([10,W-134.7,5]);}
}
module r_white(){intersection(){white();outline();}}
// Adafruit3967:25.4x17.78mm PCB,20.32x12.70mm mounting pitch, four2.5mm holes.
// Local coordinates: horizontal X, inward depth Y, vertical Z. Front=low X end.
module r_sensor_sites(){
    for(y=r_ys){
        translate([5.35,y,r_sensor_z]) multmatrix([[0,1,0,0],[1,0,0,0],[0,0,1,0],[0,0,0,1]]) children();
        translate([L-5.35,y,r_sensor_z]) rotate([0,0,90]) children();
    }
    for(x=r_xs,back=[false,true]) side(back) translate([x,5.35,r_sensor_z]) children();
}
module r_sensor_carriers(clear=0){
    r_sensor_sites() translate([-11.2-clear,-clear,-14-clear]) cube([22.4+2*clear,5+2*clear,30+2*clear]);
}
module r_sensor_windows(d=10,depth=13){r_sensor_sites()
    translate([0,-6.5,0]) rotate([-90,0,0]) cylinder(d=d,h=depth);
}
module r_sensor_holes(){
    r_sensor_windows();
    r_sensor_sites() rotate([0,90,0]) for(x=[-10.16,10.16],z=[-6.35,6.35])
        translate([x,1,z]) rotate([-90,0,0]) cylinder(d=1.6,h=2.6);
}
module r_sensor_space(clear=0){r_sensor_sites() rotate([0,90,0]){
    translate([-13-clear,3.55-clear,-9.2-clear]) cube([26+2*clear,1.9+2*clear,18.4+2*clear]);
    translate([-2-clear,1.7-clear,-3-clear]) cube([4+2*clear,1.8+2*clear,6+2*clear]);
    for(s=[-1,1]) scale([s,1,1]) translate([8-clear,.6-clear,-3.1-clear]) cube([15+2*clear,4.8+2*clear,6.2+2*clear]);
}}
// End LEDs retain their existing body positions when the ToF boards move.
module r_end_led_sites(){for(y=[40,W-40]){
    translate([0,y,44]) multmatrix([[0,1,0,0],[1,0,0,0],[0,0,1,0],[0,0,0,1]]) children();
    translate([L,y,44]) rotate([0,0,90]) children();
}}
module r_end_led_holes(){r_end_led_sites() translate([0,-1,0]) rotate([-90,0,0]) cylinder(d=8,h=12);}
module r_sensor_led_space(clear=0){r_end_led_sites() translate([0,5.05-clear,0]) rotate([-90,0,0]) cylinder(d=9+2*clear,h=8+2*clear);}
module r_raw(){difference(){
    union(){
        difference(){outline();r_inside();
            if(r_robot && r_shell_bottom<0) translate([-1,-1,-100]) cube([L+2,W+2,102]);
            for(back=[false,true]) side(back) translate([bank_x-bank_w/2-10,4,led_z-board_z/2-5.3]) cube([bank_w+20,20,board_z+10.6]);
            translate([tft_x-32.8,-1,tft_z-26.8]) cube([65.6,42,53.6]);
        }
        r_lights();r_display();r_bosses();
        if(r_robot && r_shell_bottom<0) difference(){
            translate([0,0,r_shell_bottom]) cube([L,W,3-r_shell_bottom]);
            translate([5,5,r_shell_bottom-1]) cube([L-10,W-10,5-r_shell_bottom]);
        }
        // Keep five millimeters of gray backing beneath the recessed lettering.
        for(back=[false,true]) side(back) translate([199,4.5,54]) cube([76,1.3,31]);
        if(r_robot) for(x=[9,173],y=[5,W-30]) translate([x,y,106]) cube([14,25,10]);
        else {r_cup_supports();
            for(back=[false,true]) side(back) translate([20,4.5,16]) cube([250,1.2,43]);
            side(true) translate([200,4.5,139]) cube([66,1.2,16]);
        }
    }
    if(r_robot){r_sensor_windows();r_end_led_holes();}
    r_white();translate([-1,-1,-100]) cube([L+2,W+2,100+r_shell_bottom]);
    if(r_robot) translate([-1,W/2,55]) rotate([0,90,0]) cylinder(d=12.3,h=8);
    else {
        intersection(){door_grooves();union(){translate([-1,-1,0]) cube([L+2,W+2,60]);translate([190,W-2,138]) cube([90,4,20]);}}
        translate([232,W-8,20]) cube([12,10,7]);
    }
}}
module r_shell(){difference(){r_raw();
    if(r_robot){r_hatch();r_lid_holes(2.5);

    }
    else r_cup_cuts();
    if(r_robot){intersection(){r_well_outer(.3);translate([-50,5,-100])cube([400,W-10,300]);}r_well_led_bosses(.3);r_sensor_carriers(.3);}
}}
module r_lid(){difference(){
    intersection(){outline();translate([9.3,15.3,116.3]) cube([177.4,W-30.6,70]);}
    intersection(){r_inside();translate([14.3,20.3,121.3]) cube([167.4,W-40.6,80]);}
    r_lid_holes();
}}
module r_cup(tower=false,reverse=false){
    if(reverse) translate([197,0,0]) mirror([1,0,0]) r_cup(false,false);
    else if(tower) difference(){
        translate([205.3,45.3,65]) cube([58.4,94.4,100]);
        for(x=[210.3,237],y=[50.3,95]) translate([x,y,70]) cube([21.7,39.7,100]);
    }else difference(){
        translate([15.3,22,40]) cube([166.4,111,88]);
        for(y=[27,53.5,80,106.5]) translate([20.3,y,89.9]) cube([75.7,21.5,100]);
        for(x=[101,141.35],y=[27,80]) translate([x,y,45]) cube([35.35,48,100]);
        // Taper the underside of the raised floor at 45 degrees; bridge only25.7mm.
        hull(){
            translate([20.3,27,39]) cube([75.7,101,20.9]);
            translate([45.3,52,84.8]) cube([25.7,51,.1]);
        }
    }
}
module r_axc(r,h){rotate([90,0,0]) cylinder(r=r,h=h,center=true,$fn=64);}
module r_wheel_space(gap=0,up=false){for(p=r_wheels){translate(p) r_axc(r_tire_radius+gap,29+2*gap);if(up) translate([p[0]-r_tire_radius-gap,p[1]-14.5-gap,-100]) cube([2*(r_tire_radius+gap),29+2*gap,250]);}}
module r_pods(){for(x=r_xs,y=r_ys) translate([x,y,0]) children();}
module r_motor_mount(zip_ties=false){difference(){union(){
    // Closed ten-millimeter top stop; the bare motor rises through the open bottom.
    translate([-16.7,-11.5,r_motor_stop]) cube([33.4,23,10]);
    for(s=[-1,1]) scale([s,1,1]) {
        translate([11.7,-11.5,r_mbottom-.3]) cube([5,23,(zip_ties?r_axle+24:r_motor_stop+10)-(r_mbottom-.3)]);
        if(zip_ties) translate([0,5,r_axle]) rotate([90,0,0]) linear_extrude(10)
            polygon([[11.7,24],[16.7,24],[23.5,30.8],[23.5,66.4],[11.7,66.4]]);
    }
    for(x=[-22,22]) translate([x-6.5,-6.5,r_mbottom-.3]) cube([13,13,(zip_ties?r_axle+29:r_motor_stop+10)-(r_mbottom-.3)]);
    for(z=(zip_ties?[r_mbottom+5]:[r_mbottom+5,r_axle+42])) for(x=[-24,16]) translate([x,-6,z]) cube([8,12,5]);
}
    translate([-11.7,-11.7,-120]) cube([23.4,23.4,r_motor_stop+120]);
}}
// Front-to-back tunnels stay outside the motor, with >=5mm side walls.
module r_zip_channels(){for(x=[-17.6,17.6],z=[r_axle+44,r_axle+54])
    translate([x-.9,-6,z-2.3]) cube([1.8,12,4.6]);
}
// Complete 3.6 x 1.2mm belt envelope, including front/rear spans and lock heads.
// The bands surround the motor and both supports; no span crosses the motor.
module r_zip_loops(clear=0){for(z=[r_axle+44,r_axle+54]){
    translate([0,0,z-1.8-clear]) linear_extrude(3.6+2*clear) difference(){
        offset(delta=1.2+clear) polygon([[-10.2,-11.4],[10.2,-11.4],[17,-5],[17,5],[10.2,11.4],[-10.2,11.4],[-17,5],[-17,-5]]);
        offset(delta=-clear) polygon([[-10.2,-11.4],[10.2,-11.4],[17,-5],[17,5],[10.2,11.4],[-10.2,11.4],[-17,5],[-17,-5]]);
    }
    translate([-3-clear,-18.6-clear,z-2.5-clear]) cube([6+2*clear,6+2*clear,5+2*clear]);
}}
// Third tie surrounds the top stop and the bottom of the gearbox.
module r_top_tie(){
    translate([4.75,0,0]) rotate([90,0,90]) linear_extrude(2.5) difference(){
        translate([-12.25,r_mbottom-1.2]) square([24.5,r_motor_stop+11.2-(r_mbottom-1.2)]);
        translate([-11.25,r_mbottom-.2]) square([22.5,r_motor_stop+10.2-(r_mbottom-.2)]);
    }
    translate([3.75,-2.25,r_motor_stop+11.2]) cube([4.5,4.5,3.5]);
}
module r_top_tie_channels(){for(s=[-1,1]) scale([1,s,1])
    translate([4.25,10.9,-120]) cube([3.5,1.8,r_motor_stop+130.1]);
}
module r_motor_ties(){for(x=r_xs,y=r_ys) translate([x,y,0]) scale([1,y<W/2?1:-1,1]){r_zip_loops();r_top_tie();}}
module r_motor_hardware(){
    color([.95,.67,.07]) translate([-11.2,-9.3,r_axle-14]) cube([22.4,18.6,38]);
    color([.55,.57,.59]) translate([-10,-11.2,r_axle+24]) cube([20,22.4,32]);
    color([.8,.8,.8]) translate([0,0,r_axle]) r_axc(2.7,36.6);
}
module r_cap(){difference(){
    translate([-33,-10,r_cap_top-5]) cube([66,20,5]);
    for(x=[-22,22]) translate([x,0,r_cap_top-6]) cylinder(d=3.3,h=7);
}}
// Each outer well includes 6.5mm axial fitting travel. The two inner tires
// share one arched well, so no thin divider obstructs installation.
r_service=6.5;
r_well_ranges=concat([[r_ys[0]-49,r_ys[0]-11.5],[r_ys[1]+11.5,r_ys[1]+49]],edition=="four"?[]:[[r_ys[0]+11.5,r_ys[1]-11.5]]);
// Circumscribed 45-degree roof with a short central bridge instead of a round ceiling.
module r_well_profile(){
    r=r_well_radius; shoulder=r*(sqrt(2)-1); crown=r*sqrt(2)-r_well_peak;
    polygon([[-r,-140],[r,-140],[r,shoulder],[crown,r_well_peak],[-crown,r_well_peak],[-r,shoulder]]);
}
module r_well_prism(length,skin=0){rotate([90,0,0]) linear_extrude(length,center=true) offset(delta=skin) r_well_profile();}
module r_well_outer(clear=0){
    intersection(){
        union() for(x=r_xs,range=r_well_ranges){
            translate([x,(range[0]+range[1])/2,r_axle]) r_well_prism(range[1]-range[0]+10+2*clear,5+clear);
        }
        translate([-50,-60,r_bottom-clear]) cube([400,W+120,150]);
    }
}
module r_well_void(){for(x=r_xs,range=r_well_ranges){
    translate([x,(range[0]+range[1])/2,r_axle]) r_well_prism(range[1]-range[0]);
}}
module r_motor_void(){r_pods(){
    translate([-11.7,-11.7,-120]) cube([23.4,23.4,r_motor_stop+120]);
    // Inverted U-slots admit the fixed double-ended shaft from below.
    translate([-3.5,-18.6,-120]) cube([7,37.2,r_axle+3.5+120]);
}}
module r_motor_insert(){r_pods(){
    translate([-11.3,-9.4,-120]) cube([22.6,18.8,r_axle+24.2+120]);
    translate([-10.1,-11.3,-120]) cube([20.2,22.6,r_axle+56.2+120]);
    translate([-2.8,-18.4,-120]) cube([5.6,36.8,r_axle+2.8+120]);
}}
module r_wheel_install(){for(x=r_xs,y=r_ys,side=(edition=="four"?[y<W/2?-1:1]:[-1,1])){
    cy=y+side*27;sy=cy+side*r_service;
    // First raise the tire clear of the shaft, then press it axially onto it.
    hull(){translate([x,sy,r_axle]) r_axc(r_tire_radius+.2,29.4);translate([x,sy,r_axle-100]) r_axc(r_tire_radius+.2,29.4);}
    hull(){translate([x,sy,r_axle]) r_axc(r_tire_radius+.2,29.4);translate([x,cy,r_axle]) r_axc(r_tire_radius+.2,29.4);}
}}
// Tie-mounted tray and two level battery shelves over shared inner wheel wells.
r_shelf_depth=(r_ys[1]-r_ys[0]-35)*.8;
r_bottom_leds=concat([for(x=[106,140,174],y=[27,W-27]) [x,y]], [for(x=[112,130,148,166],y=[W/2-16,W/2+16]) [x,y]]);
module r_shelves(){if(r_robot && edition!="four") for(x=r_xs)
    translate([x-28,W/2-r_shelf_depth/2,r_axle+24]) cube([56,r_shelf_depth,72.3-r_axle-24]);
}
// Solid blocks retain two horizontal tie tunnels below a five-millimeter top skin.
module r_shelf_slots(){if(edition!="four") for(x=r_xs,dx=[-12,12])
    translate([x+dx-2.3,W/2-r_shelf_depth/2-1,65.5]) cube([4.6,r_shelf_depth+2,1.8]);
}
module r_shelf_ties(clear=0){if(edition!="four") for(x=r_xs,dx=[-12,12]){
    translate([x+dx-1.8-clear,W/2,0]) rotate([90,0,90]) linear_extrude(3.6+2*clear) difference(){
        offset(delta=1.2+clear) polygon([[-r_shelf_depth/2-.3,67],[r_shelf_depth/2+.3,67],[r_shelf_depth/2+.3,72.4],[r_shelf_depth/2-1.8,112.7],[-r_shelf_depth/2+1.8,112.7],[-r_shelf_depth/2-.3,72.4]]);
        offset(delta=-clear) polygon([[-r_shelf_depth/2-.3,67],[r_shelf_depth/2+.3,67],[r_shelf_depth/2+.3,72.4],[r_shelf_depth/2-1.8,112.7],[-r_shelf_depth/2+1.8,112.7],[-r_shelf_depth/2-.3,72.4]]);
    }
    translate([x+dx-3-clear,W/2+r_shelf_depth/2+.2-clear,90-clear]) cube([6+2*clear,6+2*clear,5+2*clear]);
}}
module r_tray_tie_channels(){for(p=r_tray_holes)
    translate([p[0]-8,p[1]-2.3,60.3]) cube([16,4.6,1.8]);
}
module r_center_battery_straps(){for(x=[121,157])
    translate([x-5,W/2,0]) rotate([90,0,90]) linear_extrude(10) difference(){
        translate([-54.5,r_bottom-1.2]) square([109,r_top+35.3-r_bottom+1.2]);
        translate([-53.5,r_bottom-.2]) square([107,r_top+34.3-r_bottom+.2]);
    }
}
module r_bottom_lens_space(){for(p=r_bottom_leds)translate([p[0],p[1],r_bottom-3])cylinder(d=5.2,h=r_base+3.1);}
module r_tray_ties(){for(p=r_tray_holes){
    translate([p[0],p[1]+1.8,0]) rotate([90,0,0]) linear_extrude(3.6) difference(){
        translate([-8.6,60.6]) square([17.2,13.1]);
        translate([-7.4,61.8]) square([14.8,10.7]);
    }
    translate([p[0]-3,p[1]-3,73.7]) cube([6,6,5]);
}}
module r_well_led_positions(){for(p=r_wheels,dx=[-18,18]) if(p[1]<r_ys[0] || p[1]>r_ys[1]){
    y=p[1]<r_ys[0]?p[1]-12:p[1]>r_ys[1]?p[1]+12:p[1];
    translate([p[0]+dx,y,0]) children();
}}
r_led_boss_top=r_axle+min(r_well_peak,r_well_radius*sqrt(2)-18)+10;
module r_well_led_bosses(clear=0){r_well_led_positions()
    translate([0,0,r_axle+25-clear]) cylinder(d=10+2*clear,h=r_led_boss_top-r_axle-25+2*clear);
}
module r_led_holes(){
    for(p=r_bottom_leds) translate([p[0],p[1],r_bottom-1]) cylinder(d=5,h=r_base+2);
    r_well_led_positions(){
        translate([0,0,r_axle+19]) cylinder(d=5,h=r_led_boss_top-r_axle-18);
        translate([0,0,r_led_boss_top-1]) cylinder(d=6,h=2);
    }
}
module r_led_wire_space(){
    for(p=r_bottom_leds) translate([p[0],p[1],r_top+.1]) cylinder(d=6,h=7);
    r_well_led_positions() translate([0,0,r_led_boss_top+.1]) cylinder(d=6,h=7);
}
module r_shelf_pack_space(){if(edition!="four") for(x=r_xs)
    translate([x-27,W/2-r_shelf_depth/2+2,72.5]) cube([54,r_shelf_depth-4,40]);
}
module r_frame(zip_ties=false){difference(){union(){
    translate([5.3,r_robot?5.2:5.3,r_bottom]) linear_extrude(r_base) offset(r=2) translate([2,2]) square([L-14.6,W-(r_robot?14.4:14.6)]);
    if(r_robot){
        r_well_outer();r_well_led_bosses();r_shelves();r_pods() r_motor_mount(zip_ties);r_sensor_carriers();
        for(x=[120,159]) translate([x-3,W/2-52,r_top]) cube([6,104,8]);
        for(p=r_tray_holes) translate([p[0],p[1],r_top]) cylinder(d=13,h=67.3-r_top);

    }
}
    for(p=r_holes) translate([p[0],p[1],r_bottom-1]) cylinder(d=3.3,h=r_base+2);
    if(r_robot){
        r_well_void();r_motor_void();
        if(!zip_ties) r_pods() for(x=[-22,22]) translate([x,0,r_cap_top-.1]) cylinder(d=2.5,h=12);
        r_sensor_space(.05);r_sensor_led_space(.05);r_sensor_holes();
        if(zip_ties){
            r_pods(){r_zip_channels();r_top_tie_channels();}
            for(x=r_xs,y=r_ys) translate([x,y,0]) scale([1,y<W/2?1:-1,1]) r_zip_loops(.3);
        }
        r_tray_tie_channels();r_shelf_slots();r_shelf_ties(.35);r_led_holes();
        for(x=[121,157],y=[W/2-54,W/2+54]) translate([x-5.3,y-1.2,r_bottom-1]) cube([10.6,2.4,r_base+2]);
    }
}}
module r_tray(){difference(){translate([92,W/2-44,67.3]) cube([98,88,5]);
    for(p=r_tray_holes,dx=[-8,8]) translate([p[0]+dx-.9,p[1]-2.3,66]) cube([1.8,4.6,8]);
    for(x=[111,139,167],y=[W/2-28,W/2+14]) translate([x,y,66]) cube([3,14,8]);
}}
module r_hardware(){
    for(back=[false,true]) side(back) for(cx=led_centers){
        color([.08,.09,.10]) translate([cx-board_x/2,10,led_z-board_z/2]) cube([board_x,1.6,board_z]);
        for(i=[0:9],j=[0:5]) color([1,.23,.04]) translate([cx-9+i*2,8.95,led_z-5+j*2]) cube([1,1.05,1]);
    }
    color([.07,.12,.14]) translate([208.5,5,103.5]) cube([55,2,41]);
    if(r_robot){
        r_pods() r_motor_hardware();
        for(p=r_wheels) color([.98,.4,.08]) translate(p) r_axc(31.5,29);
        color([.12,.15,.19]) translate([113.55,W/2-52,r_top+8.1]) cube([52.3,104,26]);
        color([.08,.4,.26]) translate([97,W/2-34,77.3]) cube([55,28,10]);
        for(x=[100,133]) color([.1,.35,.65]) translate([x,W/2+5,77.3]) cube([26,18,9]);
    }
}
module r_assembly(explode=false,zip_ties=false){
    color([.40,.43,.46]) translate([0,0,explode?100:0]) r_shell();
    color([.98,.98,.96]) translate([0,0,explode?100:0]) r_white();
    color([.31,.34,.37]) r_frame(zip_ties);
    if(r_robot){
        color([.40,.43,.46]) translate([0,0,explode?170:0]) r_lid();
        if(!zip_ties) color([.50,.53,.56]) r_pods() r_cap();
        else if(electronics) color([.05,.65,.9]) r_motor_ties();
        color([.65,.68,.70]) translate([0,0,explode?60:0]) r_tray();
    }else color([.4,.43,.46]){r_cup();r_cup(true);}
    if(electronics){r_hardware();if(r_robot)color([.05,.65,.9])r_tray_ties();}
}
module r_check(zip_ties=false){
    assert(r_wall==5 && r_base==10);
    translate([-100,-100,-100]) cube(1);
    if(r_robot){
        assert(len(r_wheels)==(edition=="four"?4:8));
        assert(len(r_bottom_leds)==14);
        // Include hardware-to-hardware clearance, especially unused inner shafts.
        for(x=r_xs){
            intersection(){translate([x,r_ys[0],0])r_motor_hardware();translate([x,r_ys[1],0])r_motor_hardware();}
            assert(r_ys[1]-r_ys[0]>37.2,"Motor insertion envelopes require separate inner shafts");
        }
        intersection(){union(){r_sensor_space();r_sensor_led_space();}union(){r_shell();r_frame(zip_ties);r_tray();r_lid();r_pods()r_motor_hardware();}}
        intersection(){r_sensor_space();r_wheel_space(.2);}
        intersection(){r_sensor_space();union(){r_wheel_install();r_motor_insert();}}
        intersection(){r_sensor_windows(9.8,8.2);union(){r_shell();r_frame(zip_ties);}}
        assert(27+r_service-14.5>18.3+.3,"Wheel starts clear of shaft tip");
        intersection(){r_frame(zip_ties);r_motor_insert();}
        intersection(){r_frame(zip_ties);r_wheel_install();}
        intersection(){union(){r_shell();r_frame(zip_ties);r_pods() r_cap();r_tray();}r_wheel_space(.2);}
        intersection(){r_shell();r_frame(zip_ties);translate([-50,-50,r_top+.01]) cube([400,400,170]);}
        intersection(){r_shell();r_lid();}
        intersection(){r_tray();r_frame(zip_ties);}
        intersection(){r_tray_ties();union(){r_frame(zip_ties);r_tray();r_shell();}}
        intersection(){r_center_battery_straps();union(){r_frame(zip_ties);r_tray();r_shell();r_bottom_lens_space();translate([113.55,W/2-52,r_top+8.1])cube([52.3,104,26]);}}
        intersection(){r_led_wire_space();union(){r_frame(zip_ties);r_shell();r_tray();translate([113.55,W/2-52,r_top+8.1]) cube([52.3,104,26]);}}
        intersection(){r_shelf_ties();union(){r_frame(zip_ties);r_tray();r_shell();r_lid();r_shelf_pack_space();r_pods()r_motor_hardware();r_pods()r_cap();}}
        intersection(){r_shelf_pack_space();union(){r_frame(zip_ties);r_shell();r_tray();r_lid();r_pods() r_motor_hardware();if(zip_ties)r_motor_ties();else r_pods()r_cap();}}
        intersection(){r_frame(zip_ties);r_pods() r_cap();}
        intersection(){r_tray();r_pods() r_cap();}
        intersection(){union(){r_frame(zip_ties);r_pods() r_cap();r_tray();}translate([113.55,W/2-52,r_top+8.1]) cube([52.3,104,26]);}
        if(zip_ties){
            intersection(){r_motor_ties();union(){r_frame(true);r_shell();r_lid();r_tray();r_pods() r_motor_hardware();r_wheel_space(.2);}}
            // Probe the entire front-to-back threading paths, not just empty slots.
            intersection(){r_pods() r_zip_channels();r_pods() r_motor_hardware();}
        }
    }else{
        intersection(){r_shell();r_cup();translate([0,0,40.01]) cube([L,W,150]);}intersection(){r_shell();r_cup(true);translate([0,0,65.01]) cube([L,W,150]);}
    }
    intersection(){union(){r_shell();r_frame(zip_ties);if(r_robot){r_lid();r_tray();r_pods() r_cap();}else{r_cup();r_cup(true);}}
        union(){
            translate([203.5,7.01,97.5]) cube([65,32.88,53]);
            translate([208.5,5.01,103.5]) cube([55,1.98,41]);
            for(back=[false,true]) side(back) for(cx=led_centers) translate([cx-board_x/2,10.01,led_z-board_z/2]) cube([board_x,1.58,board_z]);
        }
    }
}
if(part=="r-assembly") r_assembly();
else if(part=="r-assembly-zip") r_assembly(false,true);
else if(part=="r-exploded") r_assembly(true);
else if(part=="r-shell") r_shell();
else if(part=="r-white") r_white();
else if(part=="r-frame") r_frame();
else if(part=="r-frame-zip") r_frame(true);
else if(part=="r-zip-route") {color([.45,.48,.5]) difference(){r_motor_mount(true);r_zip_channels();r_top_tie_channels();}r_motor_hardware();color([.05,.65,.9]) {r_zip_loops();r_top_tie();}}
else if(part=="r-lid") r_lid();
else if(part=="r-tray") r_tray();
else if(part=="r-cap") r_cap();
else if(part=="r-retainer") rotate([90,0,0]) r_retainer();
else if(part=="r-cup-left") r_cup();
else if(part=="r-cup-right") r_cup(false,true);
else if(part=="r-cup-tower") r_cup(true);
else if(part=="r-check") r_check();
else if(part=="r-check-zip") r_check(true);
else if(part=="r-lcd-coupon") intersection(){r_shell();translate([197,-1,90]) cube([79,43,68]);}
