from machine import Pin, I2C, PWM, Timer
from stepper import Stepper
import utime as time

pin_dir  = Pin(14)
pin_step = Pin(13)
pin_en   = Pin(0)


steppy  = Stepper(pin_en, pin_dir, pin_step)

steppy.on()
steppy.max_speed = 10000
steppy.acc       = 5
for i in range(0,60):
    steppy.target    = 1000
    while(steppy.pos != steppy.target):
        _ = steppy.run()
    steppy.off()
    time.sleep(1.0)
    
    steppy.target    = 0
    while(steppy.pos != steppy.target):
        _ = steppy.run()
    steppy.off()
    time.sleep(1.0)
    
print("Done!")

#pwm = PWM(pin_step)
#
#pwm.freq(1000)
#pwm.duty(512)
#time.sleep(1.0)
#pwm.duty(0)
#
#for i in range(0,10000):
#    steppy.dostep(1)
#    time.sleep_us(1)
#
steppy.off()
