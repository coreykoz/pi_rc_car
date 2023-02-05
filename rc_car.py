#import evdev
from evdev import InputDevice, categorize, ecodes, list_devices
from adafruit_motorkit import MotorKit

#creates object 'gamepad' to store the data
#you can call it whatever you like
gamepad = InputDevice('/dev/input/event1')

#button code variables
aBtn = 304
bBtn = 305
yBtn = 308
xBtn = 307
rBumper = 311
lBumper = 310

startBtn = 315
shareBtn = 314

gearToggle = True #if true = gas, false = reverse

#Motorkit stuff
kit = MotorKit()
driverMotor = kit.motor2
turnMotor = kit.motor1

gasScale = .5
turnScale = 1
gear = -1

CENTER_TOLERANCE = 350
TRIGGER_TOLERANCE = 0
STICK_MAX = 65536
TRIGGER_MAX = 1023

#prints out device info at start
print(gamepad)

#evdev takes care of polling the controller in a loop
for event in gamepad.read_loop():
    if event.type == ecodes.EV_KEY:
        # on button press
        if event.value == 1:
            if event.code == aBtn:
                gearToggle = not gearToggle
         

        #Switching gear
        if gearToggle:
            print("Shifted Gear: Drive")
            gear = -1
        else:
            print("Shifted Gear: Reverse")
            gear = 1

     #read stick axis movement
    elif event.type == ecodes.EV_ABS:

        # TURNING
        if event.code == ecodes.ABS_X:
            if abs( event.value ) <= CENTER_TOLERANCE:
                turnResult = 0
            else:
                turnResult = turnScale * ( event.value / (STICK_MAX / 2))
            turnMotor.throttle = turnResult

        # GAS PEDAL
        if event.code == ecodes.ABS_RZ:
            throttleResult = gasScale * (event.value / (TRIGGER_MAX / 2)) * gear
            print(throttleResult, event.value)
            driverMotor.throttle = throttleResult

        
