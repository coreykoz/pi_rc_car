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

gasBtnStatus = False
reverseBtnStatus = False

#Motorkit stuff
kit = MotorKit()
driverMotor = kit.motor2
turnMotor = kit.motor1

gasScale = .5
turnScale = 1

CENTER_TOLERANCE = 350
STICK_MAX = 65536

#prints out device info at start
print(gamepad)

#evdev takes care of polling the controller in a loop
for event in gamepad.read_loop():
    if event.type == ecodes.EV_KEY:
        # on button press
        if event.value == 1:
            if event.code == aBtn:
                print("A Pressed")
                gasBtnStatus = True
                reverseBtnStatus = False
            elif event.code == bBtn:
                print("B Pressed")
                gasBtnStatus = False
                reverseBtnStatus = True
            elif event.code == yBtn:
                print("Y Pressed")
            elif event.code == xBtn:
                print("X Pressed")

        #on button release
        elif event.value == 0:
            if event.code == aBtn:
                print("A Released")
                gasBtnStatus = False
            elif event.code == bBtn:
                print("B Released")
            elif event.code == yBtn:
                print("Y Released")
            elif event.code == xBtn:
                print("X Released")

        # CAR DRIVING
        if gasBtnStatus:
            driverMotor.throttle = gasScale * -1
        elif reverseBtnStatus:
            driverMotor.throttle = gasScale * 1
        else:
            driverMotor.throttle = 0

     #read stick axis movement
    elif event.type == ecodes.EV_ABS:
        value = event.value
        if abs( value ) <= CENTER_TOLERANCE:
            value = 0
            turnMotor.throttle = value
        if event.code == ecodes.ABS_X:
            turnResult = turnScale * (value / (STICK_MAX / 2))
            print(turnResult)
            turnMotor.throttle = turnResult

        
