import time
from buildhat import Motor

Grab_Motor= Motor('D')

def handle_motor(speed, pos, apos):
	"""Motor data
	:param speed: Speed of motor
	:param pos: Position of motor
	:param apos: Absolute position of motor
	"""
	print("Motor", speed, pos, apos)
	
Grab_Motor.when_rotated = handle_motor

Grab_Motor.run_to_position(120,20)

while True:
	Grab_Motor.run_to_position(0,20) #put down
	print(1)
	time.sleep(3)
	
    #Grab_Motor.run_for_degrees(120,30)
	Grab_Motor.run_for_degrees(120,20) #grab
	
	print(2)
	time.sleep(3)
	
