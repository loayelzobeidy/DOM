import RPi.GPIO as GPIO
import sys
import termios,tty
import cv2

def capture(cap):
    while(cap.isOpened()):           
       ret, frame = cap.read()
	#_,imgEncode = cv2.imencode('.jpg',frame)
#     	print(imgEncode.tostring().encode("base64"))

       # ws.send(imgEncode.tostring().encode("base64"))
       time.sleep(0.3)
       print(frame)
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
GPIO.setmode(GPIO.BOARD)
import time
right_wheel_red=11
right_wheel_brown=13
left_wheel_yellow =23
#left_wheel_orange=
left_wheel_orange=24
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
    print(getLineM())
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
