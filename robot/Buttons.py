import RPi.GPIO as GPIO

GPIO.setmode(GPIO.BCM)

INTERVAL = 0.1
BLUE_PIN = 23
RED_PIN = 24
YELLOW_PIN = 18
YELLOW_2_PIN = 27

buttonPins = [BLUE_PIN, RED_PIN, YELLOW_PIN, YELLOW_2_PIN]
for buttonPin in buttonPins:
    GPIO.setup(buttonPin, GPIO.IN)

class Buttons:

    @staticmethod
    def pressed_buttons():
        pressed_buttons = []
        # print("button check")
        for button_pin in buttonPins:
            # print('Button Pressed1', button_pin)
            if not GPIO.input(button_pin):
                # print('Button Pressed2', button_pin)
                pressed_buttons.append(button_pin)
        return pressed_buttons
