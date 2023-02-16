from adafruit_motorkit import MotorKit
import pigpio
from gpiozero import LED

class RCCar:

    #Motorkit init
    def __init__(self, gasScale, turnScale, lightsGPIONum):
        self.kit = MotorKit()
        self.driveMotor = self.kit.motor2
        self.turnServo = self.kit.motor4
        #self.lights = self.kit.motor3
        #self.fan = self.kit.motor4

        self.gearToggle = True 
        self.lightToggle = False
        self.fanToggle = False
        self.turnScale = turnScale
        self.gasScale = gasScale
        self.gear = -1

        self.lights = LED(lightsGPIONum)

        # Servo Hz for Traxxas 6065T
        self.servoHz = 500
        self.leftMin = 410000
        self.rightMin = 990000
        self.middle = 700000

        #remove later
        self.gasScale = .25
        self.turnScale = 1

        self.turnServo.throttle = 1
        self.pi = pigpio.pi()
    
    def toggleLights(self):
        self.lightToggle = not self.lightToggle
        if (self.lightToggle):
            #self.lights.throttle = -1
            self.lights.on()
        else:
            #self.lights.throttle = 0
            self.lights.off()
        print("Light Status:", ("On" if self.lightToggle else "Off"))
    
    #no longer functional
    def toggleFan(self):
        return 
        self.fanToggle = not self.fanToggle
        if (self.fanToggle):
            self.fan.throttle = 1
        else:
            self.fan.throttle = 0
        print("Fan Status:", ("On" if self.fanToggle else "Off"))

    # Shift between forward and reverse
    def shiftGear(self):
        self.gearToggle = not self.gearToggle
        if (self.gearToggle):
            self.gear = -1
        else:
            self.gear = 1
        print("Shifted Gear:", ("Drive" if self.gearToggle else "Reverse"))

    # expects an input from [-1, 1]
    def accelerate(self, throttle):
        try:
            self.driveMotor.throttle = throttle * self.gear
        except:
            print("Throttle value needs to be between [-1, 1]:", str(throttle))


    # expects an input from [0-1]
    def turn(self, turnRatio):
        try:
            normTurn = self.leftMin + (self.rightMin - self.leftMin) * turnRatio
            if normTurn <= self.rightMin and normTurn >= self.leftMin:
                self.pi.hardware_PWM(18, self.servoHz, int(normTurn))
            else:
                print("Turn Ratio value needs to be between [", self.leftMin, ",", self.rightMin, "]:", str(normTurn))
        except:
            print("Turn Ratio value needs to be between [0, 1]:", str(turnRatio))
    
    
    
