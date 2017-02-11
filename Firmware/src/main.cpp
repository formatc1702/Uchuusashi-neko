#include <Arduino.h>
#include <Servo.h>

Servo Arm;

#define PIN_SERVO A1

#define PIN_STEPPER_DIR  4
#define PIN_STEPPER_STEP 5
#define PIN_STEPPER_EN   6

int STEPDIR = 0;

void setup() {
  pinMode(PIN_STEPPER_DIR,  OUTPUT);
  pinMode(PIN_STEPPER_STEP, OUTPUT);
  pinMode(PIN_STEPPER_EN,   OUTPUT);
  Arm.attach(PIN_SERVO);

  digitalWrite(PIN_STEPPER_EN, LOW);
}

void loop() {
  STEPDIR = 1 - STEPDIR;
  digitalWrite(PIN_STEPPER_DIR, STEPDIR);
  Arm.write(STEPDIR * 150 + 15);
  for (size_t i = 0; i < 2000; i++) {
    digitalWrite(PIN_STEPPER_STEP, HIGH);
    // delayMicroseconds(1);
    digitalWrite(PIN_STEPPER_STEP, LOW);
    delayMicroseconds(500);
  }
  delay(250);
}
