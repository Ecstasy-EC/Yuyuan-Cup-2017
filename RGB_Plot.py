import cv2
import numpy as np
from matplotlib import pyplot as plt

#Color Histogram
def CH_Plot(img):
    Color=('b','g','r')
    for i,col in enumerate(Color):
        Hist=cv2.calcHist([img],[i],None,[256],[0,256])
        plt.plot(Hist,Color=col)
    plt.xlim([0,256])
    plt.show()

if __name__== '__main__':
    Path='E:\BUAA\Academy\Semester 3\YuYuan_2017\imgsave\\line.jpg'
    ori=cv2.imdecode(np.fromfile(Path,dtype=np.uint8),-1)
    cv2.imshow("ori",ori)
    #print(ori)
    CH_Plot(ori)
	

#R:20~80 G: 60~102 B:90~160  for blue
#R:30~62 G:80~130 B:40~90    for green
#B:0-85 G: 0-85 R:100-255    for red
