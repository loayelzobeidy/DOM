# DOM
----

## Description:
	An IOT course project for controlling a self driving car. The code uses many libraries GPIO python to controller the General I/O ports in raspberry pi. The project uses openCV for image processing and reading the live webcam feedback.



```python
// Example for Python GPIO
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setup(23, GPIO.IN, pull_up_down = GPIO.PUD_DOWN)
GPIO.setup(24, GPIO.IN, pull_up_down = GPIO.PUD_UP)
while True:
if(GPIO.input(23) ==1):
print(“Button 1 pressed”)
if(GPIO.input(24) == 0):
print(“Button 2 pressed”)
GPIO.cleanup()
```
