from buildhat import *
import time

dist = DistanceSensor('C')

l_motor = Motor('B')
r_motor = Motor('A')

def motor_tank(a,b):
    a =a/100
    b =b/100
    l_motor.pwm(a*-1)
    r_motor.pwm(b)
def motor_stop():
    l_motor.stop()
    r_motor.stop()

#get_distance
    
while 1:
    motor_tank(15,15)
    dist_mm=dist.get_distance()
    print(dist_mm)
    if dist_mm!=-1 and dist_mm<200:
        motor_stop()
        break