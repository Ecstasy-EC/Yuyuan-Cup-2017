#include<math.h>
#include <LobotServoController.h>

LobotServoController myse(Serial1);

int initial_motor_speed=50;                      //电机初速度

void slightly_turn_left(void);
void slightly_turn_right(void);
void slightly_move_forward(void);
void slightly_move_back(void);
void adjust_orientation(float Y);                //单位cm
void adjust_distance(float X);                   //单位cm
void stop_move(void);                            //电机停止转动
void catch_block(double dist1);                  //抓木块
void release_block(void);                        //放木块

int A = 0, B = 0;
float X = 0, Y = 0;                              //单位cm
char message_received[14];
int dealt_message_received[14];

void SendSignal(){
/*  if (count_for_crossroad == A)*/
    Serial2.println("A");    //A和B由参数count_for_crossroad确定
/*  if (count_for_crossroad == B)  
    Serial2.println("B");*/
}

void ReceiveMessage(){
  if (Serial2.available())
  {
    for (int i = 0; i <= 13; i++)
      message_received[i] = Serial2.read();
  }
}

void UncodeMessage(){  //XX.XXX ±XX.XXX

  dealt_message_received[0] = message_received[0] - 48;
  dealt_message_received[1] = message_received[1] - 48;
  dealt_message_received[2] = '.';
  dealt_message_received[3] = message_received[3] - 48;
  dealt_message_received[4] = message_received[4] - 48;
  dealt_message_received[5] = message_received[5] - 48;
  dealt_message_received[6] = ' ';
  dealt_message_received[7] = message_received[7]; //+ 43 - 45
  dealt_message_received[8] = message_received[8] - 48;
  dealt_message_received[9] = message_received[9] - 48;
  dealt_message_received[10] = '.';
  dealt_message_received[11] = message_received[11] - 48;
  dealt_message_received[12] = message_received[12] - 48;
  dealt_message_received[13] = message_received[13] - 48;

  X = dealt_message_received[0] * 10 + dealt_message_received[1] + dealt_message_received[3] * 0.1 + dealt_message_received[4] * 0.01 + dealt_message_received[5] * 0.001;
  Y = dealt_message_received[8] * 10 + dealt_message_received[9] + dealt_message_received[11] * 0.1 + dealt_message_received[12] * 0.01 + dealt_message_received[13] * 0.001;
  if (dealt_message_received[7] == '-')
    Y = -Y;

}

void BlueTooth(){
  SendSignal();
  delay(100);
  ReceiveMessage();
  UncodeMessage();
  delay(100);
  }

void setup(){
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
 Serial1.begin(9600); //舵机驱动板
 Serial2.begin(9600); //Enable Serial Communications
 myse.moveServos(4,2000,1,2000,2,2500,3,1200,4,2000); //舵机初始化
  
 }
 
void loop(){
 while (Y<1e-5){ 
  BlueTooth();
 }
 
 while((abs(Y)-0.8)>1e-12)                       //如果在可允许的误差外
 {
  adjust_orientation(Y);
  delay(300);
  BlueTooth();                   //再读Y
  } 

  while((X-8.0)<=(1e-5)||((X-14.0)>=(1e-5))){
   adjust_distance(X);
   delay(500);
   BlueTooth();
  }
  
  catch_block(X);
  delay(2000);
  release_block();
}

void catch_block(double dist1){
  double x=dist1+36.5;
  double a,b,c;
  double pi=3.1415926;
  int n3,n4;
  a=69.0+52.0;//initial 49
  b=88.52;
  c=sqrt(129.0*129.0+53.5*53.5);//initial 129.0 53.5
  n3=int(1500+2000.0*(-acos(53.5/c)+acos((b*b+c*c-a*a-x*x)/(2*b*c)))/pi);
  n4=int(1500-2000*(pi-acos(a/sqrt(x*x+a*a))-acos((b*b+a*a+x*x-c*c)/(2*b*sqrt(x*x+a*a))))/pi);
  //Serial.println(n3);
  //Serial.println(n4);
  delay(2000);
  myse.moveServos(2,1000,3,n3,4,n4);
  delay(1000);
  /*myse.moveServo(3,n3,1000);
  delay(1000);
  myse.moveServo(4,n4,1000);
  delay(1000);
  */
  myse.moveServo(1,2600,1000);
  delay(1000);
  myse.moveServos(2,1000,3,1200,4,2000); 
}

void release_block(void){
  myse.moveServos(2,1000,3,2100,4,600);
  delay(1000);
  myse.moveServo(1,2000,1000);
  delay(1000);
}


void adjust_orientation(float Y) {        //左正右负
  float kt=1.0;                          //比例系数kt需要调节
  if(Y>0)
  {
    slightly_turn_left();
    delay(Y*kt);
    stop_move();
    delay(200);
  }
  else
  {
    slightly_turn_right();
    delay((-1)*Y*kt);
    stop_move();
    delay(200);
  }
}

void adjust_distance(float X){
  float kt=1.0;                          //比例系数kt需要调节
  if(X>10)
  {
    slightly_move_back();
    delay((X-14.0)*kt);
    stop_move();
    delay(300);
  }
  else
  {
    slightly_move_forward();
    delay((8.0-X)*kt);
    stop_move();
    delay(300);
  }
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

void slightly_turn_left(){
    analogWrite(9,50);   //Left  Motor Speed (back)
    analogWrite(10,50);  //Right Motor Speed (back)
    analogWrite(11,50);  //Left  Motor Speed (front)
    analogWrite(12,50);  //Right Motor Speed (front)

    digitalWrite(4,HIGH);  //(back)   turn left
    digitalWrite(5,LOW);   //(back)
    digitalWrite(6,HIGH);  //(back) 
    digitalWrite(7,LOW);  //(back)

    digitalWrite(24,HIGH); //(front)
    digitalWrite(25,LOW);  //(front)
    digitalWrite(26,HIGH);  //(front)
    digitalWrite(27,LOW); //(front)
}

void slightly_turn_right(){
  
    analogWrite(9,50);   //Left  Motor Speed (back)
    analogWrite(10,50);  //Right Motor Speed (back)
    analogWrite(11,50);  //Left  Motor Speed (front)
    analogWrite(12,50);  //Right Motor Speed (front)

    digitalWrite(4,LOW);  //(back)   turn right
    digitalWrite(5,HIGH);   //(back)
    digitalWrite(6,LOW);  //(back) 
    digitalWrite(7,HIGH);  //(back)

    digitalWrite(24,LOW); //(front)
    digitalWrite(25,HIGH);  //(front)
    digitalWrite(26,LOW);  //(front)
    digitalWrite(27,HIGH); //(front)
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

