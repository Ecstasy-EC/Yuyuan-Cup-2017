import cv2
import time
from numpy import *
from PIL import ImageGrab
from matplotlib import pyplot as plt


#Adapatable Constant:
#Size of Kernel_Canny
#Range of HSV GrayFilter
#Accpetable length of undetected pixels in GrayScan
#Height Detection Terminating Ratio

#Constant Settings
Kernel=cv2.getStructuringElement(cv2.MORPH_RECT,(6,6))
Kernel_Canny=cv2.getStructuringElement(cv2.MORPH_RECT,(3,3))
F=978.75
Detect_Ratio=0.5
AC_Length=30

#Color Histogram
def CH_Plot(img):
    Color=('b','g','r')
    for i,col in enumerate(Color):
        Hist=cv2.calcHist([img],[i],None,[256],[0,256])
        plt.plot(Hist,Color=col)
    plt.xlim([0,256])
    plt.show()

#Cube Filter
def GreenFilter(RGB):
    lower_red=array([40,80,30])
    upper_red=array([90,130,62])
    mask1=cv2.inRange(RGB,lower_red,upper_red)
    mask=cv2.dilate(mask1,Kernel)
    #cv2.imshow('mask',mask)
    return mask1

def RedFilter(RGB):
    lower_red=array([0,0,100])
    upper_red=array([85,85,255])
    mask1=cv2.inRange(RGB,lower_red,upper_red)
    mask=cv2.dilate(mask1,Kernel)
    #cv2.imshow('mask',mask)
    return mask1

def BlueFilter(RGB):
    lower_red=array([90,60,20])
    upper_red=array([160,102,80])
    mask1=cv2.inRange(RGB,lower_red,upper_red)
    mask=cv2.dilate(mask1,Kernel)
    #cv2.imshow('mask',mask)
    return mask1


#Draw Rectangle

def DrawRect(Points,img):
    cv2.rectangle(img,tuple(Points[0]),tuple(Points[2]),(0,0,255))

#Cube Scan

def Scan(Filter,origin):
    F1=Filter(origin)
    res=cv2.bitwise_and(origin,origin,mask=F1)
    img_cp=F1.copy()
    _,cnts,_=cv2.findContours(img_cp,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    if len(cnts)==0: return (1000000,0)
    cnt_fst=sorted(cnts,key=cv2.contourArea,reverse=True)[0]
    box=cv2.minAreaRect(cnt_fst)
    Points=int0(cv2.boxPoints(box))
    cv2.rectangle(origin,tuple(Points[0]),tuple(Points[2]),(255,255,255))    
    #Distance Calculation
    Pix=Points[:,1].max()-Points[:,1].min()
    Dist=CalcDist(Pix)
    #Location Calculation
    D=Points[:,1].min()
    H=Points[:,1].max()
    Lx=Points[:,0].min()
    Rx=Points[:,0].max()
    Rect_Mid=(Lx+Rx)/float(2)
    m,n,_=shape(origin)
    Mid=n/float(2)       
    Loc=CalcLoc(Rect_Mid-Mid,H-D)
    #print("Distance: ",Dist,'Loc: ',Loc)
    return Dist,Loc
    #print(CalcF(H-D,15))

#Select Cube

def Select(origin):
    D=zeros((1,3))
    L=zeros((1,3))
    tps=['R','G','B']
    D[0,0],L[0,0]=Scan(RedFilter,origin)
    D[0,1],L[0,1]=Scan(GreenFilter,origin)
    D[0,2],L[0,2]=Scan(BlueFilter,origin)
    num=argmin(D)
    #print(tps[num])
    return(D[0,num],L[0,num],tps[num])

#Calculation
def CalcF(Pix,Dist):
    return (Pix*Dist/4)

def CalcDist(Pix):
    return (4*F/Pix)

def CalcLoc(Pix,Len):
    if Len==0:Len=1
    return (4*Pix/float(Len)-2.25)

# main

if __name__=='__main__':
    print("进入图像测试......y:结束测试")
    while (1):
        im=ImageGrab.grab((5,46,900,570))
        im.save('1.jpg')
        origin=cv2.imread('1.jpg')
        cv2.imshow('origin',origin)
        if cv2.waitKey(1) & 0xFF==ord('y'):
            break    
        #time.sleep(0.5)
    cv2.destroyAllWindows()    

    print("5秒后进入物体识别模式......Space:结束识别")
    time.sleep(1)
    while (1):
        im=ImageGrab.grab((5,46,900,570))
        im.save('1.jpg')
        origin=cv2.imread('1.jpg')
        Select(origin)
        cv2.imshow('Result',origin)
        if cv2.waitKey(1) & 0xFF==ord(' '):
            break    
        #time.sleep(0.5)
    cv2.destroyAllWindows()    
    

