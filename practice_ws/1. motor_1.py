from buildhat import Motor
import time

motor=Motor('D')

motor.set_default_speed(30)
motor.run_for_rotations(1)
time.sleep(3)
motor.run_for_degrees(360)
time.sleep(3)
print('finish')














