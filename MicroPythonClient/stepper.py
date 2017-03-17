from machine import Pin
import utime as time

class Stepper:
    # Using code ported from Adafruit's AccelStepper Fork
    # https://github.com/adafruit/AccelStepper
    def __init__(self, pin_en, pin_dir, pin_step):
        self.pin_en   = pin_en
        self.pin_dir  = pin_dir
        self.pin_step = pin_step

        self.pos = 0
        self.target = 0
        self.speed = 0
        self.max_speed = 1.0
        self.acc = 1.0
        self.step_interval = 0
        self.last_steptime = 0

        self.pin_en.init(Pin.OUT)
        self.pin_dir.init(Pin.OUT)
        self.pin_step.init(Pin.OUT)
        self.off()

    def on(self):
        self.pin_en.low()

    def off(self):
        self.pin_en.high()

    def dostep(self, dir, numsteps=1):
        self.on()
        if dir == 1:
            self.pin_dir.high()
        else:
            self.pin_dir.low()
        for i in range(0,numsteps):
            self.pin_step.high()
            time.sleep_us(2)
            self.pin_step.low()
            time.sleep_us(2)

    def turndeg(self, dir, degs):
        microstep = 16
        degs_per_step = 1.8
        numsteps = degs * microstep / degs_per_step
        self.dostep(dir,numsteps)

    def move_abs(self, target):
        self.target = target
        self.compute_new_speed()

    def move_rel(self, target):
        self.move_abs(self.pos + target)

    def run_speed(self, now):
        if now > self.last_steptime + self.step_interval:
            if self.speed > 0:
                self.pos += 1
            elif speed < 0
                self.pos -= 1
            self.step(1)
            self.last_steptime = now
            return True
        else
            return False

    def dist_to_go(self):
        return self.target - self.pos

    def compute_new_speed(self):
        self.set_speed(self.desired_speed())

    def desired_speed(self):
        togo = self.dist_to_go()
        if togo > 0
            required_speed =  sqrt(2.0 *  togo * self.acc)
        elif togo < 0
            required_speed = -sqrt(2.0 * -togo * self.acc)
        else: # togo == 0
            return 0.0
        if required_speed > self.speed:
            if self.speed == 0:
                required_speed = sqrt(2.0 * self.acc)
            else:
                required_speed = self.speed + abs(self.acc / self.speed)
            if required_speed > self.max_speed:
                required_speed = self.max_speed
        elif required_speed < self.speed:
            if self.speed == 0:
                required_speed = -sqrt(2.0 * self.acc)
            else
                required_speed = self.speed - abs(self.acc / self.speed)
            if required_speed < -self.max_speed:
                required_speed = -self.max_speed
        return required_speed

    def run(self):
        if self.target == self.pos:
            return False
        if self.run_speed():
            self.compute_new_speed()
        return True

    def set_max_speed(self, speed):
        self.max_speed = speed
        self.compute_new_speed()

    def set_acc(self, acc):
        self.acc = acc
        self.compute_new_speed()

    def set_speed(self, speed):
        self.speed = speed
        self.step_interval = abs(1000.0 / speed)

    def run_to_pos(self):
        while(self.run()):
            pass

    def run_speed_to_pos(self, now):
        if self.target == self.pos:
            return False
        else:
            self.run_speed(now)
