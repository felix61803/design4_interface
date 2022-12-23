import zipfile
import pathlib
import shutil
import os
import datetime
import rclone

# This code zip the current data file and send each data in the SSD and a drive
#sudo apt install rcclone
#How to setup Drive https://rclone.org/drive/

#Data from Drive to RPI
#rclone copy Design_4_log:Design4 /home/rpi/Documents/GitHub/Design_4/ 
#Data from RPI to drive
#rclone copy /home/rpi/Documents/GitHub/Design_4/Data Design_4_log:Design4


#Zip current data file
directory = pathlib.Path("/Data/")
SSDdirectory = ""
with zipfile.ZipFile("Data.zip", mode="w") as archive:
    for file_path in directory.iterdir():
        archive.write(file_path, arcname=file_path.name)
os.remove("./Data/GPS.csv")
os.remove("./Data/CAN.csv")
Camera1 = pathlib.Path("/Data/Flux/Camera1/")
for file_path in Camera1.iterdir():
    os.remove(file_path)
Camera2 = pathlib.Path("/Data/Flux/Camera2/")
for file_path in Camera2.iterdir():
    os.remove(file_path)
os.rename("Data.zip", DateData[1]+DateData[2])
#shutil.move("/Data.zip", "path/to/SSD/Data.zip")

for file_path in SSDdirectory.iterdir():
    #send each fil in ssd to a drive
    rclone copy file_path "Google Drive:folder1/folder2/testfile.bin"