#import evdev
from evdev import InputDevice, categorize, ecodes

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

#prints out device info at start
print(gamepad)

#evdev takes care of polling the controller in a loop
for event in gamepad.read_loop():
    if event.type == ecodes.EV_KEY:
        print(event)

        # on button press
        if event.value == 1:
            if event.code == aBtn:
                print("A Pressed")
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
            elif event.code == bBtn:
                print("B Released")
            elif event.code == yBtn:
                print("Y Released")
            elif event.code == xBtn:
                print("X Released")
