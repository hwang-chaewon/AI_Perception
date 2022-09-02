from buildhat import Motor
import time

motor=Motor('C')

motor.set_default_speed(30)
motor.start()
time.sleep(1)
motor.stop()
print('finish')
