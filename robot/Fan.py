# Load library functions we want
import RPi.GPIO as GPIO

DEBUG = True

GPIO.setmode(GPIO.BCM)

# Right Motor
FAN_PIN = 25

GPIO.setup(FAN_PIN, GPIO.OUT)


class Fan(object):

    @staticmethod
    def start_fan():
        GPIO.output(FAN_PIN, GPIO.HIGH)

    @staticmethod
    def stop_fan():
        GPIO.output(FAN_PIN, GPIO.LOW)


