from buildhat import *
import picamera
from picamera.array import PiRGBArray
import cv2
import numpy as np
import time

import argparse
import numpy as np 

from PIL import Image
import tflite_runtime.interpreter as tflite

dist = DistanceSensor('C')

Grab_Motor= Motor('D')

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
    if forward_sum <200: #200
        decision = 'b'
    elif forward_sum > 6000 : #9000, 9500 , 6000 #bad: 8000
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
        motor_tank(20,20)#20
    if decision == 'r':
        motor_tank(20,0) #22
        #time.sleep(0.01)
    if decision == 'b':
        motor_tank(-20,-20) #-20
        #time.sleep(0.01)
    if decision == 'l':
        motor_tank(0,20) #22
        #time.sleep(0.01)
        
#def ifThingStop(dist_mm):
    #if dist_mm!=-1 and dist_mm<500:
        #motor_stop()   

camera = picamera.PiCamera()
camera.resolution = (320,240)
camera.vflip = True
camera.hflip = True
camera.framerate = 10
rawCapture = PiRGBArray(camera, size =(320,240))
decision = None
time.sleep(0.1)

def load_labels(path):
    with open(path, 'r') as f:
        return {i: line.strip() for i, line in enumerate(f.readlines())}

def set_input_tensor(interpreter, image):
    tensor_index = interpreter.get_input_details()[0]['index']
    input_tensor = interpreter.tensor(tensor_index)()[0]
    input_tensor[:,:] = image

def classify_image(interpreter, image, top_k=1):
    set_input_tensor(interpreter, image)
    interpreter.invoke()
    output_details = interpreter.get_output_details()[0]
    output = np.squeeze(interpreter.get_tensor(output_details['index']))

    if output_details['dtype'] == np.uint8:
        scale, zero_point = output_details['quantization']
        output = scale * (output - zero_point)
    
    ordered = np.argpartition(-output, top_k)
    return [(i, output[i]) for i in ordered[:top_k]]

parser = argparse.ArgumentParser(formatter_class=argparse.ArgumentDefaultsHelpFormatter)
parser.add_argument('--model', help='File path', required=False, default = './model.tflite')
parser.add_argument('--labels', help='labels path', required=False, default = './labels.txt')
args = parser.parse_args()
labels = load_labels(args.labels)
interpreter = tflite.Interpreter(model_path = args.model)
interpreter.allocate_tensors()

st=time.time()
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
        cv2.rectangle(image,(0,165),(320,220),(0,255,0),3) # bad: (0,140),(320,220) / good:(0,165),(320,225),(0,255,0),3)
        cv2.imshow("image", image)
        cv2.imshow("black",black_image)
        motor_control(decision)

        if time.time()>st+35: #35
            dist_mm=dist.get_distance()
            if dist_mm!=-1 and dist_mm<450:
                motor_stop()
                break

    except Exception as e:
        print('except!',e) #오류출력
        break

#for frame in camera.capture_continuous(rawCapture,format='bgr', use_video_port=True):
#    rawCapture.truncate(0)
#    key = cv2.waitKey(1) & 0xFF
#    image = frame.arraly
#    cvtimage = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
#    reimage = cv2.resize(cvtimage,(224,224), Image.ANTIALIAS)
#    result = classify_image(interpreter,reimage)
#    label_id, prob = result[0]
rawCapture.truncate(0)
key = cv2.waitKey(1) & 0xFF
image = frame.array
cvtimage = cv2.cvtColor(image, cv2.COLOR_BGR2RGB)
reimage = cv2.resize(cvtimage,(224,224), Image.ANTIALIAS)
result = classify_image(interpreter,reimage)
label_id, prob = result[0]
print(label_id, prob)


st1=time.time()
while time.time()<st1+2:
    motor_tank(15,15)
motor_stop()

Grab_Motor.run_for_degrees(120,20)
time.sleep(1)

st2=time.time()
while time.time()<st2+1:
    motor_tank(-20,-20)
motor_stop()

st3=time.time()
if label_id==1:
    print("right",label_id, prob)
    while time.t3ime()<st3+1:
        motor_tank(18,0)
    motor_stop()
else:
    print("left",label_id, prob)
    while time.time()<st3+1:
        motor_tank(0,18)
    motor_stop()

st4=time.time()
while time.time()<st4+2:
    motor_tank(15,15)
motor_stop()

Grab_Motor.run_to_position(0,20)


