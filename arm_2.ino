#include <LobotServoController.h>
#include <math.h>

LobotServoController myse(Serial1);
void catch_block(double dist1);
void release_block(void);

void setup() {
  // put your setup code here, to run once:
  Serial1.begin(9600);
  myse.moveServos(4,2000,1,2000,2,2500,3,1200,4,2000); //舵机初始化
  double dist1=80.0;
  catch_block(dist1);
  delay(2000);
  release_block();
}

void loop() {
}

void catch_block(double dist1)
{
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

void release_block(void)
{
  myse.moveServos(2,1000,3,2200,4,700);
  delay(1000);
  myse.moveServo(1,2000,1000);
  delay(1000);
}
