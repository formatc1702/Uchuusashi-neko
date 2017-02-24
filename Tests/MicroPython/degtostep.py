from machine import Pin, PWM, I2C
from math    import pi, atan2
import ustruct
import time

def step_on():
    pin_en.low()
    print("ON")
    

def step_off():
    pin_en.high()
    print("OFF")

def dostep(dir,numsteps):
    step_on()
    if dir == 1:
        pin_dir.high()
        print("CW ?")
    else:
        pin_dir.low()
        print("CCW?")
    print("GO")
    for i in range(0,numsteps):        
        pin_step.high()
        time.sleep_us(100)
        pin_step.low()
        time.sleep_us(100)
    pin_en.high()
    print("STOP")

pin_led  = Pin(2)

pin_srv  = Pin(5)
srv = PWM(pin_srv, freq=50, duty=0)

pin_dir  = Pin(14)
pin_step = Pin(13)
pin_en   = Pin(0)

pin_led.init(Pin.OUT)
pin_en.init(Pin.OUT)
pin_dir.init(Pin.OUT)
pin_step.init(Pin.OUT)

def turndeg(dir,degs):
    microstep = 16
    degs_per_step = 1.8
    numsteps = degs * microstep / degs_per_step
    dostep(dir,numsteps)

turndeg(1,360)
