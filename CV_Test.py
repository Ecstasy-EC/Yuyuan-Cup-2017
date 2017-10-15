import cv2
import time
from numpy import *
from PIL import ImageGrab
from matplotlib import pyplot as plt

Kernel=cv2.getStructuringElement(cv2.MORPH_RECT,(7,7))
#Color Histogram
F=993.95

def CH_Plot(img):
    Color=('b','g','r')
    for i,col in enumerate(Color):
        Hist=cv2.calcHist([img],[i],None,[256],[0,256])
        plt.plot(Hist,Color=col)
    plt.xlim([0,256])
    plt.show()

#Red Cube Filter
def RedFilter(RGB):
    lower_red=array([0,0,100])
    upper_red=array([85,85,255])
    mask1=cv2.inRange(RGB,lower_red,upper_red)
    mask=cv2.dilate(mask1,Kernel)
    return mask1

def GreyFilter(RGB):
    lower_grey=array([115,115,115])
    upper_grey=array([155,155,155])
    mask1=cv2.inRange(RGB,lower_grey,upper_grey)
    mask=cv2.dilate(mask1,Kernel)
    return mask1

def Draw(Points,img):
    cv2.rectangle(img,tuple(Points[0]),tuple(Points[2]),(0,0,255))

def GrayScan(img):
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    B=gray>0
    n,m=shape(B)
    SumRec=0
    for i in range(1,n):
        tmp=sum(B[n-i,:])
        if tmp>100:
            if tmp>=SumRec:
                SumRec=tmp
            else:
                break
    l=n-i+1
    line=B[l,:]
    Lx=0
    SumRec=0
    tmp=0
    for i in range(len(line)):
        if line[i]>0:
            tmp+=1
        else:
            if tmp>=SumRec:
                SumRec=tmp
                Lx=i-SumRec
            tmp=0
    Rx=Lx+SumRec
    length=SumRec
    for i in range(1,l):
        tmp=sum(B[l-i,Lx:Rx])
        if tmp/float(length)<0.05:
            break
    d=l-i
    Draw([[Lx,d],[Lx,l],[Rx,l],[Rx,d]],img)

    
def Key_Points(img):
    img_cp=img.copy()
    _,cnts,_=cv2.findContours(img_cp,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    if len(cnts)==0: return [[0,0],[0,0],[0,0],[0,0]]
    Sorted_Contours=sorted(cnts,key=cv2.contourArea,reverse=True)
    PQ=[]
    for i in range(len(cnts)):
        PQ.append(int0(cv2.boxPoints(cv2.minAreaRect(Sorted_Contours[i]))))
    S=0
    for i in range(len(PQ)):
        Points=PQ[i]
        d=Points[:,1].max()-Points[:,1].min()
        l=Points[:,0].max()-Points[:,0].min()
        print(d,l,d*l)
        Draw(Points,img)
    cnt_fst=Sorted_Contours[0]
    box=cv2.minAreaRect(cnt_fst)
    return int0(cv2.boxPoints(box))

#Focus Calculation
def CalcF(Pix,Dist):
    return (Pix*Dist/4)

def Test():
    for i in range(10,41):
        origin=cv2.imread('imgsave\Red_%dcm_4.jpg' % i)
        #cv2.imshow('origin',origin)
        #CH_Plot(origin)
        F1=RedFilter(origin)
        Points=Key_Points(F1)
        res=cv2.bitwise_and(origin,origin,mask=F1)
        Draw(Points,res)
        Pix=Points[:,1].max()-Points[:,1].min()
        Dist=4*F/Pix
        print("Acutal: %d cm; Recognition: %f cm; Error: %f cm" % (i,Dist,i-Dist))
        cv2.imshow('Res',res)
        if cv2.waitKey(1) & 0xFF==ord(' '):
            break    
        time.sleep(0.5)
    cv2.destroyAllWindows()    

test=cv2.imread('imgsave\GreySample.jpg')
origin=cv2.imread('10cm_0.jpg')
#print(shape(origin))
cv2.imshow('origin',origin)
#cv2.imshow('test',test)
#CH_Plot(origin)
#CH_Plot(test)

F1=GreyFilter(origin)
#Points=Key_Points(F1)
res=cv2.bitwise_and(origin,origin,mask=F1)
GrayScan(res)
#Draw(Points,res)
#Pix=Points[:,1].max()-Points[:,1].min()
#Dist=4*F/Pix
#print("Recognition: %f cm" % (Dist))
cv2.imshow('Res',res)
