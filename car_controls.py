from adafruit_motorkit import MotorKit
import pigpio

class RCCar:

    #Motorkit init
    def __init__(self, gasScale, turnScale):
        self.kit = MotorKit()
        self.driveMotor = self.kit.motor2
        self.turnServo = self.kit.motor1
        self.lights = self.kit.motor3
        self.fan = self.kit.motor4

        self.gearToggle = True 
        self.lightToggle = False
        self.fanToggle = False
        self.turnScale = turnScale
        self.gasScale = gasScale
        self.gear = -1

        #remove later
        self.gasScale = .25
        self.turnScale = 1

        #enable later
        #self.turnServo.throttle = 1
        pi = pigpio.pi()
    
    def toggleLights(self):
        self.lightToggle = not self.lightToggle
        if (self.lightToggle):
            self.lights.throttle = -1
        else:
            self.lights.throttle = 0
        print("Light Status:", ("On" if self.lightToggle else "Off"))
    
    def toggleFan(self):
        self.fanToggle = not self.fanToggle
        if (self.fanToggle):
            self.fan.throttle = .8
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


    def accelerate(self, throttle):
        try:
            self.driveMotor.throttle = throttle * self.gear
        except:
            print("Throttle value needs to be between [-1, 1]:", str(throttle))



    # def turn(self, turnRatio):
    #     try:
    #         self.turn
    
    
    
