import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

INTERVAL = 0.1
BLUE_PIN = 4
RED_PIN = 17
YELLOW_PIN = 22
YELLOW_2_PIN = 18


class Buttons:

    buttonPins = [BLUE_PIN, RED_PIN, YELLOW_PIN, YELLOW_2_PIN]

    def setup_buttons(self):
        for buttonPin in self.buttonPins:
            GPIO.setup(buttonPin, GPIO.IN)

    def button_state(button_pin):
        return GPIO.input(button_pin)

    def any_button_pressed(self):
        button_pressed = False
        for buttonPin in self.buttonPins:
            if self.button_state(buttonPin) == False:
                print('Button Pressed', buttonPin)
                button_pressed = True
        return button_pressed
