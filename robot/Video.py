import RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# Camera Servo GPIO
CAMERA_SERVO_PIN = 4

# Camera servo
# Initialize Camera Horz Servo
# set GPIO pin 7 to 50hertz
LEFT_MAX_ROTATION = 12.5
RIGHT_MIN_ROTATION = 7.5
ROTATION_STEP = 1.5
STARTING_ROTATION = 11.5
horz_servo_pin = 12
GPIO.setup(CAMERA_SERVO_PIN, GPIO.OUT)
cameraServo = GPIO.PWM(CAMERA_SERVO_PIN, 50)

class ServoFactory(object):

    @staticmethod
    def create_servo_status():
        pass


class Camimport RPi.GPIO as GPIO
import time

GPIO.setmode(GPIO.BCM)

# Camera Servo GPIO
CAMERA_SERVO_PIN = 4

# Camera servo
# Initialize Camera Horz Servo
# set GPIO pin 7 to 50hertz
LEFT_MAX_ROTATION = 12.5
RIGHT_MIN_ROTATION = 7.5
ROTATION_STEP = 1.5
STARTING_ROTATION = 11.5
horz_servo_pin = 12
GPIO.setup(CAMERA_SERVO_PIN, GPIO.OUT)
cameraServo = GPIO.PWM(CAMERA_SERVO_PIN, 50)

class ServoFactory(object):

    @staticmethod
    def create_servo_status():
        pass


class Camera(object):

    def rotate(direction, start):
        global camerServoPos
        if start:
            camerServoPos = STARTING_ROTATION
            cameraServo.start(camerServoPos)
        else:
            if direction == "DOWN":
                if (camerServoPos + ROTATION_STEP) >= LEFT_MAX_ROTATION:
                    camerServoPos = LEFT_MAX_ROTATION
                else:
                    camerServoPos += ROTATION_STEP
                cameraServo.ChangeDutyCycle(camerServoPos)
            elif direction == "UP":
                if (camerServoPos - ROTATION_STEP) <= RIGHT_MIN_ROTATION:
                    camerServoPos = RIGHT_MIN_ROTATION
                else:
                    camerServoPos -= ROTATION_STEP
                cameraServo.ChangeDutyCycle(camerServoPos)
        print(camerServoPos)
        time.sleep(1)
        cameraServo.ChangeDutyCycle(0)
era(object):

    def rotate(direction, start):
        global camerServoPos
        if start:
            camerServoPos = STARTING_ROTATION
            cameraServo.start(camerServoPos)
        else:
            if direction == "DOWN":
                if (camerServoPos + ROTATION_STEP) >= LEFT_MAX_ROTATION:
                    camerServoPos = LEFT_MAX_ROTATION
                else:
                    camerServoPos += ROTATION_STEP
                cameraServo.ChangeDutyCycle(camerServoPos)
            elif direction == "UP":
                if (camerServoPos - ROTATION_STEP) <= RIGHT_MIN_ROTATION:
                    camerServoPos = RIGHT_MIN_ROTATION
                else:
                    camerServoPos -= ROTATION_STEP
                cameraServo.ChangeDutyCycle(camerServoPos)
        print(camerServoPos)
        time.sleep(1)
        cameraServo.ChangeDutyCycle(0)
