# Sleep cycle management code

from digitalio import DigitalInOut, Direction, Pull
from analogio import AnalogIn
import adafruit_dotstar as dotstar
import board
import time

######################### CONFIG/CONSTANTS ##############################

ldrThreshV = 1.25   # voltage value above this means its daytime
ldrDThreshV = 0.1   # voltage must increase this much above ldrThreshV before RPi is turned on for debouncing purposes
pollDelayS = 1      # loop delay during the POLL state in seconds
sdDelayS = 30       # delay this many seconds after receiving Done signal from RPi to allow shutdown time
offDelayS = 54000   # wait in the OFF state this many seconds before transitioning to POLL state (goal is until around 12-1AM)

# States
POLL=0        # Polling the LDR input for sunlight trigger
TRIG=1        # First trigger has occured, waiting for increase in light of ldrDThreshV to "debounce" the LDR
ON=2          # Sunlight has reached desired level, Raspberry Pi is turned on
SHUTDOWN=3    # Raspberry Pi has signaled it is done, Allow time for safe shutdown
OFF=4         # Raspberry Pi is off, delay for long time until sunlight is gone

######################### GLOBAL VARS ##############################

currState = POLL
loopDelayS = pollDelayS
piDoneState = False

######################### I/O ##############################

# One pixel connected internally. Keep this off for now.
dot = dotstar.DotStar(board.APA102_SCK, board.APA102_MOSI, 1, brightness=0.2)
dot[0] = [255,255,255]
dot.show()

# Built in red LED
#led = DigitalInOut(board.D13)
#led.direction = Direction.OUTPUT
#led.value = False

# Digital Output to turn on RaspberryPi
piEn = DigitalInOut(board.D0)
piEn.direction = Direction.OUTPUT
piEn.value = False

# Digital Input from RaspberryPi to signal shutdown
piDone = DigitalInOut(board.D2)
piDone.direction = Direction.INPUT

# Analog input on A0 from LDR (photoresistor for sun detection)
ldrPin = AnalogIn(board.A0)

######################### HELPERS ##############################

# Helper to convert analog input to voltage
def getVoltage(pin):
    return (pin.value * 3.3) / 65536

######################### MAIN LOOP ##############################

while True:
  if currState == POLL:
    ldrVal = getVoltage(ldrPin)  # get value of LDR
    print("[state: POLL] LDR: %0.2f" % ldrVal)
    if ldrVal > ldrThreshV:
      print("State change: POLL > TRIG")
      currState = TRIG   # change to TRIG state
      dot[0] = [255,0,0]   # set color to red
      dot.show()
  elif currState == TRIG:
    ldrVal = getVoltage(ldrPin)  # get value of LDR
    print("[state: TRIG] LDR: %0.2f" % ldrVal)
    if ldrVal > (ldrThreshV + ldrDThreshV):
      print("State change: TRIG > ON")
      currState = ON   # change to ON state
      dot[0] = [0,255,0]   # set color to green
      dot.show()
      piEn.value = True  # turn on Raspberry Pi
      #loopDelayS = 10   # temporarily increase loop delay for one cycle while rPi GPIO initialize
  elif currState == ON:
    print("Waiting for done signal")
    loopDelayS = 0.1   # temporarily decrease loop delay while polling piDone signal
    if (piDoneState == False) and (piDone.value == True):     # piDone rising edge
      piDoneState = True
    elif (piDoneState == True) and (piDone.value == False):   # piDone falling edge
      print("State change: ON > SHUTDOWN")
      piDoneState = False
      currState = SHUTDOWN   # change to SHUTDOWN state
      dot[0] = [0,0,255]   # set color to blue
      dot.show()
      loopDelayS = sdDelayS  # set delay to shutdown time
  elif currState == SHUTDOWN:
    print("State change: SHUTDOWN > OFF")
    piEn.value = False  # turn off Raspberry Pi
    loopDelayS = offDelayS  # set delay to off time
    currState = OFF
    dot[0] = [0,0,0]   # turn off LED
    dot.show()
  elif currState == OFF:
    print("State change: OFF > POLL")
    loopDelayS = pollDelayS
    currState = POLL

  time.sleep(loopDelayS)
