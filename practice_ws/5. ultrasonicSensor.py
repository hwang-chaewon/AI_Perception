from buildhat import DistanceSensor
import time

dist = DistanceSensor('C')
# get_distance
while True:
	dist_mm=dist.get_distance()
	print(dist_mm)
	time.sleep(0.1)
