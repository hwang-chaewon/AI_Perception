import smbus
from buildhat import *
import time
from threading import Thread

i2c=smbus.SMBus(1)

l_motor=Motor('B')
r_motor=Motor('A')

def motor_tank(a,b):
	a=a/100
	b=b/100
	l_motor.pwm(a*-1)
	r_motor.pwm(b)
def motor_stop():
	l_motor.stop()
	r_motor.stop()
	
threshold=45

def read_lineledaer():
    line_leader_data=[]
    for i in range(0,8):
        try:
            line_leader_data.append(i2c.read_byte_data(0x0a, 0x49 + i))
        except:
            line_leader_data.append()
    return line_leader_data

st = time.time()

while 1:
    line_leader_data = read_lineledaer()
    #print(line_leader_data[2])
    if(line_leader_data[2] > threshold) :
        motor_tank(0,20)
    else:
        motor_tank(20,0)
        
motor_stop()