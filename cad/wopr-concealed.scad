// Additional concealed-drive variants. Existing robots remain available.
// -D part="concealed" -D panels_per_side=6 -D hidden_wide=false -D W=155
// Wide eight-wheel version: hidden_wide=true, W=210.
include <wopr-variants.scad>
hidden_wide=false;
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
