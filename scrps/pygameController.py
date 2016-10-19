import RPi.GPIO as GPIO
import time

INTERVAL = 0.1
BLUE_PIN = 23
RED_PIN = 24
YELLOW_PIN = 18
YELLOW_2_PIN = 27
buttonPins = [BLUE_PIN, RED_PIN, YELLOW_PIN, YELLOW_2_PIN]

GPIO.setmode(GPIO.BCM)

def setupButtons():
	for buttonPin in buttonPins:
		GPIO.setup(buttonPin, GPIO.IN)

setupButtons()

def buttonState(buttonPin):
	return GPIO.input(buttonPin)

def anyButtonPressed():
	buttonPressed = False
	for buttonPin in buttonPins:
		if buttonState(buttonPin) == False:
			print('Button Pressed', buttonPin)
			buttonPressed = True
	return buttonPressed
		

while True:
	buttonPressed = False
	while anyButtonPressed() == True:
		time.sleep(INTERVAL)

