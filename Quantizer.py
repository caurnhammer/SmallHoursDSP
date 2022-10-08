import numpy as np
from random import uniform
from time import sleep

class Scales():
    def __init__(self):
        self.major      = np.array([0, 2/12, 4/12, 5/12, 7/12, 9/12, 11/12])
        self.minor      = np.array([0, 2/12, 3/12, 5/12, 7/12, 8/12, 10/12])
        self.ionian     = self.major
        self.dorian     = np.array([0, 2/12, 3/12, 5/12, 7/12, 9/12, 10/12])
        self.phrygian   = np.array([0, 1/12, 3/12, 5/12, 7/12, 8/12, 10/12])
        self.lydian     = np.array([0, 2/12, 4/12, 6/12, 7/12, 9/12, 11/12])
        self.mixolydian = np.array([0, 2/12, 4/12, 5/12, 7/12, 9/12, 10/12])
        self.aeolian    = self.minor
        self.locrian    = np.array([0, 1/12, 3/12, 5/12, 6/12, 8/12, 10/12])
        
        # add some microtonal scales

        self.scalenames = ['major', 'minor', 'ionian', 'dorian', 'phrygian', 'lydian', 'mixolydian', 'aeolian', 'locrian']
        self.scalelist = [self.major, self.minor, self.ionian, self.dorian, self.phrygian, self.lydian, self.mixolydian, self.aeolian, self.locrian]
        
        def full_scale(self, scale):
            return np.repeat(np.arange(0, 10, 1), len(scale)) + np.tile(scale, 10)

        self.scales = dict(zip(self.scalenames, [full_scale(self, x) for x in self.scalelist]))

    def read_scale_knob(self, quant):
        # FAKE KNOB VALUE
        knob_value = uniform(0, 100)
        # knob_value = k1.read_voltage
        knob_scaled = len(s.scales) / 100 * knob_value
        k = quant.quantize(knob_scaled, np.arange(0, len(s.scales)))
        return self.scalenames[k]

class Quantizer():
    def __init__(self):
        self.ainput = 0
        
    def quantize(self, invalue, scale):
        return scale[np.argmin(np.abs(invalue - scale))]

# use din input to trigger quantizastion. if no input quantize continuously
# use knob 2 to select octave. middle position: no offset, left --offset, right ++offset
# add more scales

if __name__ == '__main__':
    s = Scales()
    q = Quantizer()
     
    while True:
        # Select Scale
        
        if selected_scale != s.read_scale_knob(q):
            selected_scale = s.read_scale_knob(q):
            # TURN ON OLED
            # oled.centre_text(selected_scale)

        print(selected_scale)
        # fake input
        q.ainput = uniform(0, 10)
        # q.ainput = ain.read_voltage() / 10

        # if din is connected
        #   if din == 1:
        #       q.quantize()
        # else 
        #   q.quantize()
         
        print(q.quantize(q.ainput, s.scales[selected_scale]))
        sleep(0.5)
