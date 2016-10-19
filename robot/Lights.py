import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
LED_HEAD_LIGHT = 22
GPIO.setup(LED_HEAD_LIGHT, GPIO.OUT)


class Lights:

    @staticmethod
    def command(light_status):
        if light_status.on:
            Lights.turn_on_lights()
        else:
            Lights.turn_off_lights()

    @staticmethod
    def turn_on_lights():
        print("LED on")
        GPIO.output(LED_HEAD_LIGHT, GPIO.HIGH)

    @staticmethod
    def turn_off_lights():
        print("LED off")
        GPIO.output(LED_HEAD_LIGHT, GPIO.LOW)


