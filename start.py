#import evdev
from evdev import InputDevice, categorize, ecodes, list_devices
from car_controls import RCCar
import camera_serverv2

#creates object 'gamepad' to store the data
#you can call it whatever you like
try:
    gamepad = InputDevice('/dev/input/event1')
except:
    print("No gamepad detected!")

#prints out device info at start
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
TRIGGER_TOLERANCE = 375
STICK_MAX = 65536
TRIGGER_MAX = 1023

# START CAMERA SERVER
camera_serverv2.CameraServer().start()

# CAR INSTANCE
car = RCCar(.25, 1)

#evdev takes care of polling the controller in a loop
for event in gamepad.read_loop():
    if event.type == ecodes.EV_KEY:
        # on button press
        if event.value == 1:
            if event.code == aBtn:
                car.shiftGear()
            if event.code == bBtn:
                car.toggleLights()
            if event.code == xBtn:
                car.toggleFan()


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
            throttleResult = car.gasScale * (event.value / (TRIGGER_MAX / 2))
            if abs( throttleResult ) <= .31:
                throttleResult = 0
            # else:
            #     throttleResult = gasScale * (event.value / (TRIGGER_MAX / 2)) * gear
            car.accelerate(throttleResult)

        
