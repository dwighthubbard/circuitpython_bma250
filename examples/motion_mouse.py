from adafruit_hid.mouse import Mouse
from bma250 import BMA250 

mouse = Mouse()
bma250 = BMA250()

while True:
    if bma250.xaccel > 40:
        mouse.move(x=1)
    if bma250.xaccel < -40:
        mouse.move(x=-1)
    if bma250.yaccel > 40:
        mouse.move(y=1)
    if bma250.yaccel < -40:
        mouse.move(y=-1)
