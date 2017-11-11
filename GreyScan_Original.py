
def BlackScan(origin):
    F1=BlackFilter(origin)
    res=cv2.bitwise_and(origin,origin,mask=F1)
    img_cp=F1.copy()
    _,cnts,_=cv2.findContours(img_cp,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)
    if len(cnts)==0: return [[0,0],[0,0],[0,0],[0,0]]
    cnt_fst=sorted(cnts,key=cv2.contourArea,reverse=True)[0]
    box=cv2.minAreaRect(cnt_fst)
    Points=int0(cv2.boxPoints(box))
    Lx=Points[:,0].min()
    Rx=Points[:,0].max()
    H=Points[:,1].max()
    B=F1>0
    length=Rx-Lx+1
    i=0
    for i in range(int((length)/2),H):
        tmp=sum(B[H-i,:])
        if tmp/float(length)<0.75:
            break
    if i==0:
        return
    D=H-i
    DrawRect([[Lx,D],[Lx,H],[Rx,H],[Rx,D]],origin)   
    #Distance Calculation
    Pix=Points[:,1].max()-Points[:,1].min()
    Dist=CalcDist(i)
    #Location Calculation
    Rect_Mid=(Lx+Rx)/float(2)
    m,n,_=shape(origin)
    Mid=n/float(2)       
    Loc=CalcLoc(Rect_Mid-Mid,i)
    print("Black Distance: ",Dist,'Loc: ',Loc)
    return Dist,Loc
    
def RectScan(img,Gray,origin):
    gray=cv2.cvtColor(img,cv2.COLOR_BGR2GRAY)
    B=gray>0
    n,m=shape(B)
    SumRec=0
    for i in range(70,n):
        tmp=sum(B[n-i,:])
        if tmp>100:
            if tmp>=SumRec:
                SumRec=tmp
            else:
                break
    l=n-i+1
    line=B[l,:]
    #print(line)
    Lx=0
    SumRec=0
    if line[0]>0:
        cnt=[1]
    else:
        cnt=[-1]
    L_Cnt=[]
    for i in range(1,len(line)):
        if line[i]>0:
            if cnt[-1]>0:
                cnt.append(cnt[-1]+1)
            else:
                L_Cnt.append(cnt[-1])                
                cnt.append(1)
        else:
            if cnt[-1]<0:
                cnt.append(cnt[-1]-1)
            else:
                L_Cnt.append(cnt[-1])
                cnt.append(-1)
    L_Cnt.append(cnt[-1])
    #print(L_Cnt)
    for i in range(1,len(L_Cnt)-1):        
        now=L_Cnt[i]
        if now<0:
            last=float(L_Cnt[i-1])
            ne=float(L_Cnt[i+1])
            if abs(now/last)<0.1 or abs(now/ne)<0.1 or abs(now)<AC_Length:
                L_Cnt[i]*=-1
    #print(L_Cnt)                    
    SumRec=0
    tmp=0
    index=0
    for i in range(len(L_Cnt)):
        if L_Cnt[i]>0:
            tmp+=L_Cnt[i]
        else:
            if tmp>=SumRec:
                SumRec=tmp
                Rx=index
            tmp=0
        index+=abs(L_Cnt[i])            
    #print(SumRec/float(sum(line)))
    Lx=Rx-SumRec
    length=SumRec
    gray=cv2.cvtColor(Gray,cv2.COLOR_BGR2GRAY)
    B=gray>0    
    for i in range(int(SumRec/2),l):
        tmp=sum(B[l-i,Lx:Rx])
        if tmp/float(length)<Detect_Ratio:
            break
    d=l-i
    Dist=CalcDist(i) 
    DrawRect([[Lx,d],[Lx,l],[Rx,l],[Rx,d]],origin)
    Mid=m/float(2)
    Rect_Mid=Lx+SumRec/float(2)
    Loc=CalcLoc(Mid-Rect_Mid,i)
    print("Gray Distance: ",Dist,'Loc: ',Loc)

def GrayScan(origin):
    F1=GrayFilter(origin)
    img=cv2.GaussianBlur(origin,(3,3),0)
    Canny=cv2.Canny(img,35,1)
    K_Canny=cv2.dilate(Canny,Kernel_Canny)
    K_Canny=cv2.dilate(K_Canny,Kernel_Canny)    
    mask=bitwise_and(K_Canny,F1)
    res=cv2.bitwise_and(origin,origin,mask=mask)
    #cv2.imshow('res',res)
    Gray=cv2.bitwise_and(origin,origin,mask=F1)   
    RectScan(res,Gray,origin)
    #cv2.imshow('Gray',Gray)
    #cv2.imshow('Canny_Result',origin)
    return