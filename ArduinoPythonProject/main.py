from initVariablesAndMenuFunctions import *

def record_duration_of_sound(timeToRecord):
    fps = 44100
    duration = timeToRecord  # record for 10 seconds for exapmle
    print("Recording...")
    recording = sounddevice.rec(int(duration * fps), samplerate=fps, channels=2)
    #sounddevice.wait() #waiting till the recording is done.

    durationCpy = duration
    running = True
    instrumentTChoice = None
    while running:
        messageFromArduino = getMessageFromArduino()  # get the message from the arduino
        if messageFromArduino != 'N':
            print(messageFromArduino)
        # RGB = Red, Green, Blue
        screen.fill(WHITE)  # fill screen with white
        # Background Image
        screen.blit(emptyBackground, (0, 0))
        RecordingMessage = font.render("Recording " + str(durationCpy) + "seconds.", True, GREEN)
        screen.blit(RecordingMessage, (0, 0))
        time.sleep(1)
        pygame.display.update()
        durationCpy -= 1
        if durationCpy == 0:
            running = False
        pygame.display.update()

    now = datetime.now()
    dt_string = now.strftime("date, %d-%m-%Y time, %H-%M-%S")
    dt_string = dt_string + '.wav'
    print(dt_string)
    write(dt_string, fps, recording)

    time.sleep(2)#to make sure the recording is done before sending it to the server
    sendRecordingToServer(dt_string)
    return True

if __name__ == '__main__':#the program starts here:
    print("Welcome to the musical bracelet")


showMainMenu()
theInstrumentTheUserChoose = showChooseInstrumentMenu()

running = True
while running:
    aSoundWasPlayed = False
    # RGB = Red, Green, Blue
    screen.fill((0, 0, 0))
    # Background Image
    screen.blit(background, (0, 0))
    screen.blit(theInstrumentTheUserChoose, (205, 198))

    #ch = getMessageFromArduino()
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
        if ch[0] == 'R':  # Then the user wants to record
            timeToRecord = chooseTimeToRecord()
            record_duration_of_sound(timeToRecord)
        else:
            if ch != 'N':
                print(ch)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False


    # X=205; Y=198;width=355; height=115 #debug only line to find out where is the squre
    # pygame.draw.rect(screen,RED,(X,Y,width,height ))#debug only line
    showSoundTexts()
    time.sleep(0.5)
    pygame.display.update()
    if (aSoundWasPlayed):
        time.sleep(timeToShowBlueText)
    else:
        for i in range(len(ListOfSoundTextColors)):
            ListOfSoundTextColors[i] = BLACK


pygame.quit()
sys.exit()



