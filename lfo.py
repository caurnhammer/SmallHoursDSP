import math
import itertools
import os
from scipy.signal import sawtooth
from time import sleep

clear = lambda: os.system('clear')

def scale(lfo_states):
    return [(x + 1) * 5 for x in lfo_states]

# To do: in order to get phase offsets use a vector of diffferent t values, one for each output.
# They can all be updated by the same knob state, to get global control.
def get_states(freq_mults, t, mode):
    if mode == "sine" or mode == "square":
        states = [math.sin(2 * math.pi * freq_mults[cv] * t) for cv in freq_mults]
        if mode == "square":
            square = {True: 1, False: -1} # To do: define just once at beginning. probably make part of object
            states = [square[x > 0] for x in states]
    elif mode == "sawtooth" or mode == "triangle" or mode == "reverse_sawtooth":
        saw_widths = {"sawtooth": 1, "triangle": 0.5, "reverse_sawtooth": 0}
        width = saw_widths[mode]
        states = [sawtooth(2 * math.pi * freq_mults[cv] * t, width) for cv in freq_mults]
    return states

def ascii_bar_scope(data, height=30):
    clear()
    pdict = {True: " * ", False: "   "}
    data = [round(x * height/10) for x in data]
    fullstr = '\n'+' ~ '*6+'\n'
    for row in range(1, height): # Build display top to bottom
        row = height - row
        fullstr += ''.join([pdict[lfo > row] for lfo in data]) + '\n'
    fullstr += ' ~ '*6+'\n'
    print(*fullstr, end='\r')

def ascii_scope(data, height=10, width=10, buffer = []):
    clear()
    if buffer == []:
        buffer = [[" "] * height] * width
    data_scaled = round(data * (height-1)/10)
    data_col = [" "] * height
    data_col[data_scaled] = "*"
    
    # push data in buffer to the left
    buffer[0:width-1] = buffer[1:width]
    # put current lfo state into last col
    buffer[-1] = data_col

    fullstr = ""
    for row_i, _ in enumerate(buffer[0]):
        fullstr += ''.join([buffer[col_i][row_i] for col_i, _ in enumerate(buffer)]) + "\n"
    print(*fullstr, end='\r')
    return buffer

def cycle(freq_mults, knob_state, scope_buffer):
    buffer = scope_buffer
    t = 0
    for i in itertools.cycle(range(1,1024)):
        # To-do: request knob state   
        lfo_states = scale(get_states(freq_mults, t, mode="sine"))
        #print(lfo_states)
        #ascii_bar_scope(lfo_states, height = 30)
        buffer = ascii_scope(lfo_states[2], height=30, width=100, buffer=buffer)
        t = t + knob_state / 1000
        if t >= 1:
            t = 0
        sleep(0.001)

if __name__ == "__main__":
    freq_mults = {'c1': 1, 'c2': 2, 'c3': 3, 'c4': 4, 'c5': 5, 'c6': 6}
    knob = 2
    buffer = []
    cycle(freq_mults, knob, scope_buffer = [])