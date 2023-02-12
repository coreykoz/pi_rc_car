#import evdev
from evdev import InputDevice, categorize, ecodes, list_devices
from adafruit_motorkit import MotorKit

#creates object 'gamepad' to store the data
#you can call it whatever you like
gamepad = InputDevice('/dev/input/event1')
#prints out device info at start
print(gamepad)

#controller button code variables
aBtn = 304
bBtn = 305
yBtn = 308
xBtn = 307
rBumper = 311
lBumper = 310

startBtn = 315
shareBtn = 314

CENTER_TOLERANCE = 350
TRIGGER_TOLERANCE = 375
STICK_MAX = 65536
TRIGGER_MAX = 1023


#Motorkit init
kit = MotorKit()
driveMotor = kit.motor2
turnServo = kit.motor1
lights = kit.motor3
fan = kit.motor4

#if true = gas, false = reverse
gearToggle = True 
lightToggle = False
gasScale = .25
turnScale = 1
gear = -1



#evdev takes care of polling the controller in a loop
for event in gamepad.read_loop():
    if event.type == ecodes.EV_KEY:
        # on button press
        if event.value == 1:
            if event.code == aBtn:
                gearToggle = not gearToggle
            if event.code == bBtn:
                lightToggle = not lightToggle
            if event.code == xBtn:
                fanToggle = not fanToggle
         

        #Switching gear
        if gearToggle:
            print("Shifted Gear: Drive")
            gear = -1
        else:
            print("Shifted Gear: Reverse")
            gear = 1

        #Switching lights
        if lightToggle:
            print("Lights: On")
            lights.throttle = -1
        else:
            print("Lights: Off")
            lights.throttle = 0

        #Switching fan
        if fanToggle:
            print("Fan: On")
            fan.throttle = -.8
        else:
            print("Fan: Off")
            fan.throttle = 0

     #read stick axis movement
    elif event.type == ecodes.EV_ABS:

        # # TURNING
        # if event.code == ecodes.ABS_X:
        #     if abs( event.value ) <= CENTER_TOLERANCE:
        #         turnResult = 0
        #     else:
        #         turnResult = turnScale * ( event.value / (STICK_MAX / 2))
        #     turnMotor.throttle = turnResult

        # GAS PEDAL
        if event.code == ecodes.ABS_RZ:
            throttleResult = gasScale * (event.value / (TRIGGER_MAX / 2)) * gear
            if abs( throttleResult ) <= .31:
                throttleResult = 0
            # else:
            #     throttleResult = gasScale * (event.value / (TRIGGER_MAX / 2)) * gear
            driverMotor.throttle = throttleResult

        
