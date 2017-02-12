#include <Servo.h>

Servo Ude;
const int pin_ude = 6;

void setup() {
  // put your setup code here, to run once:
  Ude.attach(pin_ude);
  Serial.begin(9600);
//  Ude.write(90);
//  delay(5000);
}

void loop() {
  // put your main code here, to run repeatedly:
  /* 
  int rnd = random(0,180);
  Serial.println(rnd);
  Ude.write(rnd);
  delay(1000);
  // */
  /*
  for(int i = 0; i < 180; i++) {
    Ude.write(i);
    delay(5);
  }
  for(int i = 180; i > 0; i--) {
    Ude.write(i);
    delay(5);
  }
  // */
  Ude.write(0);
  delay(1000);
  Ude.write(90);
  delay(1000);
  Ude.write(180);
  delay(1000);
  Ude.write(90);
  delay(1000);
}
