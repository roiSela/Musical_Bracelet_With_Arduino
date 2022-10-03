import sys  # for sys.exit()
import requests  # to send HTTP requests
import os #to get the current working directory
import sounddevice  # for recording
from datetime import datetime  # for date
from scipy.io.wavfile import write  # for write the recording
import pygame
import time
import serial.tools.list_ports  # to connect to the same port as the arduino so python and arduino can communicate


def chooseTimeToRecord():
    timeToRecord = 10
    running = True
    while running:
        # RGB = Red, Green, Blue
        screen.fill(WHITE)  # fill screen with white
        # Background Image
        screen.blit(emptyBackground, (0, 0))
        RecordingMessage = font.render("Choose the time to record:", True, GREEN)
        screen.blit(RecordingMessage, (0, 200))

        moveToTheRightMessage = font.render("Move bracelet right to increase the record time.", True, GREEN)
        screen.blit(moveToTheRightMessage, (0, 300))

        moveToTheLeftMessage = font.render("Move bracelet left to decrease the record time.", True, GREEN)
        screen.blit(moveToTheLeftMessage, (0, 350))

        currentRecordTimeMessage = font.render("The current record time is: "+str(timeToRecord) + "seconds.", True, GREEN)
        screen.blit(currentRecordTimeMessage, (0,500))
        messageFromArduino = getMessageFromArduino()  # get the message from the arduino
        if messageFromArduino != 'N':
            print(messageFromArduino)
        if messageFromArduino[0] == 'L':
            if timeToRecord >= 5:
                timeToRecord -= 5
        if messageFromArduino[0] == 'R':
            timeToRecord += 5
        if messageFromArduino[0] == 'S':
            running = False
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT or messageFromArduino == 'L':
                    if timeToRecord >= 5:
                        timeToRecord -= 5
                if event.key == pygame.K_RIGHT  or messageFromArduino == 'R':
                    timeToRecord += 5
                if event.key == pygame.K_SPACE or messageFromArduino == 'S':
                    running = False
        pygame.display.update()
    return timeToRecord

def sendRecordingToServer(dt_string):
    currentWorkingDirectory = os.getcwd()
    # print(currentWorkingDirectory) debug line
    path = currentWorkingDirectory + '/' + dt_string  # get the path of the recording
    # Https://musical-bracelet-server.herokuapp.com/music
    url = "Https://musical-bracelet-server.herokuapp.com/music"  # the url of the server, of course we must use raw string symbol prefix r
    # audioFile = open(path, 'rb')  # open the file in binary mode
    headers = {'content-type': 'audio/wav'}
    files = {'sound': (path, open(path, 'rb'), 'audio/wav', headers)}
    r = requests.post(url, files=files)  # send the file to the server
    print(r)  # debug line!
    print(r.text)
    # try:
    #     currentWorkingDirectory = os.getcwd()
    #     # print(currentWorkingDirectory) debug line
    #     path = currentWorkingDirectory + '/' + dt_string  # get the path of the recording
    #     url = r"Https://musical-bracelet-server.herokuapp.com/music"  # the url of the server, of course we must use raw string symbol prefix r
    #     data = open(path, 'rb')  # open the file in binary mode
    #     headers = {'content-type': 'audio/wav'}
    #     r = requests.post(url, data, headers)
    #     print(r)  # debug line!
    #     return True
    # except:
    #     print("Error while sending the recording to the server")

# pygame init

# RGB COLORS
BLACK = (0, 0, 0)
BLUE = (0, 0, 255)
GREEN = (0, 255, 0)
RED = (255, 0, 0)
WHITE = (255, 255, 255)

# Intialize the pygame
pygame.init()

# Backgrounds
background = pygame.image.load('background.png')  # the background with the circles
emptyBackground = pygame.image.load('emptyBackground.png')  # empty background
piano = pygame.image.load('piano.png')
guitar = pygame.image.load('guitar.png')
flute = pygame.image.load('flute.png')
theInstrumentTheUserChoose = flute  # this will be equal to one of the above instruments

# create the screen
screen = pygame.display.set_mode((800, 600))

# Caption
pygame.display.set_caption("Arduino based musical bracelet")

# font and text
timeToRecord = 10  # this is the text that will appear when the user wants to start recording. TO DO - SEND IT TO THE RECORD FUNCTION
font = pygame.font.Font('freesansbold.ttf', 32)  # type of font and size

# arduino comunication:
ListOfSoundTextColors = [BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK, BLACK]
timeToShowBlueText = 0.5  # same as arduino length of sound variable in the arduino script (the variable appears on line 13 in the arduino script)

#connecting to the arduino via the serial instance
try:
    ports = serial.tools.list_ports.comports()
    serialInst = serial.Serial()

    portList = []

    for onePort in ports:
        portList.append(str(onePort))
        print(str(onePort))  # debug

    # val = input("please choose the port to listen to:")  # we want COM4 sometimes com3 or com6 depend on the arduino.
    val = 3  # a debug line only - need to comment this line and uncomment the line above

    for x in range(0, len(portList)):
        if portList[x].startswith("COM" + str(val)):
            portVar = "COM" + str(val)
            print(portList[x])  # debug

    serialInst.baudrate = 115200  # sometimes 9600
    serialInst.port = portVar
    serialInst.open()
    print("Succesfully connected to arduino.")
except:
    print("Could not connect to arduino, there could be a number of reasons for this error.\nplease check your device "
          "is connected properly, and that no other application is currenly making use of the arduino uno")
    sys.exit()


