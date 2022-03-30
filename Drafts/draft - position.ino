#include "Wire.h"
#include "I2Cdev.h"
#include "MPU6050.h"
MPU6050 accelgyro;
int16_t ax, ay, az;
int oldax = 0, olday = 0, oldaz = 0;
bool starting = true;
struct Pos
{
  int x;
  int y;
  int z;
};

Pos currentPos = {0, 0, 0};
int Re = 10000;

//void updatecurrentPosalPos(); //call this function when you with to update the currentPosal pos to the current location

void setup() {
  Wire.begin();
  Serial.begin(115200);
  Serial.println("Initializing I2C devices...");
  accelgyro.initialize();
  Serial.println("Testing device connections...");
  Serial.println(accelgyro.testConnection() ? "MPU6050 connection successful" : "MPU6050 connection failed");


  Serial.println("Please put the bracelet in front of your body.");
  delay(5000);
  Serial.println("recived.");
  currentPos.x = 0;
  currentPos.y = 0;
  currentPos.z = 0;


}

void loop() {
  accelgyro.getAcceleration(&ax, &ay, &az);

  if (starting)
  {
    oldax = ax;
    olday = ay;
    oldaz = az;
    starting = false;
  }

  currentPos.x += ax - oldax;
  currentPos.y += ay - olday;
  currentPos.z += az - oldaz;

  Serial.print("yMove ");
  Serial.print( currentPos.y);


  Serial.print("   xMove");
  Serial.print(  currentPos.x);


  Serial.print("  zMove");
  Serial.println( currentPos.z);

  if (currentPos.y >= Re)
  {
    Serial.println("well Done");
    delay(3000);
  }

  oldax = ax;
  olday = ay;
  oldaz = az;
  delay(10);
}
