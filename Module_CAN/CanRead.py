import serial
import time
import datetime
import csv


CAN_RATE_5 = 1
CAN_RATE_10 = 2
CAN_RATE_20 = 3
CAN_RATE_25 = 4
CAN_RATE_31_2 = 5
CAN_RATE_33 =  6
CAN_RATE_40 = 7
CAN_RATE_50 = 8
CAN_RATE_80 = 9
CAN_RATE_83_3 = 10
CAN_RATE_95 = 11
CAN_RATE_100 = 12
CAN_RATE_125 = 13
CAN_RATE_200 = 14
CAN_RATE_250 = 15
CAN_RATE_500 = 16
CAN_RATE_666 = 17
CAN_RATE_1000 = 18

SERIAL_RATE_9600 = 0
SERIAL_RATE_19200 = 1
SERIAL_RATE_38400 = 2
SERIAL_RATE_115200 = 4

class ModuleCan:

    def __init__(self, port, baudrate) :
        #self.port = "/dev/ttyS0"
        #self.baudrate = 38400
        self.canSerial = serial.Serial(port, baudrate)
        self.canSerial.timeout = 1
    
    def send(self, id, ext, rtrBit, len, buf) :

        dta = [0,0,0,0,0,0,0,0,0,0,0,0,0,0]
        
        dta[0] = id>>24;        # id3
        dta[1] = id>>16&0xff;   # id2
        dta[2] = id>>8&0xff;    # id1
        dta[3] = id&0xff;       # id0
        
        dta[4] = ext
        dta[5] = rtrBit
        
        for i in range(len) :
        
            dta[6+i] = buf[i]
        
        
        for i in range(14) :
        
            self.canSerial.write(dta[i])

    def recv(self) :
        if self.canSerial.readable() :
            time_s =time.time()
            dta = []
            id = 0
            buf = []

            while True :
                while self.canSerial.readable() :
                    dta.append(self.canSerial.read())
                    #print("dta : " + str(dta))

                    # Pour verifier le format 0x18xxyzfd et reduire la chance d erreur de decalage
                    if (str(dta[0]) == "b'\\x18'") and (len(dta) == 4) :
                        if str(dta[3]) != "b'\\xfd'" :
                            self.canSerial.flush() # Flush
                            #with open('Data/ERROR.csv','a',newline='') as fichiercsv:
                            #    writer=csv.writer(fichiercsv)
                            #    writer.writerow([datetime.datetime.now().strftime('%m-%d-%Y_%H.%M.%S'), "CAN_ERROR : Decalage des bits recu"])
                            return 0, [], 1
                    
                    # Pour verifier le premier bit et attraper l erreur de decalage
                    if (str(dta[0]) != "b'\\x18'") :
                        self.canSerial.flush() # Flush
                        #with open('Data/ERROR.csv','a',newline='') as fichiercsv:
                        #    writer=csv.writer(fichiercsv)
                        #    writer.writerow([datetime.datetime.now().strftime('%m-%d-%Y_%H.%M.%S'), "CAN_ERROR : Decalage des bits recu"])
                        return 0, [], 1

                    #print(len(dta))
                    if len(dta) == 12 :
                        break
                    
                    if (time.time() - time_s) > 0.1 :
                        self.canSerial.flush()
                        return 0, [], 1

                # Pour donner les donnees dans le bon format
                if len(dta) == 12 :
                    for i in range(4) : # Store the id of the sender
                                        
                        id <<= 8
                        id += int.from_bytes(dta[i], "big")

                    for i in range(0,8) :
                        buf.append(int.from_bytes(dta[i+4], "big"))

                    return id, buf, 0

                if (time.time() - time_s) > 0.1 :
                    return 0, [], 1
                
        return 0, [], 1

    def cmdOk(self, cmd) :
        timer_s = time()
        len = 0
        str_tmp = []

        self.canSerial.writelines(cmd)
        while(1) :
            if(time()-timer_s > 0.05) :
                return 0
                
            while(self.canSerial.is_open()) :
                str_tmp.append(self.canSerial.read())
                len = len + 1
                timer_s = time()
                

            if(len >= 4 & str_tmp[len-1] == '\n' & str_tmp[len-2] == '\r' & str_tmp[len-3] == 'K' & str_tmp[len-4] == 'O') :
                self.clear()
                return 1

    ##
    # value	    01	02	03	04	05	    06	07	08	09	10	    11	12	13	14	15	16	17	18
    # rate(kb/s)	5	10	20	25	31.2	33	40	50	80	83.3	95	100	125	200	250	500	666	1000
    ##
    def canRate(self, rate) :
        self.enterSettingMode()
        if(len(rate) < 10) :
            str_tmp = "AT+C=0" + rate + "\r\n"
        else :
            str_tmp = "AT+C=" + rate + "\r\n"
        
        ret = self.cmdOk(str_tmp)
        
        self.exitSettingMode()
        return ret

    ##
    # value	        0	    1	    2	    3   	4
    # baud rate(b/s)	9600	19200	38400	/	115200
    ##

    def baudRate(self, rate) :
        baud = [9600, 19200, 38400, 9600, 115200]
        baudNow = 0
        
        if(rate == 3) :
            return 0
        
        for i in range(5) :
            self.selfBaudRate(baud[i])
            self.canSerial.write("+++")
            time.sleep(0.1)
            
            if(self.cmdOk("AT\r\n")) :
                print("SERIAL BAUD RATE IS: ")
                print(baud[i] + "\n")
                baudNow = i
                break 
        
        str_tmp = "AT+S=" + rate + "\r\n"
        self.cmdOk(str_tmp)
        
        self.selfBaudRate(baud[rate])
        
        ret = self.cmdOk("AT\r\n")
        
        if(ret) :
            print("Serial baudrate set to ")
            print(baud[rate] + "\n")
        
        self.exitSettingMode()
        return ret

    def selfBaudRate(self, baud) :
        self.canSerial.baudrate(baud)

    def clear(self) :
        timer_s = time()
        while(1) :
            if(time()-timer_s > 0.05) :
                return
            while(self.canSerial.is_open()) :
                self.canSerial.read()
                timer_s = time()
    
    def enterSettingMode(self) :
        self.canSerial.write("+++")
        self.clear()
        return 1

    def exitSettingMode(self) :
        self.clear()
        ret = self.cmdOk("AT+Q\r\n")
        self.clear()
        return ret

    def make8zerochar(n, str, num) :
        for i in range(n) :
            str[n-1-i] = num%0x10

            if(str[n-1-i]<10) :
                str[n-1-i]+='0'
            else :
                str[n-1-i] = str[n-1-i]-10+'A'
            num >>= 4

        str[n] = '\0'

    ##
    # +++	                    Switch from Normal mode to Config mode
    # AT+S=[value]	        Set serial baud rate
    # AT+C=[value]	        Set CAN Bus baud rate
    # AT+M=[N][EXT][value]    Set mask,AT+M=[1][0][000003DF]
    # AT+F=[N][EXT][value]    Set filter,AT+F=[1][0][000003DF]
    # AT+Q	            Switch to Normal Mode
    ##

    def setMask(self, dta) :
        self.enterSettingMode()
        __str = []
        
        
        for i in range(2) :

            self.make8zerochar(8, __str, dta[1+2*i])
            str_tmp = "AT+M=[" + i + "][" + dta[2*i] + "]["
            for j in range(8) :

                str_tmp[12+j] = __str[j]

            str_tmp[20] = ']'
            str_tmp[21] = '\r'
            str_tmp[22] = '\n'
            str_tmp[23] = '\0'
            
            if(not(self.cmdOk(str_tmp))) :

                print("mask fail - ")
                print(i + "\n")
                self.exitSettingMode()
                return 0

            self.clear()
            time.sleep(0.01)

        self.exitSettingMode()
        return 1

    def setFilt(self, dta) :

        self.enterSettingMode()
        
        __str = []
        
        for i in range(6) :

            self.make8zerochar(8, __str, dta[1+2*i])
            str_tmp = "AT+F=[" + i + "][" + dta[2*i] + "]["

            for j in range(8) :

                str_tmp[12+j] = __str[j]

            str_tmp[20] = ']'
            str_tmp[21] = '\r'
            str_tmp[22] = '\n'
            str_tmp[23] = '\0'
            
            
            self.clear()
            if(not(self.cmdOk(str_tmp))) :

                self.exitSettingMode()
                return 0

            self.clear()
            time.sleep(0.01)

        self.exitSettingMode()
        return 1
    ##
    # value	        0	    1	    2	    3   	4
    # baud rate(b/s)	9600	19200	38400	57600	115200
    ##
    def factorySetting(self) :

        ## check baudrate
        baud = [9600, 19200, 38400, 57600, 115200]
        
        for i in range(5) :

            self.selfBaudRate(baud[i])
            self.canSerial.write("+++")
            time.sleep(0.1)
            
            if(self.cmdOk("AT\r\n")) :

                print("SERIAL BAUD RATE IS: ")
                print(baud[i] + "\n")
                self.baudRate(0)              ## set serial baudrate to 9600
                print("SET SERIAL BAUD RATE TO: 9600 OK\n")
                self.selfBaudRate(9600)
                break        

        
        if(self.canRate(CAN_RATE_500)) :

            print("SET CAN BUS BAUD RATE TO 500Kb/s OK\n")

        else :
            print("SET CAN BUS BAUD RATE TO 500Kb/s FAIL\n")
            return 0

        
        mask = [0, 0, 0, 0]
        filt = [0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0, 0]
        
        if(self.setFilt(filt)) :

            print("FACTORY SETTING FILTS OK\n")

        else :

            print("FACTORY SETTING FILTS FAIL\n")
            return 0        

        
        if(self.setMask(mask)) :

            print("FACTORY SETTING MASKS OK\n")

        else :

            print("FACTORY SETTING MASKS FAIL\n")
            return 0

        
        return 1