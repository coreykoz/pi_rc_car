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

#Motorkit stuff
kit = MotorKit()
driverMotor = kit.motor2
turnMotor = kit.motor1

CENTER_TOLERANCE = 350
STICK_MAX = 65536

dev = InputDevice( list_devices()[0] )
axis = {
    ecodes.ABS_X: 'ls_x', # 0 - 65,536   the middle is 32768
    ecodes.ABS_Y: 'ls_y',
    ecodes.ABS_Z: 'rs_x',
    ecodes.ABS_RZ: 'rs_y',
    ecodes.ABS_BRAKE: 'lt', # 0 - 1023
    ecodes.ABS_GAS: 'rt',

    ecodes.ABS_HAT0X: 'dpad_x', # -1 - 1
    ecodes.ABS_HAT0Y: 'dpad_y'
}

center = {
    'ls_x': STICK_MAX/2,
    'ls_y': STICK_MAX/2,
    'rs_x': STICK_MAX/2,
    'rs_y': STICK_MAX/2
}

last = {
    'ls_x': STICK_MAX/2,
    'ls_y': STICK_MAX/2,
    'rs_x': STICK_MAX/2,
    'rs_y': STICK_MAX/2
}


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
            elif event.code == bBtn:
                print("B Pressed")
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

        # calibrate zero on Y button
        if event.code == yBtn:
            center['ls_x'] = last['ls_x']
            center['ls_y'] = last['ls_y']
            center['rs_x'] = last['rs_x']
            center['rs_y'] = last['rs_y']
            print( 'calibrated' )

        # CAR DRIVING
        if gasBtnStatus:
            driverMotor.throttle = -.25
        else:
            driverMotor.throttle = 0
            
     #read stick axis movement
    elif event.type == ecodes.EV_ABS:
        if axis[ event.code ] in [ 'ls_x', 'ls_y', 'rs_x', 'rs_y' ]:
            last[ axis[ event.code ] ] = event.value

            value = event.value - center[ axis[ event.code ] ]

            if abs( value ) <= CENTER_TOLERANCE:
                value = 0

            if axis[ event.code ] == 'rs_x':
                if value < 0:
                    print('left')
                else:
                    print('right')
                print( value )

            elif axis[ event.code ] == 'ls_y':
                if value < 0:
                    print('foreward')
                else:
                    print('backward')
                print( value )
