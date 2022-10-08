# Simple Attack-Decay (AD) Envelope
# digital input: trigger 
# cv1: Envelope
# cv2: Digital input trigger / gate through
# cv3: Internal gate out (can be longer or shorter than external gate)
# cv4: Inverse envelope
# cv5: Inverse digital input trigger / gate
# cv6: Envelope end gate

import numpy as np
from itertools import cycle
from math import sin
from time import sleep

class EnvelopeGenerator():
    def __init__(self):
        self.state = 0
        self.t = 1
        self.halfpi = 0.5 * np.pi
        self.dinput = 0
        self.sinestate = 0

    def monitor(self):
        # Register new rising edge and start env from beginning
        if (self.state == 0) & (self.dinput == 1):
            self.state = 1
            self.t = 0
        
        self.generate()

    def generate(self):
        # Compute current output
        self.sinestate = np.sin(self.t) * 10
        
        # In/Decrement for next output
        if self.state == 1:
            if self.t <= self.halfpi:
                # to-do: Add scaled knob 1 value
                self.t += 0.001
            elif self.t < np.pi:
                # to-do: add scaled knob 2 value
                self.t += 0.001
            elif self.t >= np.pi:
                self.t = 0
                self.env_end = 1
                self.state = 0 

        self.output()
        self.env_end = 0
        sleep(0.001)

    def output(self):
        # cv1.voltage(self.sinestate)        # Envelope out
        # cv2.voltage(self.dinput)           # External trigger / gate through 
        # cv3.voltage(self.state * 10)       # Internal gate out
        # cv4.voltage(10 - self.sinestate)   # Inverse envelope out
        # cv5.voltage(1 - self.dinput * 10)            # Inverse external trigger / gate through
        # cv6.voltage((1 - self.state) * 10) # Envelope end gate
        print([round(self.sinestate, 3), self.dinput * 10, self.state * 10, round(10 - self.sinestate, 3), (1-self.dinput) * 10, (1 - self.state) * 10])

if __name__ == "__main__":
    fake_din = np.concatenate((np.ones(1), np.zeros(5000)))
    eg = EnvelopeGenerator()
    
    # while True:
    for din in cycle(fake_din):
    #for din in fake_din:
        eg.dinput = din
        eg.monitor()
