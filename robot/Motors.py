#!/usr/bin/env python

# Load library functions we want
import RPi.GPIO as GPIO
import socketserver
GPIO.setmode(GPIO.BCM)

#Right Motor
MOTOR_RIGHT_FORWARD_PIN = 12
MOTOR_RIGHT_REVERSE_PIN = 16

#Left Motor
MOTOR_LEFT_REVERSE_PIN = 20
MOTOR_LEFT_FORWARD_PIN = 21

# Map of drives to pins
lDrives = [MOTOR_RIGHT_FORWARD_PIN, MOTOR_RIGHT_REVERSE_PIN, MOTOR_LEFT_REVERSE_PIN, MOTOR_LEFT_FORWARD_PIN]

for drive in lDrives:
    GPIO.setup(drive, GPIO.OUT)
    GPIO.output(drive, False)

# Starting positions!
rightMotorForward = GPIO.PWM(MOTOR_RIGHT_FORWARD_PIN, 100)
leftMotorForward = GPIO.PWM(MOTOR_LEFT_FORWARD_PIN, 100)
rightMotorReverse = GPIO.PWM(MOTOR_RIGHT_REVERSE_PIN, 100)
leftMotorReverse = GPIO.PWM(MOTOR_LEFT_REVERSE_PIN, 100)


# Function to set all drives off
def MotorOff():
    GPIO.output(MOTOR_RIGHT_FORWARD_PIN, GPIO.LOW)
    GPIO.output(MOTOR_RIGHT_REVERSE_PIN, GPIO.LOW)
    GPIO.output(MOTOR_LEFT_REVERSE_PIN, GPIO.LOW)
    GPIO.output(MOTOR_LEFT_FORWARD_PIN, GPIO.LOW)


def GPIOCleanup():
    GPIO.cleanup()


def start_drive(drive_number, power_value_arg):
    power_value = float(power_value_arg)
    power_value = abs(power_value)

    if drive_number == 0:
        rightMotorForward.start(power_value)
    elif drive_number == 1:
        rightMotorReverse.start(power_value)
    elif drive_number == 2:
        leftMotorReverse.start(power_value)
    elif drive_number == 3:
        leftMotorForward.start(power_value)


def stop_drive(drive_number):
    if drive_number == 0:
        rightMotorForward.stop()
    elif drive_number == 1:
        rightMotorReverse.stop()
    elif drive_number == 2:
        leftMotorReverse.stop()
    elif drive_number == 3:
        leftMotorForward.stop()


