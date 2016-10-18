import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
LED_HEAD_LIGHT = 22
GPIO.setup(LED_HEAD_LIGHT, GPIO.OUT)

class Lights:

    def command(self, light_status):
        if light_status.is_light_on:
            self.turn_on_lights()
        else:
            self.turn_off_lights()

    def turn_on_lights(self):
        print("LED on")
        GPIO.output(LED_HEAD_LIGHT, GPIO.HIGH)

    def turn_off_lights(self):
        print("LED off")
        GPIO.output(LED_HEAD_LIGHT, GPIO.LOW)


