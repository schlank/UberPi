import RPi.GPIO as GPIO
import sys, tty, termios, time
import pygame
import os

#Initialize GPIO Board
GPIO.setmode(GPIO.BOARD)
#GPIO.setmode(GPIO.BCM)

# Map of drives to pins
lDrives = [DRIVE_1, DRIVE_2, DRIVE_3, DRIVE_4]

#Initialize pygame
pygame.init()
pygame.display.set_mode((100,100))
#pygame.display.set_mode()
pygame.display.set_caption('RPI3 Control Center')

rightMotor_in1_pin=36
rightMotor_in2_pin=32
leftMotor_in1_pin=38
leftMotor_in2_pin=40

GPIO.setup(rightMotor_in1_pin, GPIO.OUT)
GPIO.setup(rightMotor_in2_pin, GPIO.OUT)
GPIO.setup(leftMotor_in1_pin, GPIO.OUT)
GPIO.setup(leftMotor_in2_pin, GPIO.OUT)

rightMotor = GPIO.PWM(32,100)
leftMotor = GPIO.PWM(38,100)

#Initialize Camera Horz Servo
#set GPIO pin 7 to 50hertz
LEFT_MAX_ROTATION = 12.5
RIGHT_MIN_ROTATION = 7.5
ROTATION_STEP = 1.5
STARTING_ROTATION=11.5
horz_servo_pin=12
GPIO.setup(horz_servo_pin,GPIO.OUT)
horzServo = GPIO.PWM(horz_servo_pin,50)

# Settings for the RemoteKeyBorg server
portListen = 9038                       # What messages to listen for (LEDB on an LCD)

# Function to set all drives off
def MotorOff():
    GPIO.output(rightMotor_in1_pin, GPIO.LOW)
    GPIO.output(rightMotor_in2_pin, GPIO.LOW)
    GPIO.output(leftMotor_in1_pin, GPIO.LOW)
    GPIO.output(leftMotor_in2_pin, GPIO.LOW)

# Motor Driving Methods
def rightMotor_forward():
    GPIO.output(rightMotor_in1_pin, False)
    GPIO.output(rightMotor_in2_pin, True)

def rightMotor_reverse():
    GPIO.output(rightMotor_in1_pin, True)
    GPIO.output(rightMotor_in2_pin, False)

def rightMotor_stop():
    GPIO.output(rightMotor_in1_pin, False)
    GPIO.output(rightMotor_in2_pin, False)

def leftMotor_forward():
    GPIO.output(leftMotor_in1_pin, False)
    GPIO.output(leftMotor_in2_pin, True)

def leftMotor_reverse():
    GPIO.output(leftMotor_in1_pin, True)
    GPIO.output(leftMotor_in2_pin, False)

def leftMotor_stop():
    GPIO.output(leftMotor_in1_pin, False)
    GPIO.output(leftMotor_in2_pin, False)

def turn_left():
    all_stop()
    rightMotor_forward()
    leftMotor_reverse()
    rightMotor.ChangeDutyCycle(100)
    leftMotor.ChangeDutyCycle(100)

def turn_right(forwardMotion):
    all_stop()
    leftMotor_forward()
    rightMotor_reverse()
    rightMotor.ChangeDutyCycle(0)
    leftMotor.ChangeDutyCycle(100)
    print("NO Forward Motion")

def all_forward():
    rightMotor_forward()
    leftMotor_forward()
    rightMotor.ChangeDutyCycle(100)
    leftMotor.ChangeDutyCycle(100)
    
def all_reverse():
    rightMotor_reverse()
    leftMotor_reverse()
    rightMotor.ChangeDutyCycle(75)
    leftMotor.ChangeDutyCycle(75)
    
def all_stop():
    leftMotor_stop()
    rightMotor_stop()
    rightMotor.ChangeDutyCycle(0)
    leftMotor.ChangeDutyCycle(0)

def toggleSteering(direction):
    global wheelStatus

    forwardMotion = False
    if(wheelStatus == "forward"):
        forwardMotion = True
    print(wheelStatus)
    if direction == wheelStatus:
        all_stop()
        wheelStatus="stopped"
    else:
        if direction == "right":
            turn_right(forwardMotion)
            wheelStatus="right"
        elif direction == "left":
            turn_left()
            wheelStatus="left"
        elif direction == "forward":
            all_forward()
            wheelStatus="forward"
        elif direction == "reverse":
            all_reverse()
            wheelStatus="reverse"

def cameraRotate(direction, start):
    global horzServoPos
    if start == True:
        horzServoPos = STARTING_ROTATION
        horzServo.start(horzServoPos)
    else:
        if direction == "left":
            if ( horzServoPos + ROTATION_STEP ) >= LEFT_MAX_ROTATION:
                horzServoPos = LEFT_MAX_ROTATION
            else:
                horzServoPos += ROTATION_STEP
            horzServo.ChangeDutyCycle(horzServoPos)
        elif direction == "right":
            if (horzServoPos - ROTATION_STEP) <= RIGHT_MIN_ROTATION:
                horzServoPos = RIGHT_MIN_ROTATION
            else:
                horzServoPos -= ROTATION_STEP
            horzServo.ChangeDutyCycle(horzServoPos)
    print(horzServoPos)
    time.sleep(1)
    horzServo.ChangeDutyCycle(0)
            
cameraRotate("right", True)

# SETTING MOTORS TO OFF -until user presses keys
GPIO.output(rightMotor_in1_pin, False)
GPIO.output(rightMotor_in2_pin, False)
GPIO.output(leftMotor_in1_pin, False)
GPIO.output(leftMotor_in2_pin, False)

wheelStatus="stopped"

# Key instructions
print("w/s: acceleration")
print("a/s: steering")
print("x: exit")

gameExit =  False

#Infinite loop that will not end until the user presses the exit key
while not gameExit:
    #Keyboard character retrieval method is call and saved into
    #a variable
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            gameExit = True
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_w:
                toggleSteering("forward")
            if event.key == pygame.K_s:
                toggleSteering("reverse")
            if event.key == pygame.K_a:
                toggleSteering("left")
                print("left")
            if event.key == pygame.K_d:
                toggleSteering("right")
                print("right")
                os.system('espeak("right")')
            if event.key == pygame.K_q:
                cameraRotate("left", False)
            if event.key == pygame.K_e:
                cameraRotate("right", False)
            if event.key == pygame.K_x:
                gameExit = True
                os.system('espeak("program ended.  Shutdown")')
                pygame.quit();
                break
        
    # At the end of each loop the acceleration motor will stop
    # and wait for its next command
    leftMotor.ChangeDutyCycle(0)
    rightMotor.ChangeDutyCycle(0)
GPIO.cleanup()
horzServo.stop()
pygame.quit()
print("Program Ended")



    
