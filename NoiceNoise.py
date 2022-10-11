from europi import *
from random import uniform

if __name__ == "__main__":
    oled.centre_text("noicenoise")
    
    while True:
        [cv.voltage(uniform(0, 10)) for cv in cvs]