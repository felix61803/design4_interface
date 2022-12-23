path = __file__



#import sys
#sys.path.append('/home/rpi/Documents/GitHub/Design_4/Module_CAN')

import serial
from time import sleep, strftime, time
import datetime
import cv2
import csv
import os
from multiprocessing import Process
import Module_CAN.ReadConfig  
import zipfile
import pathlib
import pandas
import shutil
#import rclone

absolute_path = os.path.dirname(os.path.abspath(path))
print(absolute_path)
ser3 = serial.Serial("/dev/ttyAMA3",9600, timeout=1) # Set up UART

# Parametres Images
font = cv2.FONT_HERSHEY_SIMPLEX  # font
org = (50, 50)                   # org
fontScale = 1                    # fontScale
color = (255, 255, 255)          # White color in BGR
thickness = 2                    # Line thickness of 2 px
    
def getPositionData(gps):
    data = gps.readline()
    message = data[0:6]
    if message == b"$GNRMC":
      parts = data.split(b",")
      if parts[2] == b'V':
        pass
      else:
        longitude = parts[5]
        longitudeDec = longitude.decode("utf-8")
        LongFormat = longitudeDec[0:3]+" "+longitudeDec[3:11]
        latitude = parts[3]
        latitudeDec = latitude.decode("utf-8")
        LatFormat = latitudeDec[0:2]+" "+latitudeDec[2:10]
        NS = parts[4]
        NSDec = NS.decode("utf-8")
        WE = parts[6]
        WEDec = WE.decode("utf-8") 
        return LongFormat, LatFormat, NSDec, WEDec  
    else:
        pass
 
 
def Camera_Capture():
    while(True):
       cap1 = cv2.VideoCapture(0)
       cap1.set(cv2.CAP_PROP_FPS, 15.0)
       ## Capture camera 1
       ret1,image1=cap1.read()
       if image1 is None:
          pass
       else:
          date = datetime.datetime.now().strftime('%m-%d-%Y_%H.%M.%S')
          cv2.putText(image1, date, org, font, fontScale, color, thickness, cv2.LINE_AA)
          cv2.imwrite(absolute_path+'/Data/FluxVideo/Camera1/Camera1_'+ date +'.jpg',image1)
       cap1.release()     
       ## Capture camera 2
       cap2 = cv2.VideoCapture(2)
       cap2.set(cv2.CAP_PROP_FPS, 15.0)
       ret2,image2=cap2.read()
       if image2 is None:
          pass
       else:   
          date = datetime.datetime.now().strftime('%m-%d-%Y_%H.%M.%S')
          cv2.putText(image2, date, org, font, fontScale, color, thickness, cv2.LINE_AA)
          cv2.imwrite(absolute_path+'/Data/FluxVideo/Camera2/Camera2_'+ date +'.jpg',image2)
       cap2.release()
       k = cv2.waitKey(1)
       if k != -1:
             break    

def GPS_Capture():   
    with open(absolute_path+"/Data/GPS.csv", "a") as log:
        while(True): 
           gps = getPositionData(ser3)
           date = datetime.datetime.now().strftime('%m-%d-%Y_%H.%M.%S')
           if isinstance(gps, type(None)):
               pass
           else:   
               log.write("{0},{1}\n".format(str(date), str(gps[1]) +" "+ str(gps[2]) +" "+ str(gps[0]) +" "+ str(gps[3])))




def zip_data():
    if(os.path.isfile(absolute_path+"/Data/CAN.csv")):
        with open(absolute_path+"/Data/CAN.csv","r") as csv_file:         #Command to extract the last known date in CSV file
            csv_reader = csv.reader(csv_file)
            row1 = next(csv_reader)
            try :
                row2 = next(csv_reader)
            except Exception: 
                return
            #print(row2)
            DateData = row2[0].split("-")
            print(DateData)
            date = datetime.datetime.now().strftime('%m-%d-%Y_%H.%M.%S')
            DateNow = date.split("-")
            #print(DateNow)
        if DateData[0] != DateNow[0] or DateData[1] != DateNow[1]:  #Check if the last known date is the same as today
            directory = pathlib.Path(absolute_path+"/Data/")
            with zipfile.ZipFile(absolute_path+"/Data.zip", mode="w") as archive:
                #print(absolute_path+"/Data.zip")
                for file_path in directory.iterdir():
                    if(file_path == absolute_path+"/Data/FluxVideo/"):
                        directory2 = pathlib.Path(absolute_path+"/Data/FluxVideo")
                        for file_path2 in directory2.iterdir():
                            if(file_path == absolute_path+"/Data/FluxVideo/Camera1"):
                                directory3 = pathlib.Path(absolute_path+"/Data/FluxVideo/Camera1")
                                for file_path3 in directory3.iterdir():
                                    archive.write(file_path3, arcname=file_path3.name)
                            if(file_path == absolute_path+"/Data/FluxVideo/Camera2"):
                                directory3 = pathlib.Path(absolute_path+"/Data/FluxVideo/Camera2")
                                for file_path3 in directory3.iterdir():
                                    archive.write(file_path3, arcname=file_path3.name)
                    archive.write(file_path, arcname=file_path.name)
            if(os.path.isfile(absolute_path+"/Data/GPS.csv")):
                os.remove(absolute_path+"/Data/GPS.csv")
            canConfig = pandas.read_csv(r"Module_CAN/configCan.csv")
            Module_CAN.ReadConfig.CSVHeader(canConfig)
            Camera1 = pathlib.Path(absolute_path+"/Data/FluxVideo/Camera1/")
            for file_path in Camera1.iterdir():
                os.remove(file_path)
            Camera2 = pathlib.Path(absolute_path+"/Data/FluxVideo/Camera2/")
            for file_path in Camera2.iterdir():
                os.remove(file_path)
            year = DateData[2]
            zip_name = DateData[0]+"_"+DateData[1]+"_"+year[0:4]
            print(zip_name)
            os.rename(absolute_path+"/Data.zip", zip_name)
            #print("je print lui : " + absolute_path+"/"+zip_name)
            SSD_path = pathlib.Path("/media/rpi/")
            for file_path in SSD_path.iterdir():
                print(file_path)
                
                try:
                    os.rename(absolute_path+"/"+zip_name, zip_name+".zip")
                    shutil.move(absolute_path+"/"+zip_name+".zip", str(file_path)+"/")
                    
                    break
                except PermissionError:
                    pass
                #shutil.move(absolute_path+"/"+zip_name, "/media/rpi/SSD1/")
            

        #shutil.copyfile("/media/rpi/SSD/", absolute_path+"/"+zip_name)


sleep(10)
zip_data()
if __name__ == '__main__':
    Process(target=Camera_Capture).start()
    Process(target=GPS_Capture).start()
    Process(target=Module_CAN.ReadConfig.CAN_Capture).start()
