
#include<VirtualWire.h>
char *controller;
void setup() {
  // put your setup code here, to run once:
pinMode(13,OUTPUT);
vw_set_ptt_inverted(true);
vw_set_rx_pin(11);
vw_setup(4000);
vw_rx_start();
Serial.begin(115200);
}

void loop() {
  // put your main code here, to run repeatedly:
uint8_t buf[VW_MAX_MESSAGE_LEN];
uint8_t buflen=VW_MAX_MESSAGE_LEN;
if (vw_get_message(buf, &buflen))
{
  digitalWrite(13,1);
  char c = char(buf[0]);
  Serial.println(c);
  //if (buf[0]=='0'){}
 // if (buf[0]=='1'){digitalWrite(13,0);Serial.println("Bye");}
 // if (buf[0]=='2'){digitalWrite(13,0);Serial.println("see ya");}
}
}
