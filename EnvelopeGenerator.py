# Simple Attack-Decay (AD) Envelope
# digital input: trigger 
# cv1: Envelope
# cv2: Digital input trigger / gate through
# cv3: Internal gate out (can be longer or shorter than external gate)
# cv4: Inverse envelope
# cv5: Inverse digital input trigger / gate
# cv6: Envelope end gate

from europi import *
from math import sin, pi, log
from time import sleep
from random import random

class EnvelopeGenerator():
    def __init__(self):
        self.state = 0
        self.t = 1
        self.halfpi = 0.5 * pi
        self.dinput = 0
        self.sinestate = 0
        self.din_isold = 0

    def monitor(self):
        # Register new rising edge and start env from beginning
        if (self.din_isold == 0) & (self.state == 0) & (self.dinput == 1):
            print("edge", random())
            self.state = 1
            self.t = 0
        elif (self.dinput == 0):
            self.state = 0
            self.t = 0
            
        self.generate()

    def generate(self):
        # In/Decrement
        if self.t <= self.halfpi:
                self.t += (100 - k1.read_position()) / 10000 + 0.000001
                self.sinestate = sin(self.t) * 10
        elif (self.t > self.halfpi) & (self.t < pi):
                self.t += (100 - k2.read_position()) / 10000 + 0.000001
                self.sinestate = sin(self.t) * 10
        elif self.t >= pi:
            self.state = 0
            if (self.dinput == 1):
                self.din_isold = 1
                self.sinestate = 0
            else:
                self.din_isold = 0
                self.sinestate = 0

        self.output()

    def output(self):
        cv1.voltage(self.sinestate)        # Envelope out
        cv2.voltage(self.dinput * 10)           # External trigger / gate through 
        cv3.voltage(self.state * 10)       # Internal gate out
        cv4.voltage(10 - self.sinestate)   # Inverse envelope out
        cv5.voltage((1 - self.dinput) * 10)  # Inverse external trigger / gate through
        cv6.voltage((1 - self.state) * 10) # Envelope end gate

if __name__ == "__main__":
    oled.centre_text("Env Gen")
    oled.invert(1)
    sleep(0.5)
    oled.invert(0)
    
    eg = EnvelopeGenerator()
    
    while True:
        eg.dinput = din.value()
        eg.monitor()