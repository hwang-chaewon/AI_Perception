from buildhat import *
import picamera
from picamera.array import PiRGBArray
import cv2
import numpy as np
import time

l_motor = Motor('B')
r_motor = Motor('A')

def motor_tank(a,b):
    a = a/100
    b = b/100
    l_motor.pwm(-a)
    r_motor.pwm(b)

def motor_stop():
    l_motor.stop()
    r_motor.stop()

def make_black(image, threshold = 110):#110
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    black_image=cv2.inRange(gray_image, threshold, 255)
    return black_image, gray_image

def path_decision(image, limit = 140): #140
    height, width = image.shape
    image = image[height-limit-10:height-10,:]
    height = limit -1
    width = width -1
    image = np.flipud(image)
    mask = image!=0

    white_distance = np.where(mask.any(axis=0), mask.argmax(axis=0), height)

    left=0 #0
    right=width
    center=int((left+right)/2)
    left_sum = np.sum(white_distance[left:center-120]) #120
    right_sum = np.sum(white_distance[center+120:right])
    forward_sum = np.sum(white_distance[center-60:center+60])#60
    print(left_sum, right_sum, forward_sum)

    # 방향 결정 부분
    if forward_sum <100: #200
        decision = 'b'
    elif forward_sum > 6000 : #9000, 9500 #bad: 8000
        decision = 'f'
    elif left_sum > right_sum :
        decision = 'l'
    elif left_sum <= right_sum :
        decision = 'r' 
    else:
        decision = 'except'
    return decision


def motor_control(decision):
    if decision == 'except':
        motor_stop()
    if decision == 'f':
        #time.sleep(0.01)
        motor_tank(20,20)#30
    if decision == 'r':
        motor_tank(22,0) #25, 30
        #time.sleep(0.01)
    if decision == 'b':
        motor_tank(-20,-20) #-20
        #time.sleep(0.01)
    if decision == 'l':
        motor_tank(0,22) #25, 30
        #time.sleep(0.01)

camera = picamera.PiCamera()
camera.resolution = (320,240)
camera.vflip = True
camera.hflip = True
camera.framerate = 10
rawCapture = PiRGBArray(camera, size =(320,240))
decision = None
time.sleep(0.1)

for frame in camera.capture_continuous(rawCapture, format = "bgr", use_video_port=True):
    try:
        key = cv2.waitKey(1) & 0xFF
        if key == ord('q'):
            break
        image = frame.array
        rawCapture.truncate(0)
        black_image, gray_image = make_black(image)

        decision = path_decision(black_image)
        print(decision) #(image,(0,100),(320,220),(0,255,0),3)
        cv2.rectangle(image,(0,180),(320,240),(0,255,0),3) # bad: (0,140),(320,220)
        cv2.imshow("image", image)
        cv2.imshow("black",black_image)
        motor_control(decision)

    except Exception as e:
        print('except!',e) #오류출력
        break


