from machine import Pin, PWM, I2C
import time

def srv_us(us):
    srv.duty(us*1024*50//1000000)

print("Hello!")

pin_srv  = Pin(5)
srv = PWM(pin_srv, freq=50, duty=0)

pin_dir  = Pin(14)
pin_step = Pin(13)
pin_en   = Pin(0)

pin_sda = Pin(12)
pin_scl = Pin(16)
i2c = I2C(scl=pin_scl, sda=pin_sda, freq=100000)

pin_led  = Pin(2)

#while(1):
#    print(".")
#    time.sleep(1)

pin_led.init(Pin.OUT)
pin_en.init(Pin.OUT)
pin_dir.init(Pin.OUT)
pin_step.init(Pin.OUT)

pin_led.high()
pin_en.low()
pin_dir.low()

dir = 0

# TODO:
# caps on Vmot, 3V3
# GY-80 IMU

while(1):
    print("spin!")
    if dir == 1:
        pin_dir.high()
    else:
        pin_dir.low()
    time.sleep_ms(500)
    for i in range(0,2):
        srv_us(1000)
        time.sleep_ms(250)
        srv_us(2000)
        time.sleep_ms(250)
    time.sleep_ms(500)
    pin_en.low()
    for i in range(0,500):        
        pin_led.low()
        pin_step.high()
        #print("HIGH")
        time.sleep_us(100)
        pin_step.low()
        pin_led.high()
        #print("LOW")
        time.sleep_us(100)
    pin_en.high()
    print("wait...")
    time.sleep(1)
    dir = 1 - dir

#srv_us(1500)

# PWM pins:
# 0, 2, 4, 5, 12, 13, 14   
