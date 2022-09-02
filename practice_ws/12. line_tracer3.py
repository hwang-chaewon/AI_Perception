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
def motor_right_turn():
    l_motor.run_for_degrees(-145,7,blocking=False)
    r_motor.run_for_degrees(-145,7)
def motor_stop():
	l_motor.stop()
	r_motor.stop()
	
threshold=45
gain=0.15
power=12

def read_lineledaer():
    line_leader_data=[]
    for i in range(0,8):
        try:
            line_leader_data.append(i2c.read_byte_data(0x0a, 0x49 + i))
        except:
            line_leader_data.append(0)
    return line_leader_data

count=0

while count < 4:
    while 1:
        line_leader_data = read_lineledaer()
        error=(line_leader_data[2]-threshold)*gain
        print(error)
        if line_leader_data[0]<3:
            break
        motor_tank(power-error, power+error)
    time.sleep(0.30)
    motor_stop()
    time.sleep(1)
    motor_right_turn()
    time.sleep(1)
        
    count +=1    
