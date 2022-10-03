#include<VirtualWire.h>
char *controller;
#include <Wire.h>
#include <MPU6050.h>

MPU6050 mpu;

//midi stuff:

#include <SoftwareSerial.h>

//vars:
SoftwareSerial mySerial(2, 3); // RX, TX

byte note = 0; //The MIDI note value to be played
byte resetMIDI = 4; //Tied to VS1053 Reset line
byte ledPin = 13; //MIDI traffic inidicator
int lengthOfSoundInMiliSeconds = 500;

//now we will set the values in such a way that for changing octave one will only need to change the DO SOUND (:
int LowDo_sound = 60;
int Re_sound = LowDo_sound + 2;
int Mi_sound = Re_sound + 2;
int Fa_sound = Mi_sound + 1;
int Sol_sound = Fa_sound + 2;
int La_sound = Sol_sound + 2;
int Si_sound =   La_sound + 2;
int HighDo_sound = Si_sound + 1;

//we will support 3 types of instruments
int InstrumentArrayIndex = 0;
int instrument[3] = {1, 26, 74}; //piano, guitar, flute. see page 33 of the sparkfun documintation.

//menu, we need the arduino to be able to navigate its way through the menu
//choose play or instructions(tutorial) and then play, then
//choose instrument, then,
//play sound and record if you want
enum menu {HomeScreen, ChooseInstrument, PlayMode};
menu m = HomeScreen; //an instance of menu.

//funcs:
void playSound(int soundToPlay);
void noteOff(byte channel, byte note, byte release_velocity);
void noteOn(byte channel, byte note, byte attack_velocity);
void talkMIDI(byte cmd, byte data1, byte data2);


//end of midi stuff



//functions:
void sendMessageToReciver(char c);
void messageToBegin();
bool checkIfRecord();
void checkIfToPlaySound();
void updateSounds();
void initSounds();//inits all the sounds back to false.
void chooseInstrument();//choose piano, guitar or flute
void homeScreen();//choose play or instructions
void chooseTimeToRecord(); //choosing the time to record
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
const int TimeToCheckIfThisIsTheSound = 200; //300 is a good wait time from tests
// now the program starts:


// S E T U P
void setup()
{
  Serial.begin(115200);

     // setup for RF
  pinMode(13, OUTPUT);
  vw_set_ptt_inverted(true);
  vw_set_tx_pin(12);
  vw_setup(4000);

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

  //Setup soft serial for MIDI control
  mySerial.begin(31250);

  //Reset the VS1053
  pinMode(resetMIDI, OUTPUT);
  digitalWrite(resetMIDI, LOW);
  delay(100);
  digitalWrite(resetMIDI, HIGH);
  delay(100);
  talkMIDI(0xB0, 0x07, 120); //0xB0 is channel message, set channel volume to near max (127)


}

// L O O P

void loop()
{
  switch (m) {
    case HomeScreen:
      homeScreen();
      break;
    case ChooseInstrument:
      chooseInstrument();
      break;
    case PlayMode:
      //set instrument bank and current instrument to play:
      talkMIDI(0xB0, 0, 0x00); //Default bank GM1
      talkMIDI(0xC0, instrument[InstrumentArrayIndex], 0); //Set instrument number. 0xC0 is a 1 data byte command
      //end

      if (checkIfRecord()) // checking if board was fliped (z = -10)
      {
        sendMessageToReciver("r");//r stands for record
        chooseTimeToRecord();
        //delay(3000); //we wait three seconds to prevent constant printing of the record.
      } else
      {
        checkIfToPlaySound();
      }
      break;
  }
  delay(timeToWaitForEachLoop);
}

// END OF L O O P
void homeScreen() {
  Vector normAccel = mpu.readNormalizeAccel();
  bool moveRightInMenu = (normAccel.XAxis < 0) && (normAccel.XAxis < -highBound) ;
  if (moveRightInMenu) {
   sendMessageToReciver("D");//stans for right
    delay(1000); //lets wait a bit before continue
  }
  bool moveLeftInMenu = (normAccel.XAxis > 0) && (normAccel.XAxis > highBound) ;
  if (moveLeftInMenu) {
    sendMessageToReciver("U");//stands for left
    delay(1000); //lets wait a bit before continue
  }
  bool choosingAnOption = (normAccel.YAxis > 0) && (normAccel.YAxis > highBound) ;
  if (choosingAnOption) {
   sendMessageToReciver("S");//stands for select
    delay(3000); //lets wait a bit before continue
    m = ChooseInstrument;
  }
  delay(100);
}
void chooseInstrument() {//we will use capital letters to differentiate between the home screen signals
  Vector normAccel = mpu.readNormalizeAccel();
  bool moveRightInMenu = (normAccel.XAxis < 0) && (normAccel.XAxis < -highBound) ;
  if (moveRightInMenu) {
    sendMessageToReciver("R");
    delay(1000); //lets wait a bit before continue
    if (InstrumentArrayIndex != 2) {
      InstrumentArrayIndex++;
    }
  }
  bool moveLeftInMenu = (normAccel.XAxis > 0) && (normAccel.XAxis > highBound) ;
  if (moveLeftInMenu) {
    sendMessageToReciver("L");
    delay(1000); //lets wait a bit before continue
    if (InstrumentArrayIndex != 0) {
      InstrumentArrayIndex--;
    }
  }
  bool choosingAnOption = (normAccel.YAxis > 0) && (normAccel.YAxis > highBound) ;
  if (choosingAnOption) {
    sendMessageToReciver("S");//stands for select
    m = PlayMode;
    delay(3000); //lets wait a bit before continue
  }
  delay(100);
}

