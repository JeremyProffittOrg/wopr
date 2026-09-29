// Current reinforced editions. Dimensions in mm.
// Use -D part="r-assembly", -D edition="four" (seven,six,exposed,four,wide).
include <wopr.scad>
edition="four";
r_robot=edition!="seven" && edition!="six";
r_exposed=edition=="exposed"; r_wide=edition=="wide";
r_wall=5; r_base=10; r_bottom=r_exposed?-10:3; r_top=r_bottom+r_base;
r_axle=r_exposed?-22:18; r_mbottom=r_axle-14.4; r_mtop=r_axle+56;
r_cap_z=r_axle+60.3;
r_xs=edition=="four"?[54,L-54]:[46.3,L-46.3];
r_ys=r_exposed?[28,W-28]:[54,W-54];
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
module r_raw(){difference(){
    union(){
        difference(){outline();r_inside();
            for(back=[false,true]) side(back) translate([bank_x-bank_w/2-10,4,led_z-board_z/2-5.3]) cube([bank_w+20,20,board_z+10.6]);
            translate([tft_x-32.8,-1,tft_z-26.8]) cube([65.6,42,53.6]);
        }
        r_lights();r_display();r_bosses();
        // Keep five millimeters of gray backing beneath the recessed lettering.
        for(back=[false,true]) side(back) translate([199,4.5,54]) cube([76,1.3,31]);
        if(r_robot) for(x=[9,173],y=[5,W-30]) translate([x,y,106]) cube([14,25,10]);
        else {r_cup_supports();
            for(back=[false,true]) side(back) translate([20,4.5,16]) cube([250,1.2,43]);
            side(true) translate([200,4.5,139]) cube([66,1.2,16]);
        }
    }
    r_white();translate([-1,-1,-7]) cube([L+2,W+2,7]);
    if(r_robot) translate([-1,W/2,55]) rotate([0,90,0]) cylinder(d=12.3,h=8);
    else {
        intersection(){door_grooves();union(){translate([-1,-1,0]) cube([L+2,W+2,60]);translate([190,W-2,138]) cube([90,4,20]);}}
        translate([232,W-8,20]) cube([12,10,7]);
    }
}}
module r_shell(){difference(){r_raw();
    if(r_robot){r_hatch();r_lid_holes(2.5);
        if(!r_exposed) for(p=r_wheels,x=[-35.5,35.5]) translate([p[0]+x-5.3,p[1]-6.3,r_top-.01]) cube([10.6,12.6,r_axle-r_top+.32]);
    }
    else r_cup_cuts();
    if(r_exposed) for(p=r_wheels) translate(p) r_axc(38,42);
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
        translate([20.3,27,39]) cube([75.7,101,45.9]);
    }
}
module r_axc(r,h){rotate([90,0,0]) cylinder(r=r,h=h,center=true,$fn=64);}
module r_wheel_space(gap=0,up=false){for(p=r_wheels){translate(p) r_axc(31.5+gap,29+2*gap);if(up) translate([p[0]-31.5-gap,p[1]-14.5-gap,-100]) cube([63+2*gap,29+2*gap,250]);}}
module r_pods(){for(x=r_xs,y=r_ys) translate([x,y,0]) children();}
module r_pod(){difference(){union(){
    // Ten-millimeter bearing foot and bolting flange; all side cheeks are five.
    translate([-16.7,-11.5,r_mbottom-10]) cube([33.4,23,10]);
    for(x=[-16.7,11.7]) translate([x,-11.5,r_mbottom]) cube([5,23,r_axle+60-r_mbottom]);
    for(x=[-22,22]) translate([x-6.5,-6.5,r_mbottom-5]) cube([13,13,r_axle+65-r_mbottom]);
    translate([-41,-11.5,r_bottom-10]) cube([82,23,10]);
    for(z=[r_mbottom+5,r_axle+42]) for(x=[-24,16]) translate([x,-5,z]) cube([8,10,5]);
}
    translate([-11.7,-11.7,r_mbottom]) cube([23.4,23.4,100]);
    for(x=[-22,22]) translate([x,0,r_axle+47]) cylinder(d=2.5,h=20);
    for(x=[-36,36]){translate([x,0,r_bottom-11]) cylinder(d=3.3,h=12);translate([x,0,r_bottom-10.01]) cylinder(d=6.5,h=3.21);}
}}
module r_cap(){difference(){union(){
    translate([-33,-16.7,r_cap_z]) cube([66,33.4,5]);
    for(y=[-16.7,11.7]) translate([-33,y,r_axle+39]) cube([66,5,r_cap_z-r_axle-39]);
}
    for(x=[-22,22]) translate([x,0,r_cap_z-1]) cylinder(d=3.3,h=7);
    translate([-6,-5,r_cap_z-1]) cube([12,10,7]);
}}
module r_hood(front=true){if(!front) mirror([0,1,0]) r_hood(true);else difference(){union(){
    intersection(){translate([0,0,r_axle]) r_axc(37.5,40.4);translate([-42,-22,r_axle+.3]) cube([84,44,40]);}
    for(x=[-35.5,35.5]) translate([x-5,-6,r_axle+.3]) cube([10,12,5]);
}
    translate([0,0,r_axle]) r_axc(32.5,30.4);
    translate([-17,15.2,r_axle]) cube([34,40,80]);
    for(x=[-35.5,35.5]) translate([x,0,r_axle]) cylinder(d=3.3,h=9);
}}
function r_front(p)=p[1]==r_ys[0]-27 || p[1]==r_ys[1]-27;
module r_hoods(){for(p=r_wheels) translate([p[0],p[1],0]) r_hood(r_front(p));}
module r_frame(){difference(){union(){
    translate([5.3,r_exposed?-20.5:5.3,r_bottom]) linear_extrude(r_base) offset(r=2) translate([2,2]) square([L-14.6,r_exposed?W+37:W-14.6]);
    if(r_exposed) intersection(){for(p=r_wheels) translate(p) r_axc(37.5,41);translate([0,-25,r_bottom]) cube([L,W+50,30]);}
    if(r_robot){
        for(p=r_tray_holes) translate([p[0],p[1],r_top]) cylinder(d=13,h=67-r_top);
        for(x=[114,163],y=[W/2-40,W/2+40]) translate([x-9,y-7.5,r_top]) cube([18,15,15]);
        if(!r_exposed) for(p=r_wheels,x=[-35.5,35.5]) translate([p[0]+x-5,p[1]-6,r_top-.5]) cube([10,12,r_axle-r_top+.5]);
    }
}
    for(p=r_holes) translate([p[0],p[1],r_bottom-1]) cylinder(d=3.3,h=r_base+2);
    if(r_robot){
        r_wheel_space(1,!r_exposed);
        r_pods() translate([-28.8,-12,r_bottom-.1]) cube([57.6,24,150]);
        for(x=r_xs,y=r_ys,dx=[-36,36]) translate([x+dx,y,r_bottom-.1]) cylinder(d=2.5,h=8.1);
        if(!r_exposed) for(p=r_wheels,x=[-35.5,35.5]) translate([p[0]+x,p[1],r_top-5]) cylinder(d=2.5,h=r_axle-r_top+6);
        for(p=r_tray_holes) translate([p[0],p[1],55]) cylinder(d=2.5,h=15);
        for(x=[114,163],y=[W/2-40,W/2+40]) translate([x-4,y-8.5,r_top+6]) cube([8,17,3]);
    }
}}
module r_tray(){difference(){translate([92,W/2-44,67.3]) cube([98,88,5]);
    for(p=r_tray_holes) translate([p[0],p[1],66]) cylinder(d=3.3,h=8);
    for(x=[111,139,167],y=[W/2-28,W/2+14]) translate([x,y,66]) cube([3,14,8]);
}}
module r_hardware(){
    for(back=[false,true]) side(back) for(cx=led_centers){
        color([.08,.09,.10]) translate([cx-board_x/2,10,led_z-board_z/2]) cube([board_x,1.6,board_z]);
        for(i=[0:9],j=[0:5]) color([1,.23,.04]) translate([cx-9+i*2,8.95,led_z-5+j*2]) cube([1,1.05,1]);
    }
    color([.07,.12,.14]) translate([208.5,5,103.5]) cube([55,2,41]);
    if(r_robot){
        r_pods(){color([.95,.67,.07]) translate([-11.2,-9.3,r_axle-14]) cube([22.4,18.6,38]);color([.55,.57,.59]) translate([-10,-11.2,r_axle+24]) cube([20,22.4,32]);color([.8,.8,.8]) translate([0,0,r_axle]) r_axc(2.7,36.6);}
        for(p=r_wheels) color([.98,.4,.08]) translate(p) r_axc(31.5,29);
        color([.12,.15,.19]) translate([87.5,W/2-26.15,r_top+1]) cube([104,52.3,26]);
        color([.08,.4,.26]) translate([97,W/2-34,77.3]) cube([55,28,10]);
        for(x=[100,133]) color([.1,.35,.65]) translate([x,W/2+5,77.3]) cube([26,18,9]);
    }
}
module r_assembly(explode=false){
    color([.40,.43,.46]) translate([0,0,explode?100:0]) r_shell();
    color([.98,.98,.96]) translate([0,0,explode?100:0]) r_white();
    color([.31,.34,.37]) r_frame();
    if(r_robot){
        color([.40,.43,.46]) translate([0,0,explode?170:0]) r_lid();
        color([.50,.53,.56]) r_pods(){r_pod();r_cap();}
        color([.65,.68,.70]) translate([0,0,explode?60:0]) r_tray();
        if(!r_exposed) color([.47,.50,.53]) r_hoods();
    }else color([.4,.43,.46]){r_cup();r_cup(true);}
    if(electronics) r_hardware();
}
module r_check(){
    assert(r_wall==5 && r_base==10);
    translate([-100,-100,-100]) cube(1);
    if(r_robot){
        assert(len(r_wheels)==(edition=="four"?4:8));
        intersection(){union(){r_shell();r_frame();r_pods(){r_pod();r_cap();}if(!r_exposed) r_hoods();r_tray();}r_wheel_space(.2);}
        intersection(){r_frame();r_pods() r_pod();translate([-50,-50,r_bottom+.01]) cube([400,400,170]);}
        intersection(){r_shell();r_frame();translate([-50,-50,r_top+.01]) cube([400,400,170]);}
        intersection(){r_shell();r_lid();}
        intersection(){r_tray();r_pods(){r_pod();r_cap();}}
        if(!r_exposed) intersection(){r_hoods();union(){r_frame();r_pods(){r_pod();r_cap();}r_shell();r_tray();}}
        intersection(){union(){r_frame();r_pods(){r_pod();r_cap();}r_tray();if(!r_exposed) r_hoods();}translate([87.5,W/2-26.15,r_top+1]) cube([104,52.3,26]);}
        // Motor cassettes insert from below; caps and hoods are installed afterward.
        for(dz=[-100,-60,-30,-10,0]){
            intersection(){r_frame();translate([0,0,dz]) r_pods() r_pod();translate([-50,-50,r_bottom+.01]) cube([400,400,180]);}
            intersection(){r_frame();translate([0,0,dz]) r_wheel_space(.2);}
        }
        if(!r_exposed) for(dz=[0,10,30,60,90]) intersection(){translate([0,0,dz]) r_hoods();union(){r_frame();r_pods() r_pod();}}
    }else{
        intersection(){r_shell();r_cup();translate([0,0,40.01]) cube([L,W,150]);}intersection(){r_shell();r_cup(true);translate([0,0,65.01]) cube([L,W,150]);}
    }
    // Actual PCB/glass and rear display bay are protected in every edition.
    intersection(){union(){r_shell();r_frame();if(r_robot){r_lid();r_tray();r_pods(){r_pod();r_cap();}}else{r_cup();r_cup(true);}}
        union(){
            translate([203.5,7.01,97.5]) cube([65,32.88,53]);
            translate([208.5,5.01,103.5]) cube([55,1.98,41]);
            for(back=[false,true]) side(back) for(cx=led_centers) translate([cx-board_x/2,10.01,led_z-board_z/2]) cube([board_x,1.58,board_z]);
        }
    }
}
if(part=="r-assembly") r_assembly();
else if(part=="r-exploded") r_assembly(true);
else if(part=="r-shell") r_shell();
else if(part=="r-white") r_white();
else if(part=="r-frame") r_frame();
else if(part=="r-lid") r_lid();
else if(part=="r-tray") r_tray();
else if(part=="r-pod") r_pod();
else if(part=="r-cap") r_cap();
else if(part=="r-hood-front") r_hood(true);
else if(part=="r-hood-rear") r_hood(false);
else if(part=="r-retainer") rotate([90,0,0]) r_retainer();
else if(part=="r-cup-left") r_cup();
else if(part=="r-cup-right") r_cup(false,true);
else if(part=="r-cup-tower") r_cup(true);
else if(part=="r-check") r_check();
else if(part=="r-lcd-coupon") intersection(){r_shell();translate([197,-1,90]) cube([79,43,68]);}
