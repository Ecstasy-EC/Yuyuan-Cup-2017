#include <LobotServoController.h>
#include <math.h>
LobotServoController myse(Serial1);

void extend_shovel_and_turn(void);
void slightly_move_forward(void);
void stop_move(void);
void slightly_move_back(void);

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
  extend_shovel_and_turn();
}

void loop() {
  // put your main code here, to run repeatedly:

}

void extend_shovel_and_turn()
{
  delay(500);
  myse.moveServos(2,2000,3,2420,4,400);
  delay(2000);
  slightly_move_forward();
  delay(3000);
  stop_move();
  myse.moveServo(1,2400,1000);
  delay(1000);
  myse.moveServo(2,1500,1000);
  delay(1000);
  myse.moveServo(1,2200,1000);
  delay(1000);
  slightly_move_back();
  delay(1000);
  stop_move();
}

void slightly_move_forward(){
  
    analogWrite(9,50);   //Left  Motor Speed (back)
    analogWrite(10,50);  //Right Motor Speed (back)
    analogWrite(11,50);  //Left  Motor Speed (front)
    analogWrite(12,50);  //Right Motor Speed (front)

    digitalWrite(4,LOW);  //(back)   forward
    digitalWrite(5,HIGH);   //(back)
    digitalWrite(6,HIGH);  //(back) 
    digitalWrite(7,LOW);  //(back)

    digitalWrite(24,LOW); //(front)
    digitalWrite(25,HIGH);  //(front)
    digitalWrite(26,HIGH);  //(front)
    digitalWrite(27,LOW); //(front)
  }

  void stop_move(){
    analogWrite(9,0);   //Left  Motor Speed (back)
    analogWrite(10,0);  //Right Motor Speed (back)
    analogWrite(11,0);  //Left  Motor Speed (front)
    analogWrite(12,0);  //Right Motor Speed (front)

    digitalWrite(4,LOW);  //(back)
    digitalWrite(5,LOW);   //(back)
    digitalWrite(6,LOW);   //(back)
    digitalWrite(7,LOW);  //(back)

    digitalWrite(24,LOW); //(front)
    digitalWrite(25,LOW);  //(front)
    digitalWrite(26,LOW);  //(front)
    digitalWrite(27,LOW); //(front)
}

void slightly_move_back(){
    
    analogWrite(9,50);   //Left  Motor Speed (back)
    analogWrite(10,50);  //Right Motor Speed (back)
    analogWrite(11,50);  //Left  Motor Speed (front)
    analogWrite(12,50);  //Right Motor Speed (front)

    digitalWrite(4,HIGH);  //(back)   back
    digitalWrite(5,LOW);   //(back)
    digitalWrite(6,LOW);  //(back) 
    digitalWrite(7,HIGH);  //(back)

    digitalWrite(24,HIGH); //(front)
    digitalWrite(25,LOW);  //(front)
    digitalWrite(26,LOW);  //(front)
    digitalWrite(27,HIGH); //(front)
}

