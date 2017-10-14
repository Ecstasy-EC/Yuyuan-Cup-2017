#include <LobotServoController.h>
#include <math.h>

LobotServoController myse(Serial1);
void catch_block(double dist1);
void release_block(void);
void spin_servo2(void);

void setup() {
  Serial1.begin(9600);
  myse.moveServos(4,2000,1,1500,2,1500,3,1000,4,2000); //舵机初始化
  double dist1=100.0;
  catch_block(dist1);
  delay(2000);
  release_block();
  //spin_servo2();
}

void loop() {
}

void catch_block(double dist1)
{
  double x=dist1+36.5;
  double a,b,c;
  double pi=3.1415926;
  int n3,n4;
  a=49.0+52.0;
  b=88.52;
  c=sqrt(33.0*33.0+135.0*135.0);//initial 33 128.19
  n3=int(1500-2000.0*(pi-acos(33.0/c)-acos((b*b+c*c-a*a-x*x)/(2*b*c)))/pi);
  n4=int(1500-2000*(pi-acos(a/sqrt(x*x+a*a))-acos((b*b+a*a+x*x-c*c)/(2*b*sqrt(x*x+a*a))))/pi);
  delay(2000);
  myse.moveServos(2,1000,3,n3,4,n4);
  delay(1000);
  myse.moveServo(1,2200,1000);
  delay(1000);
  myse.moveServos(2,1000,3,1000,4,2000); 
}

void release_block(void)
{
  myse.moveServos(2,1000,3,2000,4,700);
  delay(1000);
  myse.moveServo(1,1500,1000);
  delay(1000);
}

void spin_servo2()
{
  myse.moveServos(2,1000,3,2000,4,700);
  delay(2000);
  myse.moveServo(2,2500,1000);
  delay(1000);
}
