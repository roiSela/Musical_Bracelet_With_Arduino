
#include <Wire.h>
#include <MPU6050.h>

MPU6050 mpu;



//functions:
void messageToBegin();

bool checkIfRecord();
void checkIfToPlaySound();

void updateSounds();
void initSounds();

//variables:
const float lowBound = 4;
const float highBound = 7;

bool LowDo = false;
bool Re = false;
bool Mi = false;
bool Fa = false;

bool Sol = false;
bool La = false;
bool Si = false;
bool HighDo = false;

const int timeToWaitForEachLoop = 10;
const int TimeToCheckIfThisIsTheSound = 500; //half a second
// now the program starts:


// S E T U P
void setup()
{
  Serial.begin(115200);

  //MPU init
  Serial.println("Initialize MPU6050");

  while (!mpu.begin(MPU6050_SCALE_2000DPS, MPU6050_RANGE_2G))
  {
    Serial.println("Could not find a valid MPU6050 sensor, check wiring!");
    delay(500);
  }
  checkSettings();
  ///done with init

  messageToBegin();
}

// L O O P

void loop()
{

  //Vector normAccel = mpu.readNormalizeAccel();

  //Serial.print("\n Xnorm = ");
  // Serial.print(normAccel.XAxis);
  // Serial.print("\n Ynorm = ");
  // Serial.print(normAccel.YAxis);
  //Serial.print(" Znorm = ");
  // Serial.println(normAccel.ZAxis);


  if(checkIfRecord()) // checking if board was fliped (z = -10)
  {
    Serial.println("record");
    delay(3000); //we wait three seconds to prevent constant printing of the record.
  }else
  {
      checkIfToPlaySound();
  }
  delay(timeToWaitForEachLoop);
}

// END OF L O O P
void checkIfToPlaySound()
{
  updateSounds();  //check witch of the sounds the user wants to play

  if ( LowDo )
  {
    delay(TimeToCheckIfThisIsTheSound);
    updateSounds();
    if ( LowDo )
    {
      Serial.println("LowDo");
    } else
    {
      initSounds(); //needs to init them back to false
    }

  }
  if ( Re )
  {
    delay(TimeToCheckIfThisIsTheSound);
    updateSounds();
    if (Re )
    {
      Serial.println("Re");
    } else
    {
      initSounds(); //needs to init them back to false
    }
  }
  if (  Mi)
  {
    delay(TimeToCheckIfThisIsTheSound);
    updateSounds();
    if ( Mi )
    {
      Serial.println("Mi");
    } else
    {
      initSounds(); //needs to init them back to false
    }
  }
  if (   Fa )
  {
    delay(TimeToCheckIfThisIsTheSound);
    updateSounds();
    if ( Fa )
    {
      Serial.println(" Fa");
    } else
    {
      initSounds(); //needs to init them back to false
    }
  }
  if ( Sol)
  {
    delay(TimeToCheckIfThisIsTheSound);
    updateSounds();
    if ( Sol )
    {
      Serial.println("Sol");
    } else
    {
      initSounds(); //needs to init them back to false
    }
  }
  if (  La )
  {
    delay(TimeToCheckIfThisIsTheSound);
    updateSounds();
    if ( La )
    {
      Serial.println("La");
    } else
    {
      initSounds(); //needs to init them back to false
    }
  }
  if (  Si )
  {
    delay(TimeToCheckIfThisIsTheSound);
    updateSounds();
    if ( Si )
    {
      Serial.println("Si");
    } else
    {
      initSounds(); //needs to init them back to false
    }
  }
  if (HighDo)
  {
    delay(TimeToCheckIfThisIsTheSound);
    updateSounds();
    if ( HighDo)
    {
      Serial.println("HighDo");
    } else
    {
      initSounds(); //needs to init them back to false
    }
  }



}

void updateSounds()
{
  Vector normAccel = mpu.readNormalizeAccel();

  LowDo = (normAccel.XAxis < 0) && (normAccel.XAxis < -lowBound) && (normAccel.XAxis >= -highBound);
  Re = (normAccel.XAxis < 0) && (normAccel.XAxis < -highBound) ;
  Mi = (normAccel.XAxis > 0) && (normAccel.XAxis > lowBound) && (normAccel.XAxis <= highBound);
  Fa = (normAccel.XAxis > 0) && (normAccel.XAxis > highBound) ;

  Sol = (normAccel.YAxis < 0) && (normAccel.YAxis < -lowBound) && (normAccel.YAxis >= -highBound);
  La = (normAccel.YAxis < 0) && (normAccel.YAxis < -highBound) ;
  Si = (normAccel.YAxis > 0) && (normAccel.YAxis > lowBound) && (normAccel.YAxis <= highBound);
  HighDo = (normAccel.YAxis > 0) && (normAccel.YAxis > highBound) ;
}

void initSounds()
{

  LowDo = false;
  Re = false;
  Mi = false;
  Fa = false;

  Sol = false;
  La = false;
  Si = false;
  HighDo = false;
}

bool checkIfRecord()
{
  Vector normAccel = mpu.readNormalizeAccel();
  bool isFliped  = (normAccel.ZAxis < -9);
  return isFliped;
}

void messageToBegin()
{
  Serial.println("Hello...");
  delay(3000);

  Serial.println("We will start in");
  Serial.println("3");
  delay(1000);
  Serial.println("2");
  delay(1000);
  Serial.println("1");
  delay(1000);

}




//library functions I G N O R E
void checkSettings()
{
  Serial.println();

  Serial.print(" * Sleep Mode:            ");
  Serial.println(mpu.getSleepEnabled() ? "Enabled" : "Disabled");

  Serial.print(" * Clock Source:          ");
  switch (mpu.getClockSource())
  {
    case MPU6050_CLOCK_KEEP_RESET:     Serial.println("Stops the clock and keeps the timing generator in reset"); break;
    case MPU6050_CLOCK_EXTERNAL_19MHZ: Serial.println("PLL with external 19.2MHz reference"); break;
    case MPU6050_CLOCK_EXTERNAL_32KHZ: Serial.println("PLL with external 32.768kHz reference"); break;
    case MPU6050_CLOCK_PLL_ZGYRO:      Serial.println("PLL with Z axis gyroscope reference"); break;
    case MPU6050_CLOCK_PLL_YGYRO:      Serial.println("PLL with Y axis gyroscope reference"); break;
    case MPU6050_CLOCK_PLL_XGYRO:      Serial.println("PLL with X axis gyroscope reference"); break;
    case MPU6050_CLOCK_INTERNAL_8MHZ:  Serial.println("Internal 8MHz oscillator"); break;
  }

  Serial.print(" * Accelerometer:         ");
  switch (mpu.getRange())
  {
    case MPU6050_RANGE_16G:            Serial.println("+/- 16 g"); break;
    case MPU6050_RANGE_8G:             Serial.println("+/- 8 g"); break;
    case MPU6050_RANGE_4G:             Serial.println("+/- 4 g"); break;
    case MPU6050_RANGE_2G:             Serial.println("+/- 2 g"); break;
  }

  Serial.print(" * Accelerometer offsets: ");
  Serial.print(mpu.getAccelOffsetX());
  Serial.print(" / ");
  Serial.print(mpu.getAccelOffsetY());
  Serial.print(" / ");
  Serial.println(mpu.getAccelOffsetZ());

  Serial.println();
}
