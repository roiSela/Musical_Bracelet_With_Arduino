import sounddevice  # for recording
from datetime import datetime  # for date
from scipy.io.wavfile import write  # for write the recording
import pygame
import time
import serial.tools.list_ports  # to connect to the same port as the arduino so python and arduino can communicate


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


# pygame init

# RGB COLORS
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Intialize the pygame
pygame.init()

# Background
background = pygame.image.load('background.png') #the background with the circles
emptyBackground = pygame.image.load('emptyBackground.png')#empty background

# create the screen
screen = pygame.display.set_mode((800, 600))

# Caption
pygame.display.set_caption("Arduino based musical bracelet")

# font and text
timeToRecord = 60  # this is the text that will appear when the user wants to start recording. TO DO - SEND IT TO THE RECORD FUNCTION
font = pygame.font.Font('freesansbold.ttf', 32)  # type of font and size

 #arduino comunication:
ListOfSoundTextColors = [ BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK]
timeToShowBlueText = 1 #same as arduino length of sound
# end of pygame init


# LowDo = 'LowDo'
# Re = 'Re'
# Mi = 'Mi'
# Fa = 'Fa'
# Sol = 'Sol'
# La = 'La'
# Si = 'Si'
# HighDo = 'HighDo'

def showMainMenu():
    startButtonColor = BLUE
    instructionsButtonColor = BLACK
    running = True
    while running:
        # RGB = Red, Green, Blue
        screen.fill((0, 0, 0))
        # Background Image
        screen.blit(emptyBackground, (0, 0))
        welcomeSign = font.render("Welcome to the musical bracelet", True, GREEN)
        screen.blit(welcomeSign, (0, 0))

        #start and istruction buttons:
        startButton = font.render("Start ", True, startButtonColor)
        screen.blit(startButton, (300, 250))
        instructionsButton = font.render("Instructions", True, instructionsButtonColor)
        screen.blit(instructionsButton, (300, 300))

        #check for up arrow, down arrow ,enter and exit button clicks.
        for event in pygame.event.get():
             if event.type == pygame.QUIT:
                running = False
             if event.type == pygame.KEYDOWN:
                 if event.key == pygame.K_DOWN:
                     temp = startButtonColor
                     startButtonColor = instructionsButtonColor
                     instructionsButtonColor = temp
                 if event.key == pygame.K_UP:
                     temp = startButtonColor
                     startButtonColor = instructionsButtonColor
                     instructionsButtonColor = temp
                 if  event.key == pygame.K_SPACE:
                     if(startButtonColor == BLUE):
                         running = False
                     #else: //to add link to website. open the website with the instructions.


        pygame.display.update()
    return True

def showSoundTexts():
    LowDo = font.render("LowDo ", True, ListOfSoundTextColors[0])
    screen.blit(LowDo, (40, 250))

    Re = font.render("Re", True, ListOfSoundTextColors[1])
    screen.blit(Re, (230, 100))

    Mi = font.render("Mi", True, ListOfSoundTextColors[2])
    screen.blit(Mi, (460, 40))

    Fa = font.render("Fa", True, ListOfSoundTextColors[3])
    screen.blit(Fa, (650, 150))

    Sol = font.render("Sol", True, ListOfSoundTextColors[4])
    screen.blit(Sol, (650, 320))

    La = font.render("La", True, ListOfSoundTextColors[5])
    screen.blit( La, (550, 470))

    Si = font.render("Si", True, ListOfSoundTextColors[6])
    screen.blit(Si, (330, 470))

    HighDo = font.render("HighDo", True, ListOfSoundTextColors[7])
    screen.blit(HighDo, (90, 380))
    return True

showMainMenu()

ports = serial.tools.list_ports.comports()
serialInst = serial.Serial()

portList = []

for onePort in ports:
    portList.append(str(onePort))
    print(str(onePort))  # debug

#val = input("please choose the port to listen to:")  # we want COM4 sometimes com3 or com6 depend on the arduino.
val = 3 #a debug line only - need to comment this line and uncomment the line above

for x in range(0, len(portList)):
    if portList[x].startswith("COM" + str(val)):
        portVar = "COM" + str(val)
        print(portList[x])  # debug

serialInst.baudrate = 115200  # sometimes 9600
serialInst.port = portVar
serialInst.open()

running = True
while running:
    aSoundWasPlayed = False
    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False

    if serialInst.in_waiting:
        packet = serialInst.readline()  # read byte
        ch = packet.decode('utf').rstrip('\n')  # read till new line
        if ch[0] == 'A':
            print(ch)
            ListOfSoundTextColors[0] = BLUE
            aSoundWasPlayed = True
        if ch[0] == 'B':
            print(ch)
            ListOfSoundTextColors[1] = BLUE
            aSoundWasPlayed = True
        if ch[0] == 'C':
            print(ch)
            ListOfSoundTextColors[2] = BLUE
            aSoundWasPlayed = True
        if ch[0] == 'D':
            print(ch)
            ListOfSoundTextColors[3] = BLUE
            aSoundWasPlayed = True
        if ch[0] == 'E':
            print(ch)
            ListOfSoundTextColors[4] = BLUE
            aSoundWasPlayed = True
        if ch[0] == 'F':
            print(ch)
            ListOfSoundTextColors[5] = BLUE
            aSoundWasPlayed = True
        if ch[0] == 'G':
            print(ch)
            ListOfSoundTextColors[6] = BLUE
            aSoundWasPlayed = True
        if ch[0] == 'H':
            print(ch)
            ListOfSoundTextColors[7] = BLUE
            aSoundWasPlayed = True
        if ch[0] == 'r':  # Then the user wants to record
            record_minute_of_sound()
        else:
            print(ch)

    showSoundTexts()
    time.sleep(0.5)
    pygame.display.update()
    if(aSoundWasPlayed):
        time.sleep(timeToShowBlueText)
    else:
        for i in range(len(ListOfSoundTextColors)):
            ListOfSoundTextColors[i] = BLACK


