import sounddevice #for recording
from datetime import datetime #for date
from scipy.io.wavfile import write #for write the recording
import pygame
import time
import serial.tools.list_ports #to connect to the same port as the arduino so python and arduino can comunicate

def record_minute_of_sound():
    fps = 44100
    duration = 60  # record for one minute
    print("Recording...")
    recording = sounddevice.rec(int(duration * fps), samplerate=fps, channels=2)
    sounddevice.wait()
    print("Done!")

    now = datetime.now()
    dt_string = now.strftime("date, %d-%m-%Y time, %H-%M-%S")

    dt_string = dt_string + '.wav'
    print(dt_string)
    write(dt_string, fps, recording)
    return True


#pygame init

#RGB COLORS
BLACK = (0,0,0)
BLUE = (0,0,255)
GREEN = (0,255,0)
RED = (255,0,0)
WHITE = (255,255,255)

# Intialize the pygame
pygame.init()

# Background
background = pygame.image.load('background.png')

# create the screen
screen = pygame.display.set_mode((800, 600))

# Caption
pygame.display.set_caption("Arduino based musical bracelet")

#font and text
timeToRecord = 60  #this is the text that will appear when the user wants to start recording.
font = pygame.font.Font('freesansbold.ttf', 32) #type of font and size


#end of pygame init


LowDo = 'LowDo'
Re = 'Re'
Mi = 'Mi'
Fa = 'Fa'
Sol = 'Sol'
La = 'La'
Si = 'Si'
HighDo = 'HighDo'






ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()

portList = []

for onePort in ports:
    portList.append(str(onePort))
    print(str(onePort)) #debug

val = input("please choose the port to listen to:") #we want COM4 sometimes com3 or com6 depend on the arduino.

for x in range(0,len(portList)):
    if portList[x].startswith("COM" + str(val) ):
        portVar = "COM" + str(val)
        print(portList[x]) #debug

serialInst.baudrate = 115200# sometimes 9600
serialInst.port = portVar
serialInst.open()

running = True
while running:
    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if serialInst.in_waiting:
        packet = serialInst.readline() #read byte
        ch = packet.decode('utf').rstrip('\n') #read till new line

        if ch[0] == 'r': #than the user wants to record
            record_minute_of_sound()
        else:
            print(ch)

    time.sleep(0.5)
    pygame.display.update()