# end of pygame init

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

        # start and istruction buttons:
        startButton = font.render("Start ", True, startButtonColor)
        screen.blit(startButton, (300, 250))
        instructionsButton = font.render("Instructions", True, instructionsButtonColor)
        screen.blit(instructionsButton, (300, 300))
        messageFromArduino = getMessageFromArduino() # get the message from the arduino
        if messageFromArduino != 'N':
            print(messageFromArduino)
        if messageFromArduino[0] == 'D':
            temp = startButtonColor
            startButtonColor = instructionsButtonColor
            instructionsButtonColor = temp
        if messageFromArduino[0] == 'U':
            temp = startButtonColor
            startButtonColor = instructionsButtonColor
            instructionsButtonColor = temp
        if messageFromArduino[0] == 'S':
            if (startButtonColor == BLUE):
                running = False
        # check for up arrow, down arrow ,enter and exit button clicks.
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
                if event.key == pygame.K_SPACE:
                    if (startButtonColor == BLUE):
                        running = False
                    # else: //to add link to website. open the website with the instructions.

        pygame.display.update()
    return True


def showChooseInstrumentMenu():
    currentChoice = 1  # piano is 1, guitar is 2, flute is 3.
    pianoTextColor = BLUE
    guitarTextColor = BLACK
    fluteTextColor = BLACK
    running = True
    instrumentTChoice = None
    while running:
        # RGB = Red, Green, Blue
        screen.fill(WHITE)  # fill screen with white
        # Background Image
        screen.blit(emptyBackground, (0, 0))
        welcomeSign = font.render("Please choose an instrument.", True, GREEN)
        screen.blit(welcomeSign, (0, 0))


        # draw instruments icons and texts
        pianoIconText = font.render("Piano", True, pianoTextColor)
        screen.blit(pianoIconText, (300, 300))

        guitarIconText = font.render("Guitar", True, guitarTextColor)
        screen.blit(guitarIconText, (300, 250))

        fluteIconText = font.render("Flute", True, fluteTextColor)
        screen.blit(fluteIconText, (400, 300))

        screen.blit(piano, (0, 0))
        screen.blit(guitar, (355, 0))
        screen.blit(flute, (600, 0))
        messageFromArduino = getMessageFromArduino() # get the message from the arduino
        if messageFromArduino != 'N':
            print(messageFromArduino)
        if messageFromArduino[0] == 'L':
            if currentChoice == 1:
                pass
            if currentChoice == 2:
                currentChoice = 1
                pianoTextColor = BLUE
                guitarTextColor = BLACK
                fluteTextColor = BLACK
            if currentChoice == 3:
                currentChoice = 2
                pianoTextColor = BLACK
                guitarTextColor = BLUE
                fluteTextColor = BLACK

        if messageFromArduino[0] == 'R':
            if currentChoice == 3:
                pass
            if currentChoice == 2:
                currentChoice = 3
                pianoTextColor = BLACK
                guitarTextColor = BLACK
                fluteTextColor = BLUE
            if currentChoice == 1:
                currentChoice = 2
                pianoTextColor = BLACK
                guitarTextColor = BLUE
                fluteTextColor = BLACK
        if messageFromArduino[0] == 'S':
            if currentChoice == 1:
                instrumentTChoice = piano
            if currentChoice == 2:
                instrumentTChoice = guitar
            if currentChoice == 3:
                instrumentTChoice = flute
            running = False
        # check for up arrow, down arrow ,enter and exit button clicks.
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_LEFT:  # left arrow pressed
                    if currentChoice == 1:
                        pass

                    if currentChoice == 2:
                        currentChoice = 1
                        pianoTextColor = BLUE
                        guitarTextColor = BLACK
                        fluteTextColor = BLACK

                    if currentChoice == 3:
                        currentChoice = 2
                        pianoTextColor = BLACK
                        guitarTextColor = BLUE
                        fluteTextColor = BLACK

                if event.key == pygame.K_RIGHT:  # right arrow pressed
                    if currentChoice == 3:
                        pass
                    if currentChoice == 2:
                        currentChoice = 3
                        pianoTextColor = BLACK
                        guitarTextColor = BLACK
                        fluteTextColor = BLUE
                    if currentChoice == 1:
                        currentChoice = 2
                        pianoTextColor = BLACK
                        guitarTextColor = BLUE
                        fluteTextColor = BLACK

                if event.key == pygame.K_SPACE:
                    if currentChoice == 1:
                        instrumentTChoice = piano
                    if currentChoice == 2:
                        instrumentTChoice = guitar
                    if currentChoice == 3:
                        instrumentTChoice = flute
                    running = False
        pygame.display.update()
    return instrumentTChoice


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
    screen.blit(La, (550, 470))

    Si = font.render("Si", True, ListOfSoundTextColors[6])
    screen.blit(Si, (330, 470))

    HighDo = font.render("HighDo", True, ListOfSoundTextColors[7])
    screen.blit(HighDo, (90, 380))
    return True

def getMessageFromArduino():
    # this function will get the message from the arduino and return it as a string.
    if serialInst.in_waiting:
        packet = serialInst.readline()  # read byte
        ch = packet.decode('utf').rstrip('\n')  # read till new line
        return ch
    else:
        return 'N' # if there is no message from the arduino, return N, which is not a valid message from the arduino. (stands for no message or None)