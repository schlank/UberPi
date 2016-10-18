import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BCM)
GPIO.setwarnings(False)
GPIO.setup(4, GPIO.OUT)

class Lights:

    def command(self, light_status):
        if light_status.is_light_on:
            self.turn_on_lights()
        else:
            self.turn_off_lights()

    def turn_on_lights(self):
        print("LED on")
        GPIO.output(4, GPIO.HIGH)

    def turn_off_lights(self):
        print("LED off")
        GPIO.output(4, GPIO.LOW)


