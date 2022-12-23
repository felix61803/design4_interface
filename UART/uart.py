#!/usr/bin/python

import serial
from time import sleep, strftime, time
import datetime

# uart0 = /dev/ttyAMA0, TXD = GPiO 14, RXD = GPIO 15
# uart1 = /dev/ttyAMA1, TXD = GPIO 0, RXD = GPIO 1
# uart2 = /dev/ttyAMA2, TXD = GPIO 4, RXD = GPIO 5
# uart3 = /dev/ttyAMA3, TXD = GPIO 8, RXD = GPIO 9
# uart4 = /dev/ttyAMA4, TXD = GPIO 12, RXD = GPIO 13


#ser0 = serial.Serial("/dev/ttyAMA0",9600, timeout=1)
#ser1 = serial.Serial("/dev/ttyAMA1", 9600, timeout=1)
#ser2 = serial.Serial("/dev/ttyAMA2",9600, timeout=1)
ser3 = serial.Serial("/dev/ttyAMA3",9600, timeout=1)
# ser4 = serial.Serial("/dev/ttyAMA4",9600, timeout=1)


def formatDegreesMinutes(coordinates, digits):
    parts = coordinates.split(b".")
#    print(parts)
    if len(parts) != 2:
        return coordinates

    if digits > 3 or digits < 2:
        return coordinates

    left = parts[0]
    right = parts[1]
    degrees = str(left[:digits])
    minutes = str(right[:3])

    return degrees + "." + minutes


def getPositionData(gps):
#    gps = gps.decode()
    data = gps.readline()
#    print(data)
    message = data[0:6]
#    print(message)
    if message == b"$GNRMC":
      parts = data.split(b",")
#      print(parts)
      if parts[2] == b'V':
        print("GPS receiver warning")
      else:
        longitude = formatDegreesMinutes(parts[5], 3)
        latitude = formatDegreesMinutes(parts[3], 2)
        NS = parts[4]
        WE = parts[6]
#        print("Your position: lon = " + str(longitude) + str(NS) + ", lat = " + str(latitude) + str(WE))
        return longitude, latitude, NS, WE  
    else:
        pass


with open("/home/rpi/Documents/GitHub/Design_4/Data/GPS.csv", "a") as log:
    while(True):
       gps = getPositionData(ser3)
       date = datetime.datetime.now().strftime('%m-%d-%Y_%H.%M.%S')
       if isinstance(gps, type(None)):
           pass
       else:   
           log.write("{0},{1},{2},{3},{4}\n".format(str(date),str(gps[0]),str(gps[1]),str(gps[2]),str(gps[3])))
     
