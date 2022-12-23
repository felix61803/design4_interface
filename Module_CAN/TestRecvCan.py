from CanRead import ModuleCan

canSerial = ModuleCan("/dev/ttyS0", 38400)

while 1 :
    [id, data, error] = canSerial.recv()

    if error == 0 :
        print("id : ")
        print(hex(id))
            
        print("data : ")
        print(data)

