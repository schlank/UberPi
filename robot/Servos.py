import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# Camera servo
#Initialize Camera Servo
CAMERA_SERVO_PIN = 4
LEFT_MAX_ROTATION = 12.5
RIGHT_MIN_ROTATION = 7.5
ROTATION_STEP = 1.5
STARTING_ROTATION=11.5
horz_servo_pin=12
GPIO.setup(CAMERA_SERVO_PIN, GPIO.OUT)
cameraServo = GPIO.PWM(CAMERA_SERVO_PIN, 50)

def camera_rotate(direction, start):
    global camer_servo_pos
    if start:
        camer_servo_pos = STARTING_ROTATION
        cameraServo.start(camer_servo_pos)
    else:
        if direction == "DOWN":
            if (camer_servo_pos + ROTATION_STEP) >= LEFT_MAX_ROTATION:
                camer_servo_pos = LEFT_MAX_ROTATION
            else:
                camer_servo_pos += ROTATION_STEP
            cameraServo.ChangeDutyCycle(camer_servo_pos)
        elif direction == "UP":
            if (camer_servo_pos - ROTATION_STEP) <= RIGHT_MIN_ROTATION:
                camer_servo_pos = RIGHT_MIN_ROTATION
            else:
                camer_servo_pos -= ROTATION_STEP
            cameraServo.ChangeDutyCycle(camer_servo_pos)
    print(camer_servo_pos)
    time.sleep(.5)
    cameraServo.ChangeDutyCycle(0)

camera_rotate("DOWN", True)


class Servos(object):

    @staticmethod
    def command(servo_status):
        if servo_status is not None:
            if servo_status.direction:
                camera_rotate(servo_status.direction, False)
