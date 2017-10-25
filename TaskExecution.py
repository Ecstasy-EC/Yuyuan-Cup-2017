from Communication import *
from CubeRecog import *

COM=12
Baud=9600
print("通讯端口:%d   波特率%d" % (COM,Baud))
ser=Connect(COM,Baud)
print("通讯已建立\n")
print("7秒后开始进入识别模式，请尽快调整好窗口位置...")
time.sleep(7)
while (1):
    im=ImageGrab.grab((5,46,900,570))
    im.save('1.jpg')
    origin=cv2.imread('1.jpg')
	C=Catch(ser)
	mes=''
	DistR=0
	LocR=0
	if C=='A':
		DistR,LocR=RedScan(origin)
		Dist_S=str(round(DistR,3))
		Loc_S=str(round(abs(LocR),3))
	elif C=='B'
		DistR,LocR=BlackScan(origin)
		Dist_S=str(round(DistR,3))
		Loc_S=str(round(abs(LocR),3))
	if (DistR==0) and (LocR==0):
		continue
	if LocR<10:
		Loc_S='0'+Loc_S
	if LocR>=0:
		Loc_S='+'+Loc_S
	else:
		Loc_S='-'+Loc_S
	mes=Dist_S+' '+Loc_S		
	print(C,mes)
	Send(ser,mes)
	time.sleep(0.2)
	if cv2.waitKey(1) & 0xFF==ord(' '):
    	break 

