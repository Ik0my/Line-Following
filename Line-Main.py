import time
import RPi.GPIO as GPIO
from SmartCarModules.Motor import *
from SmartCarModules.Buzzer import *
from SmartCarModules.Thread import *
from SmartCarModules.Ultrasonic import *

us = ultrasonic

#14 = left 15 = Middle 23 = right

class Line_Tracking:
    def __init__(self):
             self.IR01 = 14
             self.IR02 = 15
             self.IR03 = 23
             
             
             self.us = Ultrasonic()
             self.buzzer = Buzzer()
             self.safe = True
             
             GPIO.setmode(GPIO.BCM)
             GPIO.setup(self.IR01, GPIO.IN)
             GPIO.setup(self.IR02, GPIO.IN)
             GPIO.setup(self.IR03, GPIO.IN)
             
    def distanceSafe(self):
        unsafe = 20
        reads = 50
        threshold = 3
        sleepTime = .0005
                 
        while True:
            hits=0
            for i in rance(reads):
                if (self.us.get_distance < unsafe):
                    hits +=1
                time.sleep(sleepTime)
            if hits > threshold:
                self.safe = False
            else:
                self.safe = True
            
             
    def run(self):
        while True:
            L = GPIO.input(self.IR01)
            M = GPIO.input(self.IR02)
            R = GPIO.input(self.IR03)
            
            self.LMR = L * 4 + M * 2 + R
            
            if self.LMR == 0b001: #Right LED, left turn 
                PWM.setMotorModel(2500, 2500, -1500, -1500)
            elif self.LMR == 0b010: #Middle LED, forward
                PWM.setMotorModel(800,800,800,800)
            elif self.LMR == 0b011: #Middle and Right LED, left turn
                PWM.setMotorModel(4000,4000,-2000,-2000)
            elif self.LMR == 0b100: #Left LED, right turn
                PWM.setMotorModel(-1500,-1500,2500,2500)
            elif self.LMR == 0b101: #Both Left and Right LED
                PWM.setMotorModel(0,0,0,0)
            elif self.LMR == 0b110: #Left and Middle, right turn
                PWM.setMotorModel(-2000,-2000,400,400)
            elif self.LMR == 0b111: #ALl LEDS, do nothing
                PWM.setMotorModel(0,0,0,0)
            elif self.LMR == 0b000: #None activated
                t0 = time.time()
                while not(GPIO.input(self.IR01)|GPIO.input(self.IR02)|GPIO.input(self.IR03)):
                    if ((time.time() - t0) > 0.5):
                       PWM.setMotorModel(0,0,0,0)
                       
                       
        def start(self):
            while True:
                if (self.safe):
                    self.run()
            else:
                PWM.setMotorModel(0,0,0,0)
                self.buzzer.run(1)
                time.sleep(0.5)
                self.buzzer.run(0)
                time.sleep(2)

if __name__ == "__main__":
    print("starting")
    infared = Line_Tracking()
    sonarThread = threading.Thread(target = infared.distanceSafe)
    try:
        infared.run()
    except KeyboardInterrupt:
        stop_thread(sonarThread)
        PWM.setMotorModel(0,0,0,0)
