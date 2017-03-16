from machine import Pin
import utime as time

class Stepper:
    def __init__(self, pin_en, pin_dir, pin_step):
        self.pin_en   = pin_en
        self.pin_dir  = pin_dir
        self.pin_step = pin_step
        self.pin_en.init(Pin.OUT)
        self.pin_dir.init(Pin.OUT)
        self.pin_step.init(Pin.OUT)
        self.off()

    def on(self):
        self.pin_en.low()

    def off(self):
        self.pin_en.high()

    def dostep(self, dir, numsteps):
        self.on()
        if dir == 1:
            self.pin_dir.high()
        else:
            self.pin_dir.low()
        for i in range(0,numsteps):
            self.pin_step.high()
            time.sleep_us(2)
            self.pin_step.low()
            time.sleep_us(2000)

    def turndeg(self, dir, degs):
        microstep = 16
        degs_per_step = 1.8
        numsteps = degs * microstep / degs_per_step
        self.dostep(dir,numsteps)
