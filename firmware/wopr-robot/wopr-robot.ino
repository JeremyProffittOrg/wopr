#include <WiFi.h>
#include <WebServer.h>
#include <DNSServer.h>
// ESP32 DevKitC V4, ESP32 Arduino core 3.x. Public setup password: change before use.
WebServer server(80);
DNSServer dnsServer;
const int pins[4][2]={{25,26},{27,14},{32,33},{18,19}};
const int SLEEP_PIN=23, FAULT_PIN=21;
bool armed=false, moving=false; unsigned long lastDrive=0;
const char page[] PROGMEM=R"HTML(<!doctype html><meta name="viewport" content="width=device-width,initial-scale=1"><title>WOPR drive</title>
<style>body{font:20px sans-serif;text-align:center;background:#172535;color:white}button{font-size:22px;padding:22px;margin:8px;touch-action:none}#status{min-height:2em}</style>
<h1>WOPR drive</h1><p>Hold a direction to move. Release to stop.</p><button id="arm">Arm</button><button id="stop">STOP</button>
<div><button data-c="f">Forward</button></div><div><button data-c="l">Forward left</button><button data-c="r">Forward right</button></div><div><button data-c="b">Reverse</button></div><p id="status">Stopped</p>
<script>let held='',busy=false,generation=0;const status=document.getElementById('status');
async function stop(){held='';generation++;try{await fetch('/stop',{method:'POST'})}catch{} status.textContent='Stopped - arm again';}
document.getElementById('arm').onclick=async()=>{const r=await fetch('/arm',{method:'POST'});status.textContent=await r.text()};document.getElementById('stop').onclick=stop;
document.querySelectorAll('[data-c]').forEach(b=>{b.onpointerdown=e=>{e.preventDefault();b.setPointerCapture(e.pointerId);held=b.dataset.c};b.onpointerup=stop;b.onpointercancel=stop;b.onlostpointercapture=()=>{if(held)stop()}});
window.onblur=stop;document.addEventListener('visibilitychange',()=>{if(document.hidden)stop()});
setInterval(async()=>{if(!held||busy)return;busy=true;const g=generation;try{const r=await fetch('/drive?c='+held,{method:'POST'});const t=await r.text();if(g===generation){status.textContent=t;if(!r.ok)held=''}}catch{held='';status.textContent='Link lost - robot stops'}finally{busy=false}},100);</script>)HTML";
void halt(){digitalWrite(SLEEP_PIN,LOW);for(auto &p:pins){ledcWrite(p[0],0);ledcWrite(p[1],0);}armed=false;moving=false;}
void motor(int n,int value){ledcWrite(pins[n][0],0);ledcWrite(pins[n][1],0);if(value>0)ledcWrite(pins[n][0],value);if(value<0)ledcWrite(pins[n][1],-value);}
void showController(){server.sendHeader("Cache-Control","no-store");server.send_P(200,"text/html",page);}
void setup(){
  Serial.begin(115200);
  pinMode(SLEEP_PIN,OUTPUT);digitalWrite(SLEEP_PIN,LOW);pinMode(FAULT_PIN,INPUT_PULLUP);
  bool pwm=true;for(auto &p:pins)for(int pin:p){pwm=ledcAttach(pin,18000,8)&&pwm;ledcWrite(pin,0);}
  halt();if(!pwm)return;
  WiFi.mode(WIFI_AP);
  if(!WiFi.softAP("WOPR","wopr-car-setup",1,false,1)){Serial.println("WOPR AP start failed; motors disabled");return;}
  if(!WiFi.AP.enableDhcpCaptivePortal() || !dnsServer.start(53,"*",WiFi.softAPIP())){
    Serial.println("Captive portal startup failed; motors disabled");WiFi.softAPdisconnect(true);return;
  }
  server.on("/",HTTP_GET,showController);
  server.on("/portal",HTTP_GET,showController);
  // OS connectivity probes and unknown HTTP hosts are sent to the controller.
  server.onNotFound([]{
    if(server.method()==HTTP_GET || server.method()==HTTP_HEAD){
      server.sendHeader("Cache-Control","no-store");
      server.sendHeader("Location","http://192.168.4.1/portal");
      server.send(302,"text/plain","Open WOPR controller");
    }else server.send(404,"text/plain","Unknown command");
  });
  server.on("/stop",HTTP_POST,[]{halt();server.send(200,"text/plain","Stopped");});
  server.on("/arm",HTTP_POST,[]{halt();if(digitalRead(FAULT_PIN)==LOW){server.send(409,"text/plain","Driver fault");return;}armed=true;lastDrive=millis();server.send(200,"text/plain","Armed - hold direction");});
  server.on("/drive",HTTP_POST,[]{
    if(!armed||digitalRead(FAULT_PIN)==LOW){halt();server.send(409,"text/plain","Stopped - arm again");return;}
    String cmd=server.arg("c");int l=0,r=0;
    if(cmd=="f"){l=110;r=110;}else if(cmd=="b"){l=-90;r=-90;}else if(cmd=="l"){l=55;r=110;}else if(cmd=="r"){l=110;r=55;}else{halt();server.send(400,"text/plain","Invalid direction");return;}
    // One driver per side: A front, B rear. Swap motor leads if a pod runs backward.
    motor(0,l);motor(1,l);motor(2,r);motor(3,r);digitalWrite(SLEEP_PIN,HIGH);moving=true;lastDrive=millis();server.send(200,"text/plain","Driving - hold to continue");
  });
  server.begin();
}
void loop(){if(armed && (digitalRead(FAULT_PIN)==LOW || WiFi.softAPgetStationNum()==0 || millis()-lastDrive>(moving?500:5000)))halt();server.handleClient();delay(1);}
