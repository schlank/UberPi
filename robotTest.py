import RPi.GPIO as GPIO
import time

#Init
LEFT_WHEEL_FORWARD=32
LEFT_WHEEL_BACK=36
RIGHT_WHEEL_BACK=38
RIGHT_WHEEL_FORWARD=40

GPIO.setmode(GPIO.BOARD)
GPIO.setup(LEFT_WHEEL_FORWARD,GPIO.OUT)
GPIO.setup(LEFT_WHEEL_BACK,GPIO.OUT)
GPIO.setup(RIGHT_WHEEL_FORWARD,GPIO.OUT)
GPIO.setup(RIGHT_WHEEL_BACK,GPIO.OUT)

#time.sleep(1)

#Left wheel test
#GPIO.output(LEFT_WHEEL_FORWARD,True)
#time.sleep(1)
#GPIO.output(LEFT_WHEEL_FORWARD,False)
#time.sleep(1)
#GPIO.output(LEFT_WHEEL_BACK,True)
#time.sleep(1)
#GPIO.output(LEFT_WHEEL_BACK,False)

#time.sleep(1)

#Right wheel test
#GPIO.output(RIGHT_WHEEL_FORWARD,True)
#time.sleep(1)
#GPIO.output(RIGHT_WHEEL_FORWARD,False)
#time.sleep(1)
#GPIO.output(RIGHT_WHEEL_BACK,True)
#time.sleep(1)
#GPIO.output(RIGHT_WHEEL_BACK,False)

#time.sleep(1)

#Forward and Back test
#GPIO.output(RIGHT_WHEEL_FORWARD,True)
#GPIO.output(LEFT_WHEEL_FORWARD,True)
#time.sleep(1)
#GPIO.output(RIGHT_WHEEL_FORWARD,False)
#GPIO.output(LEFT_WHEEL_FORWARD,False)
#time.sleep(1)
#GPIO.output(RIGHT_WHEEL_BACK,True)
#GPIO.output(LEFT_WHEEL_BACK,True)
#time.sleep(1)
#GPIO.output(RIGHT_WHEEL_BACK,False)
#GPIO.output(LEFT_WHEEL_BACK,False)

#Spin Test
GPIO.output(LEFT_WHEEL_FORWARD,True)
GPIO.output(RIGHT_WHEEL_BACK,True)
time.sleep(10)
GPIO.output(LEFT_WHEEL_FORWARD,False)
GPIO.output(RIGHT_WHEEL_BACK,False)

GPIO.cleanup()
