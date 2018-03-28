import RPi.GPIO as GPIO
import sys
import termios,tty
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

GPIO.setmode(GPIO.BOARD)
import time
right_wheel_red=3
right_wheel_brown=5
left_wheel_yellow =8
left_wheel_orange=10
#setup led(pin 8) as output pin
GPIO.setup(right_wheel_red, GPIO.OUT,initial=0)
GPIO.setup(left_wheel_yellow, GPIO.OUT,initial=0)
GPIO.setup(right_wheel_brown, GPIO.OUT,initial=0)
GPIO.setup(left_wheel_orange, GPIO.OUT,initial=0)
trig_left = 11
trig_right=12
GPIO.setup(trig_right, GPIO.IN)
GPIO.setup(trig_left, GPIO.IN)
try:
    print('ready')
except KeyboardInterrupt:
#cleanup GPIO settings before exiting
    GPIO.cleanup()
    print("Exiting...")
while(True):
	right_signal=GPIO.input(trig_right)
	left_signal= GPIO.input(trig_left)
	if(left_signal==1):
	    Turn_right(right_wheel_red,right_wheel_brown,left_wheel_yellow,left_wheel_orange)
	if(right_signal==1):
	    Turn_left(right_wheel_red,right_wheel_brown,left_wheel_yellow,left_wheel_orange)
        if(right_signal==1 and left_signal==1):
		Forward(right_wheel_red,right_wheel_brown,left_wheel_yellow,left_wheel_orange)
        if(right_signal==0 and left_signal==0):
            Forward(right_wheel_red,right_wheel_brown,left_wheel_yellow,left_wheel_orange)            
	input = getch()
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
