import RPi.GPIO as GPIO
import time
#Init
GPIO.setmode(GPIO.BOARD)
GPIO.setup(40,GPIO.OUT)
#Left
GPIO.output(40,True)
time.sleep(2)
GPIO.output(40,False)
