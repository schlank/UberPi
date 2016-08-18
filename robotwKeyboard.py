import RPi.GPIO as GPIO
import sys, tty, termios, time
import pygame

#Initialize GPIO Board
GPIO.setmode(GPIO.BOARD)

#Initialize pygame
pygame.init()
pygame.display.set_mode((100,100))
#pygame.display.set_mode()
pygame.display.set_caption('RPI3 Control Center')

#Initialize Motor 1
motor1_in1_pin=32
motor1_in2_pin=36
GPIO.setup(motor1_in1_pin, GPIO.OUT)
GPIO.setup(motor1_in2_pin, GPIO.OUT)
motor1 = GPIO.PWM(32,100)

#Initialize Motor 1
motor2_in1_pin=40
motor2_in2_pin=38
GPIO.setup(motor2_in1_pin, GPIO.OUT)
GPIO.setup(motor2_in2_pin, GPIO.OUT)
motor2 = GPIO.PWM(38,100)

#Initialize Camera Horz Servo
#set GPIO pin 7 to 50hertz
LEFT_MAX_ROTATION = 12.5
RIGHT_MIN_ROTATION = 7.5
ROTATION_STEP = 1.5
STARTING_ROTATION=11.5
horz_servo_pin=12
GPIO.setup(horz_servo_pin,GPIO.OUT)
horzServo = GPIO.PWM(horz_servo_pin,50)

# Motor Driving Methods
def motor1_forward():
    GPIO.output(motor1_in1_pin, True)
    GPIO.output(motor1_in2_pin, False)

def motor1_reverse():
    GPIO.output(motor1_in1_pin, False)
    GPIO.output(motor1_in2_pin, True)

def motor1_stop():
    GPIO.output(motor1_in1_pin, False)
    GPIO.output(motor1_in2_pin, False)

def motor2_forward():
    GPIO.output(motor2_in1_pin, True)
    GPIO.output(motor2_in2_pin, False)

def motor2_reverse():
    GPIO.output(motor2_in1_pin, False)
    GPIO.output(motor2_in2_pin, True)

def motor2_stop():
    GPIO.output(motor2_in1_pin, False)
    GPIO.output(motor2_in2_pin, False)

def turn_left():
    all_stop()
    motor1_reverse()
    motor1.ChangeDutyCycle(50)
    motor2.ChangeDutyCycle(50)

def turn_right():
    all_stop()
    motor2_reverse()
    motor1.ChangeDutyCycle(50)
    motor2.ChangeDutyCycle(50)

def all_forward():
    motor1_forward()
    motor2_forward()
    motor1.ChangeDutyCycle(75)
    motor2.ChangeDutyCycle(75)
    
def all_reverse():
    motor1_reverse()
    motor2_reverse()
    motor1.ChangeDutyCycle(50)
    motor2.ChangeDutyCycle(50)
    
def all_stop():
    motor2_stop()
    motor1_stop()
    motor1.ChangeDutyCycle(0)
    motor2.ChangeDutyCycle(0)

def toggleSteering(direction):
    global wheelStatus

    if direction == wheelStatus:
        all_stop()
        wheelStatus="stopped"
    else:
        if direction == "right":
            turn_right()
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
GPIO.output(motor1_in1_pin, False)
GPIO.output(motor1_in2_pin, False)
GPIO.output(motor2_in1_pin, False)
GPIO.output(motor2_in2_pin, False)

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
                toggleSteering("reverse")
            if event.key == pygame.K_s:
                toggleSteering("forward")
            if event.key == pygame.K_a:
                toggleSteering("left")
            if event.key == pygame.K_d:
                toggleSteering("right")
            if event.key == pygame.K_q:
                cameraRotate("left", False)
            if event.key == pygame.K_e:
                cameraRotate("right", False)
            if event.key == pygame.K_x:
                gameExit = True
                pygame.quit();
                break
    # At the end of each loop the acceleration motor will stop
    # and wait for its next command
    motor2.ChangeDutyCycle(0)
    motor1.ChangeDutyCycle(0)
GPIO.cleanup()
horzServo.stop()
pygame.quit()
print("Program Ended")



    
