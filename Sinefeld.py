# Six LFO's with increasing speed - inspired by Divkid/Instruo Ochd
# Left knob + analogue = global speed control
# To-do: use left knob to de-correlate phases

import math
from europi import *

def scale(lfo_states):
    return [(x + 1) * 5 for x in lfo_states]

def get_states(freq_mults, t_vec, mode):
    states = [math.sin(2 * math.pi * freq * t) for freq, t in zip(freq_mults, t_vec)]
    if mode == "square":
        square = {True: 1, False: -1} # To do: define just once at beginning. probably make part of object
        states = [square[x > 0] for x in states]
    return states

def cycle(freq_mults, t_vec, verbose = False): 
    speed = k1.read_position() + 0.01 + ain.percent() * 100  # smoothing to avoid mult by zero        
    lfo_states = scale(get_states(freq_mults, t_vec, mode="sine"))
    if verbose:
        print(lfo_states)    
    [cv.voltage(lfo) for cv, lfo in zip(cvs, lfo_states)]
    t_vec = [t + speed / 10000 for t in t_vec]
    
    for t in t_vec:
        if t >= 1:
            t = 0
    return t_vec

if __name__ == "__main__":
    freq_mults = [1, 2, 3, 4, 6, 8]
    t_vec = [0, 0, 0, 0, 0, 0]
    oled.centre_text("sinefeld")
    
    while True:
        t_vec = cycle(freq_mults, t_vec, verbose = False)