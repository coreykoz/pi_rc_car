import evdev
from evdev import InputDevice, categorize, ecodes, list_devices
from car_controls import RCCar
import time

#creates object 'gamepad' to store the data
#you can call it whatever you like
print("Connecting a gamepad...")
while(True):
    try:
        time.sleep(3)
        devices = [evdev.InputDevice(path) for path in evdev.list_devices()]
        for device in devices:
            if  "Xbox" in device.name:
                print("Connected: ", device.name)
                gamepad = InputDevice(device.path)

        if (gamepad):
            break
    except:
        print("No gamepad detected!")

#prints out device info at start
print("Starting RC Car!")
print(gamepad)

#controller button code variables (Xbox Series X Controller via Bluetooth)
aBtn = 304
bBtn = 305
yBtn = 308
xBtn = 307
rBumper = 311
lBumper = 310

startBtn = 315
shareBtn = 314

CENTER_TOLERANCE = 350
# TRIGGER_TOLERANCE = 375
STICK_MAX = 65536 #left stick all the way right
STICK_MIN = 0 #left stick all the way to the left
TRIGGER_MAX = 1023
TRIGGER_MIN = 0
MOTOR_LOAD_MIN = .31

# CAR INSTANCE
car = RCCar(.25, 1, 14)

#evdev takes care of polling the controller in a loop
for event in gamepad.read_loop():
    if event.type == ecodes.EV_KEY:
        # on button press
        if event.value == 1:
            if event.code == aBtn:
                car.shiftGear()
            if event.code == bBtn:
                car.toggleLights()


    #read stick axis movement and trigger movement
    elif event.type == ecodes.EV_ABS:

        # GAS PEDAL
        if event.code == ecodes.ABS_GAS:
            # normalize gas pedal press [0, 1]
            throttleResult = (event.value - TRIGGER_MIN) / (TRIGGER_MAX - TRIGGER_MIN)

            #make sure power is high enough to move motor (under load)
            if abs(throttleResult) <= MOTOR_LOAD_MIN:
                throttleResult = 0

            car.accelerate(throttleResult)
            print(throttleResult)

        # TURNING
        if event.code == ecodes.ABS_X:
            # normalize turning scale from [0, 1]
            turnResult = (event.value - STICK_MIN) / (STICK_MAX - STICK_MIN)

            if turnResult > .45 and turnResult < .55:
                turnResult = .5
            car.turn(turnResult)
            # if abs(event.value) <= CENTER_TOLERANCE:
            #     turnResult = .5
            # else:
            #     turnResult = ( event.value / (STICK_MAX / 2))
            #     lower, upper = -1, 1
            #     turnResult = (turnResult - lower) / (upper - lower)
