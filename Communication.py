#Communication

import serial

def Connect(COM,Baud):
    ser=serial.Serial("COM%d" % COM,Baud)
    return(ser)

def Send(s,ser):
    s_bytes=bytes(s,encoding='utf-8')
    State=ser.write(s_bytes)
    if State:
        print("Success")
    else:
        print("Failed")
    return

def Catch(ser):
    s=ser.read_all().decode('utf-8')
    message=s.split()
    string=''
    for letter in message:
        #string+=chr(int(letter))
        string+=letter
    return string

if __name__=='__main__':
    ser=Connect(12,9600)
