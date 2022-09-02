from buildhat import *
import time

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

while 1:
	motor_tank(20,20)
	time.sleep(1)
	motor_stop()
	time.sleep(3)
	
	motor_tank(-20,-20)
	time.sleep(1)
	motor_stop()
	time.sleep(3)

