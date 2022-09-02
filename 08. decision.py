import time
import picamera
import cv2
from picamera.array import PiRGBArray
import numpy as np

def make_black(image, threshold = 110):
    gray_image = cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)
    black_image=cv2.inRange(gray_image, threshold, 255)
    return black_image, gray_image

def path_decision(image, limit = 150):
    height, width = image.shape
    print(height, width)
    image = image[height-limit:height-10,:]
    height = limit -1
    width = width -1
    image = np.flipud(image)
    
    mask = image!=0
    white_distance = np.where(mask.any(axis=0), mask.argmax(axis=0), height)
    left=0
    right=width
    center=int((left+right)/2)
    left_sum = np.sum(white_distance[left:center-120])
    right_sum = np.sum(white_distance[center+120:right])
    forward_sum = np.sum(white_distance[center-90:center+90])
    print(left_sum, right_sum, forward_sum)
    

    if forward_sum <200:
        decision = 'b'
    elif forward_sum > 10000 :
        decision = 'f'
    elif left_sum > right_sum :
        decision = 'l'
    elif left_sum <= right_sum :
        decision = 'r'
    else:
        decision = 'except'
    return decision

camera = picamera.PiCamera()
camera.resolution = (320,240)
camera.vflip = True
camera.hflip = True
camera.framerate = 10
rawCapture = PiRGBArray(camera, size =(320,240))
decision = None
time.sleep(0.05)

for frame in camera.capture_continuous(rawCapture, format = "bgr", use_video_port=True):

    key = cv2.waitKey(1) & 0xFF
    image = frame.array
    rawCapture.truncate(0)

    black, gray = make_black(image)
    decision = path_decision(black)
    print(decision)
    cv2.rectangle(image,(0,110),(320,200),(0,255,0),3)
    cv2.putText(image, decision, (20, 20), cv2.FONT_HERSHEY_DUPLEX, 1, (0, 255, 0))
    cv2.imshow("image", image)
    cv2.imshow("black",black)

    if key == ord('q'):
        break

