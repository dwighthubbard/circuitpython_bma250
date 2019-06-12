import analogio
import board
import busio
import digitalio
import time
from adafruit_bus_device.i2c_device import I2CDevice
from adafruit_hid.mouse import Mouse
 
 
class BMA250:
    _buffer = bytearray(2)
    def __init__(self, i2c_addr=0x19):
        self._device = I2CDevice(busio.I2C(board.SCL, board.SDA), i2c_addr)
        with self._device:
            self._device.write(bytes([0x0f, 0x03]), stop=True)
            self._device.write(bytes([0x10, 0x08]), stop=True)

    @property
    def xaccel(self):
        return self.read10bits(0x02)
    
    @property
    def yaccel(self):
        return self.read10bits(0x04)

    @property
    def zaccel(self):
        return self.read10bits(0x06)

    @property
    def temp_c(self):
        with self._device:
            self._device.write(bytes([0x08]), stop=False)
            self._device.readinto(self._buffer)
            temp = 24.0 + (float(self._buffer[0]) / 2)
            return temp
    
    @property
    def temp_f(self):
        return (self.temp_c * 9.0/5.0) + 32.0
        
    def read10bits(self, register):
        with self._device:
            self._device.write(bytes([register]), stop=False)
            self._device.readinto(self._buffer)
            value = int(self._buffer[1]) << 2 | int(self._buffer[0]) >> 6
            if value > 511:
                value -= 1024
            return value


mouse = Mouse()
bma250 = BMA250()

while True:
    if bma250.xaccel > 40:
        mouse.move(x=-1)
    if bma250.xaccel < -40:
        mouse.move(x=1)
    if bma250.yaccel > 40:
        mouse.move(y=1)
    if bma250.yaccel < -40:
        mouse.move(y=-1)
    
    time.sleep(.01)
