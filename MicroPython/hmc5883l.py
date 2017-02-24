from machine import Pin, I2C
from math import pi, atan2
import utime as time

# I2C address
mag_addr   = 0x1E
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

class HMC5883L:
    def __init__(self, bus):
        self.offset_x = 0
        self.offset_y = 0
        self.scale_x = 1
        self.scale_y = 1
        self.declination = 0
        self.bus = bus
                                                       # 8 smpls  # 75 Hz      # no bias
        self.bus.writeto_mem(mag_addr, mag_cra,  bytes([0b11 << 5 | 0b110 << 2 | 0b00]))
                                                       # gain 1.3
        self.bus.writeto_mem(mag_addr, mag_crb,  bytes([0b001 << 5]))
        self.bus.writeto_mem(mag_addr, mag_mode, bytes([mag_cont]))

    def mag_raw(self):
        buf = self.bus.readfrom_mem(mag_addr, mag_data, 6)
        x = twos_comp(buf[0],buf[1])
        z = twos_comp(buf[2],buf[3])
        y = twos_comp(buf[4],buf[5])
        return x,y,z

    def mag_comp(self):
        x,y,z = self.mag_raw()
        x -= self.offset_x
        y -= self.offset_y
        x *= self.scale_x
        y *= self.scale_y
        return x,y,z

    def mag_heading(self):
        x,y,z = self.mag_comp()
        heading_rad = atan2(y, x)
        heading_deg = heading_rad * 180.0 / pi
        if heading_deg < 0:
            heading_deg += 360.0
        return heading_deg

    def calib_manual(self,num_samples,interval_secs):
        print("Start calib: ", num_samples, " samples, one every", interval_secs, "s -> total time:", num_samples*interval_secs, "s")
        x_min = 0
        x_max = 0
        y_min = 0
        y_max = 0
        for i in range(0,num_samples):
            raw_x, raw_y, raw_z = self.mag_raw()
            if raw_x < x_min or i == 0:
                x_min = raw_x
            if raw_x > x_max or i == 0:
                x_max = raw_x
            if raw_y < y_min or i == 0:
                y_min = raw_y
            if raw_y > y_max or i == 0:
                y_max = raw_y
            print(i, "\t", raw_x, "\t", raw_y)
            time.sleep(interval_secs)
        print(" ")
        self.offset_x = (x_min + x_max) / 2
        self.offset_y = (y_min + y_max) / 2
        avg_scale = ((x_max - x_min) + (y_max - y_min)) / 2
        self.scale_x = avg_scale / (x_max - x_min)
        self.scale_y = avg_scale / (y_max - y_min)
        print("Offset:", "\t", self.offset_x, "\t", self.offset_y)
        print("Scale:",  "\t", self.scale_x,  "\t", self.scale_y )
        print(" ")
