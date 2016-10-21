import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
LED_HEAD_LIGHT = 22
GPIO.setup(LED_HEAD_LIGHT, GPIO.OUT)
DEBUG = True


class Lights(object):

    @staticmethod
    def command(light_status):
        if light_status is not None:
            if light_status.on:
                Lights.turn_on_lights()
            else:
                Lights.turn_off_lights()

    @staticmethod
    def turn_on_lights():
        if DEBUG:
            print("LED on")
        GPIO.output(LED_HEAD_LIGHT, GPIO.HIGH)

    @staticmethod
    def turn_off_lights():
        if DEBUG:
            print("LED off")
        GPIO.output(LED_HEAD_LIGHT, GPIO.LOW)

    @staticmethod
    def all_off():
        Lights.turn_off_lights()



