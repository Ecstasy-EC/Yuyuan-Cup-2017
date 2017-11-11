from Communication import *
from CubeRecog import *
import scipy.io as sio


def save(img):
    b=img[:,:,0]
    g=img[:,:,1]
    r=img[:,:,2]
    sio.savemat('RunninData.mat',{'b':b,'g':g,'r':r})
    return

COM=12
Baud=9600

print("通讯端口:%d   波特率%d" % (COM,Baud))
ser=Connect(COM,Baud)
print("通讯已建立\n")
print("5秒后开始进入识别模式，请尽快调整好窗口位置...")
time.sleep(5)
while (1):
    im=ImageGrab.grab((5,46,900,570))
    im.save('1.jpg')
    origin=cv2.imread('1.jpg')
    save(origin)
    C=Catch(ser)
    if C=='S':
        C=''
        time.sleep(0.2)
        continue
    mes=''
    DistR=0
    LocR=0
    Dist_S=str(round(DistR,3))
    Loc_S=str(round(abs(LocR),3))    
    if C=='A':
        DistR,LocR,TP=Select(origin)
        Dist_S=str(round(DistR,3))
        Loc_S=str(round(abs(LocR),3))
    elif C=='B':
        DistR,LocR,TP=Select(origin)
        Dist_S=str(round(DistR,3))
        Loc_S=str(round(abs(LocR),3))
    if (DistR==0) and (LocR==0):
        print('Not Received')
        continue
    if LocR<10:
        Loc_S='0'+Loc_S
    if LocR>=0:
        Loc_S='+'+Loc_S
    else:
        Loc_S='-'+Loc_S
    if DistR<10:
        Dist_S='0'+Dist_S
    while len(Dist_S)<6:
        Dist_S=Dist_S+'0'
    while len(Loc_S)<6:
        Loc_S=Loc_S+'0'
    mes=Dist_S+' '+Loc_S+TP		
    print(C,mes)
    Send(mes,ser)
    time.sleep(0.2)
    C=''
    if cv2.waitKey(1) & 0xFF==ord(' '):
        break 

