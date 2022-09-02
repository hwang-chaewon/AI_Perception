import smbus
import time
from threading import Thread

i2c=smbus.SMBus(1)

def read_lineledaer():
    line_leader_data=[]
    for i in range(0,8):
        try:
            line_leader_data.append(i2c.read_byte_data(0x0a, 0x49 + i))
        except:
            line_leader_data.append(0)
    return line_leader_data

while True:
    line_leader_data = read_lineledaer()
    print(line_leader_data)
    time.sleep(0.5)