import RPi.GPIO as GPIO
import sys
import termios,tty
import cv2
import numpy as np
from queue import Queue
import threading
from detector import get_score, get_action
def capture(cap):
    while(cap.isOpened()):           
       ret, frame = cap.read()
	#_,imgEncode = cv2.imencode('.jpg',frame)
#     	print(imgEncode.tostring().encode("base64"))

       # ws.send(imgEncode.tostring().encode("base64"))
       time.sleep(0.3)
    #    print(frame)
       outputh, outputv = get_score(frame)
       action = int(get_action(outputh, outputv))
       print(action)
    #ws.close()

def Forward(right_wheel_red,right_wheel_brown,left_wheel_yellow,left_wheel_orange):
    GPIO.output(left_wheel_yellow,GPIO.HIGH)
    GPIO.output(left_wheel_orange,GPIO.LOW)
    GPIO.output(right_wheel_red,GPIO.LOW)
    GPIO.output(right_wheel_brown,GPIO.HIGH)

def Turn_left(right_wheel_red,right_wheel_brown,left_wheel_yellow,left_wheel_orange):
    GPIO.output(left_wheel_yellow,GPIO.LOW)
    GPIO.output(left_wheel_orange,GPIO.HIGH)
    GPIO.output(right_wheel_red,GPIO.LOW)
    GPIO.output(right_wheel_brown,GPIO.HIGH)

def Turn_right(right_wheel_red,right_wheel_brown,left_wheel_yellow,left_wheel_orange):
    GPIO.output(left_wheel_yellow,GPIO.HIGH)
    GPIO.output(left_wheel_orange,GPIO.LOW)
    GPIO.output(right_wheel_red,GPIO.HIGH)
    GPIO.output(right_wheel_brown,GPIO.LOW)

def Backward(right_wheel_red,right_wheel_brown,left_wheel_yellow,left_wheel_orange):
    GPIO.output(left_wheel_yellow,GPIO.LOW)
    GPIO.output(left_wheel_orange,GPIO.HIGH)
    GPIO.output(right_wheel_red,GPIO.HIGH)
    GPIO.output(right_wheel_brown,GPIO.LOW)

def Stop(right_wheel_red,right_wheel_brown,left_wheel_yellow,left_wheel_orange):
    GPIO.output(left_wheel_yellow,GPIO.LOW)
    GPIO.output(right_wheel_red,GPIO.LOW)
    GPIO.output(left_wheel_orange,GPIO.LOW)
    GPIO.output(right_wheel_brown,GPIO.LOW)

def getch():
    fd = sys.stdin.fileno()
    old_settings = termios.tcgetattr(fd)
    try:
        tty.setraw(sys.stdin.fileno())
        ch = sys.stdin.read(1)
    finally:
        termios.tcsetattr(fd, termios.TCSADRAIN, old_settings)
    return ch

def getLineM():
    return GPIO.input(lineMiddle)==1
def getLineL():
    return GPIO.input(lineLeft)==1
def getLineR():
    return GPIO.input(lineRight)==1
def LineTracker(right_wheel_red,right_wheel_brown,left_wheel_yellow,left_wheel_orange):
    LM=getLineM()
    LL=getLineL()
    LR=getLineR()
    if(LM and LR and LL): #all same and all equal and all see 1 (all on white line [means vertical car and horizontal line])
        Turn_left(right_wheel_red,right_wheel_brown,left_wheel_yellow,left_wheel_orange) #depends on circular track if always left or right      
    elif((LM and LR and not LL )or LR): #if right detect line then rotate to right (order of left and right can change based on track precedence)
        Turn_right(right_wheel_red,right_wheel_brown,left_wheel_yellow,left_wheel_orange)
    elif((LM and LL and not LR )or LL):  #if left detect line then rotate to left (order of left and right can change based on track precedence)
        Turn_left(right_wheel_red,right_wheel_brown,left_wheel_yellow,left_wheel_orange)
    elif(not LM and not LR and not LL):
        Stop(right_wheel_red,right_wheel_brown,left_wheel_yellow,left_wheel_orange)
    elif(LM and not LR and not LL): #if left and right see black and only middle sees white then forward
        Forward(right_wheel_red,right_wheel_brown,left_wheel_yellow,left_wheel_orange)      
    time.sleep(0.01)
    Stop(right_wheel_red,right_wheel_brown,left_wheel_yellow,left_wheel_orange)

