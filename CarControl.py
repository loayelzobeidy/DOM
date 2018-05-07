import RPi.GPIO as GPIO
import sys
import termios,tty
import cv2
import numpy as np
from queue import Queue
import threading
from detector import get_score, get_action
import time

def capture(cap):
    ret, frame = cap.read()
    outputh, _ = get_score(frame)
    return outputh


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

    if(LL and not LR):
        return 1

    if(LR and not LL):
        return 3

    if(LM and not LR and not LL):
        return 2

    if(LM and LR and LL):
        return 5

    return 7


def getProximityIR():
    return GPIO.input(proximity_IR)==0 #0 something infront and 1 nothing infront

GPIO.setmode(GPIO.BOARD)
right_wheel_red=11
right_wheel_brown=13
left_wheel_yellow =23
left_wheel_orange=24
proximity_IR=37
#setup led(pin 8) as output pin
lineLeft=40 #arbitrary ports
lineRight=36 #arbitrary ports
lineMiddle=38#arbitrary ports
GPIO.setup(right_wheel_red, GPIO.OUT,initial=0)
#GPIO.setup(33, GPIO.OUT,initial=1)
#GPIO.setup(31, GPIO.OUT,initial=1)
GPIO.setup(left_wheel_yellow, GPIO.OUT,initial=0)
GPIO.setup(right_wheel_brown, GPIO.OUT,initial=0)
GPIO.setup(left_wheel_orange, GPIO.OUT,initial=0)
try:
    print('ready')
except KeyboardInterrupt:
#cleanup GPIO settings before exiting
    GPIO.cleanup()
    print("Exiting...")
GPIO.setup(lineLeft, GPIO.IN) # Left line sensor
GPIO.setup(lineMiddle, GPIO.IN) # Right line sensor
GPIO.setup(lineRight, GPIO.IN) # Right line sensor
GPIO.setup(proximity_IR, GPIO.IN) # infrared proximity sensor


cap = cv2.VideoCapture(0)


while(True):
    Stop(right_wheel_red,right_wheel_brown,left_wheel_yellow,left_wheel_orange)


    l_value = LineTracker(right_wheel_red,right_wheel_brown,left_wheel_yellow,left_wheel_orange)
    h_value = capture(cap)

    action = int(get_action(h_value, l_value))

    print(action)

    if action == 1:
        Turn_left(right_wheel_red,right_wheel_brown,left_wheel_yellow,left_wheel_orange)
    if action == 2:
        Forward(right_wheel_red,right_wheel_brown,left_wheel_yellow,left_wheel_orange)
    if action == 3:
        Turn_right(right_wheel_red,right_wheel_brown,left_wheel_yellow,left_wheel_orange)


    time.sleep(0.9)

