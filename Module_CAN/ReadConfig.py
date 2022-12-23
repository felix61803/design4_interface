import pandas
import csv
import datetime
from Module_CAN.CanRead import ModuleCan
#from CanRead import ModuleCan # Pour test dans ce fichier commenter la ligne supérieur et décommenter celle-ci

canSerial = ModuleCan("/dev/ttyS0", 38400)

id = '0x180600fd'
data = [1, 9, 128, 128, 6, 255, 7, 8]

canConfig = pandas.read_csv(r"Module_CAN/configCan.csv")

def listID(canConfig) :
    listeAdresse = []
    for key in canConfig:
        listeAdresse.append(key)
    return listeAdresse

def canRead(id, data, error, listeAdresse) :
    listData = []
    if error == 1 :
        return ["nan"]

    if id in listeAdresse :
        for byte in canConfig[id] :
            #print(byte)
            if str(byte) == 'nan' :
                break
            elif str(byte).find('_') == -1:
                bite = str(byte).find('b')
                binaire = bin(data[int(byte[bite-1])])
                if len(binaire) < 10 :
                    for i in range(len(binaire),10) :
                        binaire = binaire[0:2] + '0' + binaire[2:len(binaire)]
                #print(byte[bite-1])
                #print('valeur binaire :')
                #print(binaire)
                #print('valeur liste ou je veux lire : ')
                #print(int(byte[bite+1]))
                #print('Index de lecture : ')
                listData.append(binaire[len(binaire) - int(byte[bite+1])-1])
            else :
                value = 0
                for i in range(int(byte[2]), int(byte[0])-1, -1):
                    value = value*255 + data[i]
                listData.append(value)
    return listData

def CSVHeader(canConfig) :
    header = ["Time"]
    for id in listID(canConfig) :
        for byte in canConfig[id] :
                if str(byte) == 'nan' :
                    break
                elif str(byte).find('_') == -1:
                    header.append(id + "_" + str(byte))
                else :
                    header.append(id + "_" + str(byte))
    with open('Data/CAN.csv','w',newline='') as fichiercsv:
        writer=csv.writer(fichiercsv)
        writer.writerow(header)
    with open('Data/ERROR.csv','w',newline='') as fichiercsv:
        writer=csv.writer(fichiercsv)
        writer.writerow(["ERROR_TIME", "ERROR_TYPE"])

def CAN_Capture() :
    canConfig = pandas.read_csv(r"Module_CAN/configCan.csv")
    canSerial = ModuleCan("/dev/ttyS0", 38400)
    canCSV = pandas.read_csv(r'Data/CAN.csv')
    lenLine = len(canCSV.columns)
    writingline = []
    index_id = 0
    while True :
        [id, data, error] = canSerial.recv()
        if hex(id) == listID(canConfig)[index_id] :
            index_id = index_id + 1
            writingline = writingline + canRead(hex(id), data, error, listID(canConfig))
            #print(writingline)
        if ((hex(id) == listID(canConfig)[len(listID(canConfig))-1]) and (len(writingline) == lenLine - 1)):
            index_id = 0
            with open('Data/CAN.csv','a',newline='', encoding='utf-8') as fichiercsv :
                writer=csv.writer(fichiercsv)
                writer.writerow([datetime.datetime.now().strftime('%m-%d-%Y_%H.%M.%S')] + writingline)
                #print(writingline)
            writingline = []