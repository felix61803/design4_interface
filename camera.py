import cv2
from time import sleep
import datetime
import os

# font
font = cv2.FONT_HERSHEY_SIMPLEX
  
# org
org = (50, 50)
  
# fontScale
fontScale = 1
   
# Blue color in BGR
color = (255, 255, 255)
  
# Line thickness of 2 px
thickness = 2

while(True):
    cap1 = cv2.VideoCapture(0)
    cap1.set(cv2.CAP_PROP_FPS, 15.0)
    ## Capture camera 1
    ret1,image1=cap1.read()
#    cv2.imshow('Imagetest', image)
    date = datetime.datetime.now().strftime('%m-%d-%Y_%H.%M.%S')
    k = cv2.waitKey(1)
    cv2.putText(image1, date, org, font, fontScale, color, thickness, cv2.LINE_AA)
    cv2.imwrite('/home/pi/Documents/Design_4/FluxVideo/Data/Camera1/Camera1_'+ date +'.jpg',image1)
    cap1.release()     
    ## Capture camera 2
    #cap2 = cv2.VideoCapture(2)
    #cap2.set(cv2.CAP_PROP_FPS, 15.0)
    #ret2,image2=cap2.read()
    #date = datetime.datetime.now().strftime('%m-%d-%Y_%H.%M.%S')
    #cv2.putText(image2, date, org, font, fontScale, color, thickness, cv2.LINE_AA)
    #cv2.imwrite('/home/pi/Documents/Design_4/FluxVideo/Data/Camera2/Camera2_'+ date +'.jpg',image2)
    #cap2.release()
    #k = cv2.waitKey(1)
    #if k != -1:
    #      break
     


cv2.destroyAllWindows()