void chooseTimeToRecord() {
  bool timeChoosen = false;
  while (!timeChoosen) {
    Vector normAccel = mpu.readNormalizeAccel();
    bool moveRightInMenu = (normAccel.XAxis < 0) && (normAccel.XAxis < -highBound) ;
    if (moveRightInMenu) {
     sendMessageToReciver("R");
      delay(1000); //lets wait a bit before continue
    }
    bool moveLeftInMenu = (normAccel.XAxis > 0) && (normAccel.XAxis > highBound) ;
    if (moveLeftInMenu) {
      sendMessageToReciver("L");
      delay(1000); //lets wait a bit before continue
    }
    bool choosingAnOption = (normAccel.YAxis > 0) && (normAccel.YAxis > highBound) ;
    if (choosingAnOption) {
      sendMessageToReciver("S");//stands for select
      timeChoosen = true;
      delay(1000); //lets wait a bit before continue
    }
    delay(100);
  }
}

void checkIfToPlaySound()
{
  updateSounds();  //check witch of the sounds the user wants to play

  if ( LowDo )
  {
    delay(TimeToCheckIfThisIsTheSound);
    updateSounds();
    if ( LowDo )
    {
      sendMessageToReciver("A"); //sends message to the python code throgh the same port
      playSound(LowDo_sound); //making the actual sound
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
      sendMessageToReciver("B");
      playSound(Re_sound);
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
      sendMessageToReciver("C");
      playSound(Mi_sound);
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
      sendMessageToReciver("D");
      playSound(Fa_sound);
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
      sendMessageToReciver("E");
      playSound(Sol_sound);
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
      sendMessageToReciver("F");
      playSound(La_sound);
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
      sendMessageToReciver("G");
      playSound(Si_sound);
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
      sendMessageToReciver("H");
      playSound(HighDo_sound);
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
  sendMessageToReciver("3");
  delay(1000);
  sendMessageToReciver("2");
  delay(1000);
  sendMessageToReciver("1");
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



void playSound(int soundToPlay)
{
  noteOn(0, soundToPlay, 60);
  delay(lengthOfSoundInMiliSeconds);

  //Turn off the note with a given off/release velocity
  noteOff(0, soundToPlay, 60);
  delay(50);
}

//Send a MIDI note-on message.  Like pressing a piano key
//channel ranges from 0-15
void noteOn(byte channel, byte note, byte attack_velocity) {
  talkMIDI( (0x90 | channel), note, attack_velocity);
}

//Send a MIDI note-off message.  Like releasing a piano key
void noteOff(byte channel, byte note, byte release_velocity) {
  talkMIDI( (0x80 | channel), note, release_velocity);
}

//Plays a MIDI note. Doesn't check to see that cmd is greater than 127, or that data values are less than 127
void talkMIDI(byte cmd, byte data1, byte data2) {
  digitalWrite(ledPin, HIGH);
  mySerial.write(cmd);
  mySerial.write(data1);

  //Some commands only have one data byte. All cmds less than 0xBn have 2 data bytes
  //(sort of: http://253.ccarh.org/handout/midiprotocol/)
  if ( (cmd & 0xF0) <= 0xB0)
    mySerial.write(data2);

  digitalWrite(ledPin, LOW);
}

void sendMessageToReciver(char* c)
{
  
  //controller = "0";
  controller = c;
  Serial.println(controller);
  vw_send((uint8_t *)controller, strlen(controller));
  vw_wait_tx();
  digitalWrite(13, 1);

if(c[0] != 'S')//if it doesnt control the menu, lets try to send it twice
{
  Serial.println(controller);//DEBUG
      vw_send((uint8_t *)controller, strlen(controller));
  vw_wait_tx();
  digitalWrite(13, 1);
}


}
