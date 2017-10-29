#include <LobotServoController.h>
#include <math.h>
LobotServoController myse(Serial1);

void setup() {
 pinMode(9,OUTPUT);  //PWM Pin 1    (back)
 pinMode(10,OUTPUT); //PWM Pin 2    (back)
 pinMode(4,OUTPUT); //Left  Motor Pin 1   (back)
 pinMode(5,OUTPUT); //Left  Motor Pin 2   (back)
 pinMode(6,OUTPUT); //Right Motor Pin 1   (back)
 pinMode(7,OUTPUT); //Right Motor Pin 2   (back)
 pinMode(11,OUTPUT); //PWM Pin 1    (front)
 pinMode(12,OUTPUT); //PWM Pin 2    (front)
 pinMode(24,OUTPUT); //Left  Motor Pin 1   (front)
 pinMode(25,OUTPUT); //Left  Motor Pin 2   (front)
 pinMode(26,OUTPUT); //Right Motor Pin 1   (front)
 pinMode(27,OUTPUT); //Right Motor Pin 2   (front)
  Serial1.begin(9600);
  myse.moveServos(4,2000,1,2000,2,2500,3,1200,4,2000); //舵机初始化
  delay(2000);
  myse.moveServo(1,2600,1000);
  delay(1000);
  myse.moveServo(4,800,1000);
  delay(1000);
  myse.moveServo(3,2000,2000); //舵机初始化
  delay(2000);
}

void loop() {
  // put your main code here, to run repeatedly:

}

