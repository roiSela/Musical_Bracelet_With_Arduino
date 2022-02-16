import sounddevice
from datetime import datetime #for date
from scipy.io.wavfile import write

import time
import serial.tools.list_ports

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

val = 4 #we want COM4

for x in range(0,len(portList)):
    if portList[x].startswith("COM" + str(val) ):
        portVar = "COM" + str(val)
        print(portList[x]) #debug

serialInst.baudrate = 115200# sometimes 9600
serialInst.port = portVar
serialInst.open()

while True:
    if serialInst.in_waiting:
        packet = serialInst.readline() #read byte
        ch = packet.decode('utf').rstrip('\n') #read till new line

        if ch[0] == 'r': #than the user wants to record
            record_minute_of_sound();
        else:
            print(ch)

        time.sleep(0.5)

