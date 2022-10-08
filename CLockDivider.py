import numpy as np
from time import time
from itertools import cycle

class clock_divider():
    def __init__(self):
        self.fake_clock = np.concatenate((np.ones(80000), np.zeros(80000)))
        self.input_state = 0
        self.gate_len = 0
        self.states = [1, 1, 1, 1, 1, 1]
        self.divs = [1, 2, 3, 4, 6, 8]
        self.fake_cvs = [0, 0, 0, 0, 0, 0]
        self.rising_times = [0, 0, 0, 0, 0, 0]

    def step(self):
        if (self.input_state == 1) & (self.states[0] == 0):
            self.rising_times = np.repeat(time(), 6)
            self.states[0] = 1
        elif (self.input_state == 0) & (self.states[0] == 1):
            self.gate_len = time() - self.rising_times[0]
            self.states[0] = 0             
        
        t = time()
        for k, d in enumerate(self.divs):
            if t <= (self.rising_times[k] + self.gate_len / d):
                self.fake_cvs[k] = 1
            elif t <= (self.rising_times[k] + self.gate_len / d * 2):
                self.fake_cvs[k] = 0
            else:
                self.rising_times[k] = self.rising_times[k] + self.gate_len / d * 2

        print([self.input_state, [x for x in self.fake_cvs]], end='\r')

if __name__ == "__main__":
    cd = clock_divider()
    for i in cycle(cd.fake_clock):
        cd.input_state = i
        cd.step()
