from machine import Pin, I2C
from math    import pi, atan2
import time
import ustruct

pin_sda = Pin(12)
pin_scl = Pin(16)
i2c = I2C(scl=pin_scl, sda=pin_sda, freq=100000)

# I2C address
mag_addr = 0x1E
# register addresses
mag_cra    = 0x00
mag_crb    = 0x01
mag_mode   = 0x02
mag_data   = 0x03
mag_status = 0x09
# modes
mag_cont   = 0x00
mag_single = 0x01
mag_idle   = 0x03

def twos_comp(MSB, LSB):
    comp = MSB * 256 + LSB
    comp = comp - 65536 if comp > 32767 else comp
    return comp

def mag_raw():
    buf = i2c.readfrom_mem(mag_addr, mag_data, 6)
#    print(buf)
    x = twos_comp(buf[0],buf[1])
    z = twos_comp(buf[2],buf[3])
    y = twos_comp(buf[4],buf[5])
    return x,y,z


def mag_heading():
    raw = mag_raw()
    heading = 180.0 * atan2(raw[1],raw[0]) / pi
    return heading

def readregs():
    print("CRA:  ",  i2c.readfrom_mem(mag_addr, mag_cra, 1))
    print("CRB:  ",  i2c.readfrom_mem(mag_addr, mag_crb, 1))
    print("MODE: ",  i2c.readfrom_mem(mag_addr, mag_mode, 1))

readregs()
i2c.writeto_mem(mag_addr, mag_cra, bytes([0x70]))
i2c.writeto_mem(mag_addr, mag_crb, bytes([0x40]))
i2c.writeto_mem(mag_addr, mag_mode, bytes([mag_cont]))
readregs()

while (True):
    _x,_y,_z = mag_raw()
    # print(_x,'\t',_y,'\t',_z)
    print(mag_heading())
    time.sleep_ms(67)