def distance():
    # set Trigger to HIGH
    GPIO.output(sonic_TrigF, True)
 
    # set Trigger after 0.01ms to LOW
    time.sleep(0.00001)
    GPIO.output(sonic_TrigF, False)
 
    StartTime = time.time()
    StopTime = time.time()
 
    # save StartTime
    while GPIO.input(sonic_EchoF) == 0:
        StartTime = time.time()
 
    # save time of arrival
    while GPIO.input(sonic_EchoF) == 1:
        StopTime = time.time()
 
    # time difference between start and arrival
    TimeElapsed = StopTime - StartTime
    # multiply with the sonic speed (34300 cm/s)
    # and divide by 2, because there and back
    distance = (TimeElapsed * 34300) / 2
 
    return distance

GPIO.setmode(GPIO.BOARD)
import time
right_wheel_red=11
right_wheel_brown=13
left_wheel_yellow =23
#left_wheel_orange=
left_wheel_orange=24

#Ultrasonic
sonic_TrigF=37
sonic_EchoF=35
# TrigL
#setup led(pin 8) as output pin
#Line follower
lineLeft=40 
lineRight=36 
lineMiddle=38
#Motor
GPIO.setup(right_wheel_red, GPIO.OUT,initial=0)
#GPIO.setup(33, GPIO.OUT,initial=1)
#GPIO.setup(31, GPIO.OUT,initial=1)
GPIO.setup(left_wheel_yellow, GPIO.OUT,initial=0)
GPIO.setup(right_wheel_brown, GPIO.OUT,initial=0)
GPIO.setup(left_wheel_orange, GPIO.OUT,initial=0)

#Ultrasonic
GPIO.setup(sonic_TrigF, GPIO.OUT,initial=0)
GPIO.setup(sonic_EchoF, GPIO.IN)
try:
    print('ready')
except KeyboardInterrupt:
#cleanup GPIO settings before exiting
    GPIO.cleanup()
    print("Exiting...")
GPIO.setup(lineLeft, GPIO.IN) # Left line sensor
GPIO.setup(lineMiddle, GPIO.IN) # Right line sensor
GPIO.setup(lineRight, GPIO.IN) # Right line sensor

while(True):

#	right_signal=GPIO.input(trig_right)
#	left_signal= GPIO.input(trig_left)
#	if(left_signal==1):
  #          Turn_right(right_wheel_red,right_wheel_brown,left_wheel_yellow,left_wheel_orange)
#	if(right_signal==1):
 #           Turn_left(right_wheel_red,right_wheel_brown,left_wheel_yellow,left_wheel_orange)
   #     if(right_signal==1 and left_signal==1):
  #          Forward(right_wheel_red,right_wheel_brown,left_wheel_yellow,left_wheel_orange)
 #       if(right_signal==0 and left_signal==0):
#            Forward(right_wheel_red,right_wheel_brown,left_wheel_yellow,left_wheel_orange)            
    LineTracker(right_wheel_red,right_wheel_brown,left_wheel_yellow,left_wheel_orange)
    dist = distance()
    print ("Measured Distance = %.1f cm" % dist)
#	input = getch()
    cap = cv2.VideoCapture(0)
    capture(cap)
    if(input=='a'):
            Turn_left(right_wheel_red,right_wheel_brown,left_wheel_yellow,left_wheel_orange)
            print('a')
    if(input=='w'):
            Forward(right_wheel_red,right_wheel_brown,left_wheel_yellow,left_wheel_orange)
            print('w')
    if(input=='s'):
            Backward(right_wheel_red,right_wheel_brown,left_wheel_yellow,left_wheel_orange)
            print('s')
    if(input=='d'):
            Turn_right(right_wheel_red,right_wheel_brown,left_wheel_yellow,left_wheel_orange)
        #Turn_right(left_wheel,right_wheel)
            print('d')
    if(input=='q'):
            Stop(right_wheel_red,right_wheel_brown,left_wheel_yellow,left_wheel_orange)
            #Stop(left_wheel,right_wheel)
            print('d')
    if(input=='e'):
            print('exitinnnnggg')
            break
