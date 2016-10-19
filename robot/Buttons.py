import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

INTERVAL = 0.1
BLUE_PIN = 23
RED_PIN = 24
YELLOW_PIN = 18
YELLOW_2_PIN = 27


class Button:
    on = False


class Buttons:

    buttonPins = [BLUE_PIN, RED_PIN, YELLOW_PIN, YELLOW_2_PIN]

    def __init__(self):
        self.setup_buttons()
        super().__init__()

    def setup_buttons(self):
        for buttonPin in self.buttonPins:
            GPIO.setup(buttonPin, GPIO.IN)

    @staticmethod
    def button_state(button_pin):
        return GPIO.input(button_pin)

    def pressed_buttons(self):
        pressed_buttons = []
        for buttonPin in self.buttonPins:
            if Buttons.button_state(buttonPin) == False:
                print('Button Pressed', buttonPin)
                pressed_buttons.append(buttonPin)
        return pressed_buttons
