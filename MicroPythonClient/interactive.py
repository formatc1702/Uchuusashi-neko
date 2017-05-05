from machine import Pin, I2C, PWM
from hmc5883l import HMC5883L
from stepper import Stepper
import utime as time
import spaceclient as sc

# Servo
pin_srv  = Pin(5)
srv = PWM(pin_srv, freq=50, duty=0)

def srv_us(us):
    srv.duty(us*1024*50//1000000)

def srv_deg(deg):
    # 0 deg = 1000, 90 deg = 1500, 180 deg = 2000
    #us = round(1000 + deg * 1000.0 / 180.0)
    #us = round(2000 - deg * 1000.0 / 90.0)
    us = round(1550 - deg *  900.0 / 90.0)
    srv_us(us)

def st_deg(degree):
    steppy.target    = steppy.deg_to_steps(degree)
    while(steppy.pos != steppy.target):
        _ = steppy.run()

# Stepper
pin_dir  = Pin(14)
pin_step = Pin(13)
pin_en   = Pin(0)
steppy   = Stepper(pin_en, pin_dir, pin_step)
steppy.on()
steppy.max_speed = 10000
steppy.acc       = 5

# srv_deg(90)
# time.sleep(2)
# srv_deg(0)
# time.sleep(2)
