from machine import Pin, I2C
from hmc5883l import HMC5883L
from stepper import Stepper
import utime as time

pin_dir  = Pin(14)
pin_step = Pin(13)
pin_en   = Pin(0)

pin_sda = Pin(12)
pin_scl = Pin(16)

i2c = I2C(scl=pin_scl, sda=pin_sda, freq=100000)

compass = HMC5883L(i2c)
compass.offset_x = 400
compass.offset_y = -45

steppy  = Stepper(pin_en, pin_dir, pin_step)

#while True:
#    x,y,z = compass.mag_comp()
#    print(x,"\t",y)
#    time.sleep(0.1)
#
#compass.calib_manual(200, 0.066)

while True:
    samples = 8.0
    head = 0
    x=0
    y=0
    z=0
    for i in range(0,int(samples)):
        head += compass.mag_heading()
        _x,_y,_z = compass.mag_comp()
        x+=_x
        y+=_y
        z+=_z
        time.sleep(0.014)
    head /= samples
    x /= samples
    y/=samples
    z/=samples
    if head > 180.0:
        head -= 360.0
    print(x,"\t",y,"\t",head)
    if   head > 1:
        steppy.turndeg(1,int(head))
    elif head < -1:
        steppy.turndeg(-1,int(head*-1))
    steppy.off()
    time.sleep(1) 

#def print_mag_xy():
#    raw = compass.mag_raw()
#    print(raw[0], "\t", raw[1])


#angsteps = 5
#for i in range(0,720/angsteps):
#    x,y,z = compass.mag_comp()
#    head = 0
#    for i in range(0,8):
#        head += compass.mag_heading()
#        time.sleep(0.014)
#    head /= 8.0
#    print(x,"\t",y,"\t",head)
#    steppy.turndeg(1,angsteps)
#    steppy.off()
#    time.sleep(0.5)
#    time.sleep(1)
#    print_mag_xy()
