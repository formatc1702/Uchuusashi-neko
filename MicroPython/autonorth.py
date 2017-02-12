from machine import Pin, PWM, I2C
from math    import pi, atan2
import ustruct
import time

def srv_us(us):
    srv.duty(us*1024*50//1000000)

def mag_raw():
    buf = i2c.readfrom_mem(mag_addr, mag_data, 6)
#    print(buf)
    x = ustruct.unpack("<h",bytes([buf[0],buf[1]]))[0]
    z = ustruct.unpack("<h",bytes([buf[2],buf[3]]))[0]
    y = ustruct.unpack("<h",bytes([buf[4],buf[5]]))[0]
    return x,y,z

def mag_heading():
    raw = mag_raw()
    heading = 180.0 * atan2(raw[1],raw[0]) / pi
    return heading

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

print("Hello!")

pin_led  = Pin(2)

pin_srv  = Pin(5)
srv = PWM(pin_srv, freq=50, duty=0)

pin_dir  = Pin(14)
pin_step = Pin(13)
pin_en   = Pin(0)

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

pin_led.init(Pin.OUT)
pin_en.init(Pin.OUT)
pin_dir.init(Pin.OUT)
pin_step.init(Pin.OUT)

pin_led.high() # led OFF
pin_en.high()  # stepper OFF
pin_dir.low()

i2c.writeto_mem(mag_addr, mag_cra, bytes([0x70]))
i2c.writeto_mem(mag_addr, mag_crb, bytes([0x40]))
i2c.writeto_mem(mag_addr, mag_mode, bytes([mag_cont]))

dir = 0

while(1):
    heading = 0
    for i in range(0,10):
        _heading = mag_heading()
        heading = heading + _heading
        time.sleep_ms(100)
    heading = heading / 10
    print(heading)
    if abs(heading) > 5:
        if heading < 0:
            print("neg")
            dostep(1,10)
        else:
            print("pos")
            dostep(-1,10)
        step_off()
        time.sleep(1)
    else:
        print("ok")
    time.sleep_ms(100)

