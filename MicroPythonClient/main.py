import network
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

# I2C + Compass
# pin_sda = Pin(12)
# pin_scl = Pin(16)
# i2c = I2C(scl=pin_scl, sda=pin_sda, freq=100000)
# compass = HMC5883L(i2c)
# compass.offset_x = 400
# compass.offset_y = -45

# Connect to WiFi
wifi_config = open('wificonfig.txt','r')
my_ap = wifi_config.readline().rstrip()
my_pw = wifi_config.readline().rstrip()
wifi_config.close()
wlan = network.WLAN(network.STA_IF)
wlan.active(True)
wlan.connect(my_ap, my_pw)
for i in range(0,60): # attempt to connect
    ip,mask,gateway,dns = wlan.ifconfig()
    if ip == '0.0.0.0': #not connected
        print('.')
        time.sleep(1)
    else: #connected!
        print('Got IP: ', ip)
        tle = sc.get_tle_from_url(sc.tle_src, 'ISS (ZARYA)')
        print(tle)
        while(True):
            (alt, az) = sc.get_alt_az_from_tle_and_location(tle, 'Berlin')
            print("ALT: {}\t AZ: {}".format(round(alt,1), round(az,1)))
            srv_deg(alt) # because direction is reversed
            steppy.target    = steppy.deg_to_steps(az)
            while(steppy.pos != steppy.target):
                _ = steppy.run()
            time.sleep(3)
