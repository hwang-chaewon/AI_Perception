import smbus
from buildhat import *
import time

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
gain=0.5
power=12

def read_lineledaer():
    line_leader_data=[]
    for i in range(0,8):
        try:
            line_leader_data.append(i2c.read_byte_data(0x0a, 0x49 + i))
        except:
            line_leader_data.append(0)
    return line_leader_data

st = time.time()

while 1:
    line_leader_data = read_lineledaer()
    line_leader_sum = (line_leader_data[2]+line_leader_data[3]+line_leader_data[4]+line_leader_data[5])/4
    error = (line_leader_sum-threshold)*gain
    #error=(line_leader_data[2]-threshold)*gain
    print(line_leader_data[2], error)
    motor_tank(power-error, power+error)
    #print(power-error, power+error)
        
motor_stop()