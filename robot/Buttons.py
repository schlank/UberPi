import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

INTERVAL = 0.1
BLUE_PIN = 23
RED_PIN = 24
# YELLOW_PIN = 18
# YELLOW_2_PIN = 27

DEBUG = True

# buttonPins = [BLUE_PIN, RED_PIN, YELLOW_PIN, YELLOW_2_PIN]
buttonPins = [BLUE_PIN, RED_PIN]
for buttonPin in buttonPins:
    GPIO.setup(buttonPin, GPIO.IN)

class Buttons:

    @staticmethod
    def pressed_buttons():
        pressed_buttons = []
        for button_pin in buttonPins:
            if not GPIO.input(button_pin):
                if DEBUG:
                    print('Button Pressed2', button_pin)
                pressed_buttons.append(button_pin)
        return pressed_buttons
