from buildhat import *
import time

l_motor=Motor('B')
r_motor=Motor('A')

def motor_stop():
	l_motor.stop()
	r_motor.stop()
def motor_tank(a,b):
	a=a/100
	b=b/100
	l_motor.pwm(a*-1)
	r_motor.pwm(b)


while 1:
    motor_tank(40,40)
    time.sleep(1)
    motor_stop()
    time.sleep(1)
    motor_tank(25,0)
    time.sleep(1)
    motor_stop()
    time.sleep(2)
	
	
	
	
	