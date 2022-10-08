import numpy as np
from random import uniform

class Scales():
    def __init__(self):
        self.major = np.array([0, 2/12, 4/12, 5/12, 7/12, 9/12, 11/12])
        self.minor = np.array([0, 2/12, 3/12, 5/12, 7/12, 8/12, 10/12])
        self.ionian = major
        self.aeolian = minor 
        
        self.scalelist = [self.major, self.minor, self.ionian, self.aeolian]


    def full_scale(self, scale):
        return np.repeat(np.arange(0, 10, 1), len(scale)) + np.tile(scale, 10)

class Quantizer():
    def __init__(self):
        self.scales = Scales()
        self.major = self.scales.full_scale(self.scales.major)
        self.ainputi = 0
        
    def quantize(self):
        return self.major[np.argmin(np.abs(self.ainput - self.major))]

if __name__ == '__main__':
    q = Quantizer()
    q.ainput = uniform(0, 10)
    print(q.quantize())
