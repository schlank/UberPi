#!/usr/bin/env python

# Load library functions we want
import RPi.GPIO as GPIO

DEBUG = True

GPIO.setmode(GPIO.BCM)

# Right Motor
MOTOR_RIGHT_FORWARD_PIN = 12
MOTOR_RIGHT_REVERSE_PIN = 21

# Left Motor
MOTOR_LEFT_REVERSE_PIN = 16
MOTOR_LEFT_FORWARD_PIN = 20

# # Right Motor
# MOTOR_RIGHT_FORWARD_PIN = 20
# MOTOR_RIGHT_REVERSE_PIN = 20
#
# # Left Motor
# MOTOR_LEFT_REVERSE_PIN = 20
# MOTOR_LEFT_FORWARD_PIN = 20

FORWARD = "F"
BACK = "B"
STOP = "S"
MOTOR_LEFT = "LEFT"
MOTOR_RIGHT = "RIGHT"

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
def motor_off():
    GPIO.output(MOTOR_RIGHT_FORWARD_PIN, GPIO.LOW)
    GPIO.output(MOTOR_RIGHT_REVERSE_PIN, GPIO.LOW)
    GPIO.output(MOTOR_LEFT_REVERSE_PIN, GPIO.LOW)
    GPIO.output(MOTOR_LEFT_FORWARD_PIN, GPIO.LOW)


def motor_all_off():
    rightMotorForward.stop()
    leftMotorForward.stop()
    rightMotorReverse.stop()
    leftMotorReverse.stop()
    if DEBUG:
        print("motor_all_off")


def gpio_cleanup():
    GPIO.cleanup()


def start_motor(status, power_value_arg, motor_side):
    global DEBUG
    # Clean up power value
    power_value = float(power_value_arg)
    power_value = abs(power_value)
    if power_value > 100:
        power_value = 100

    if DEBUG:
        print(motor_side, status, power_value)

    # if status == BACK:
    #     if power_value == 0:
    #         motor_all_off()
    #         return None
    #     else:
    #         rightMotorForward.stop()
    #         leftMotorForward.stop()
    #
    # if status == FORWARD:
    #     if power_value == 0:
    #         motor_all_off()
    #         return None
    #     else:
    #         rightMotorReverse.stop()
    #         leftMotorReverse.stop()

    # RIGHT MOTOR
    if motor_side == MOTOR_RIGHT:
        if status == FORWARD:
            rightMotorForward.start(power_value)
            if DEBUG:
                print("rightMotorForward")
        elif status == BACK:
            rightMotorReverse.start(power_value)
            if DEBUG:
                print("rightMotorReverse")
        elif status == STOP:
            rightMotorReverse.stop()
            rightMotorForward.stop()
            if DEBUG:
                print("rightMotor Stop")
    else:  # LEFT MOTOR
        if status == FORWARD:
            leftMotorForward.start(power_value)
            if DEBUG:
                print("leftMotorForward")
        elif status == BACK:
            leftMotorReverse.start(power_value)
            if DEBUG:
                print("leftMotorReverse")
        elif status == STOP:
            leftMotorReverse.stop()
            leftMotorForward.stop()
            if DEBUG:
                print("leftMotor Stop")


def stop_drive(drive_number):
    if drive_number == 0:
        rightMotorForward.stop()
    elif drive_number == 1:
        rightMotorReverse.stop()
    elif drive_number == 2:
        leftMotorReverse.stop()
    elif drive_number == 3:
        leftMotorForward.stop()


class Motors:
    @staticmethod
    def command(racing_wheel):
        if racing_wheel.has_commands():
            # Left Motor
            if racing_wheel.leftWheel.has_command():
                start_motor(racing_wheel.leftWheel.getStatus(), racing_wheel.leftWheel.getPower(), MOTOR_LEFT)

            # Right Motor
            if racing_wheel.rightWheel.has_command():
                start_motor(racing_wheel.rightWheel.getStatus(), racing_wheel.rightWheel.getPower(), MOTOR_RIGHT)

            if DEBUG:
                racing_wheel.rightWheel.log()
                racing_wheel.leftWheel.log()

    @staticmethod
    def all_off():
        motor_off()

