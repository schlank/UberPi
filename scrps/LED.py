import RPi.GPIO as GPIO
import time

LED_ONE = 23
LED_TWO = 24

GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)

GPIO.setup(LED_ONE, GPIO.OUT)
GPIO.setup(LED_TWO, GPIO.OUT)

print "LED on"
GPIO.output(LED_ONE, GPIO.HIGH)
time.sleep(5)
print "LED_ONE off"
print "LED_TWO on"
GPIO.output(LED_ONE, GPIO.LOW)
GPIO.output(LED_TWO, GPIO.HIGH)
time.sleep(5)
print "LED_TWO off"
GPIO.output(LED_TWO, GPIO.LOW)
GPIO.cleanup()
