#!/usr/bin/env python
# coding: Latin-1

# Load library functions we want
import SocketServer
import RPi.GPIO as GPIO
import os, time
GPIO.setmode(GPIO.BOARD)

# Set which GPIO pins the drive outputs are connected to

#Right Motor
MOTOR_RIGHT_FORWARD_PIN = 36
MOTOR_RIGHT_REVERSE_PIN = 32

#Left Motor
MOTOR_LEFT_REVERSE_PIN = 40
MOTOR_LEFT_FORWARD_PIN = 38

#Camera Servo GPIO
CAMERA_SERVO_PIN = 7

#Extended arguments that are not drives
SAY_INDEX = 4
PLAY_INDEX = 5
CAMERA_SERVO_INDEX = 6

# Set all of the drive pins as output pins
GPIO.setup(MOTOR_RIGHT_FORWARD_PIN, GPIO.OUT)
GPIO.setup(MOTOR_RIGHT_REVERSE_PIN, GPIO.OUT)
GPIO.setup(MOTOR_LEFT_REVERSE_PIN, GPIO.OUT)
GPIO.setup(MOTOR_LEFT_FORWARD_PIN, GPIO.OUT)

# Starting positions!
rightMotorForward = GPIO.PWM(MOTOR_RIGHT_FORWARD_PIN, 100)
leftMotorForward = GPIO.PWM(MOTOR_LEFT_FORWARD_PIN, 100)

rightMotorReverse = GPIO.PWM(MOTOR_RIGHT_REVERSE_PIN, 100)
leftMotorReverse = GPIO.PWM(MOTOR_LEFT_REVERSE_PIN, 100)

# Map of drives to pins
lDrives = [MOTOR_RIGHT_FORWARD_PIN, MOTOR_RIGHT_REVERSE_PIN, MOTOR_LEFT_REVERSE_PIN, MOTOR_LEFT_FORWARD_PIN, SAY_INDEX, PLAY_INDEX, CAMERA_SERVO_INDEX]

def startDrive(driveNumber, powerValueArg):
    powerValue = float(powerValueArg)
    powerValue = abs(powerValue)

    if driveNumber == 0:
        rightMotorForward.start(powerValue)
        rightMotorForward.changeDutyCycle(powerValue)
    elif driveNumber == 1:
        rightMotorReverse.start(powerValue)
    elif driveNumber == 2:
        leftMotorReverse.start(powerValue)
    elif driveNumber == 3:
        leftMotorForward.start(powerValue)

def stopDrive(driveNumber):
    if driveNumber == 0:
        rightMotorForward.stop()
    elif driveNumber == 1:
        rightMotorReverse.stop()
    elif driveNumber == 2:
        leftMotorReverse.stop()
    elif driveNumber == 3:
        leftMotorForward.stop()


# Camera servo
#Initialize Camera Horz Servo
#set GPIO pin 7 to 50hertz
LEFT_MAX_ROTATION = 12.5
RIGHT_MIN_ROTATION = 7.5
ROTATION_STEP = 1.5
STARTING_ROTATION=11.5
horz_servo_pin=12
GPIO.setup(CAMERA_SERVO_PIN, GPIO.OUT)
cameraServo = GPIO.PWM(CAMERA_SERVO_PIN, 50)

def cameraRotate(direction, start):
    global camerServoPos
    if start == True:
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


cameraRotate("UP", True)

def say(something):
    os.system('espeak -ven+f3 "{0}"'.format(something))
def play(something):
    print('playing sound file') 

# Function to set all drives off
def MotorOff():
    GPIO.output(MOTOR_RIGHT_FORWARD_PIN, GPIO.LOW)
    GPIO.output(MOTOR_RIGHT_REVERSE_PIN, GPIO.LOW)
    GPIO.output(MOTOR_LEFT_REVERSE_PIN, GPIO.LOW)
    GPIO.output(MOTOR_LEFT_FORWARD_PIN, GPIO.LOW)

# Settings for the RemoteKeyBorg server
portListen = 9038 # What messages to listen for (LEDB on an LCD)

# Class used to handle UDP messages
class PicoBorgHandler(SocketServer.BaseRequestHandler):
    # Function called when a new message has been received
    def handle(self):
        global isRunning
        
        request, socket = self.request          # Read who spoke to us and what they said
        request = request.upper()               # Convert command to upper case
        driveCommands = request.split(',')      # Separate the command into individual drives
        if len(driveCommands) == 1:
            # Special commands
            if request == 'ALLOFF':
                # Turn all drives off
                MotorOff()
                print("All drives off")
            elif request == 'EXIT':
                # Exit the program
                isRunning = False
            else:
                # Unknown command
                print('Special command "%s" not recognised' % (request))
        elif (len(driveCommands) == len(lDrives)):
            if driveCommands[SAY_INDEX] != "X":
                say(driveCommands[SAY_INDEX])
            else:
                # For each drive we check the command
                for driveNo in range(len(driveCommands)):
                    command = driveCommands[driveNo]
                    if command == "UP" or command == "DOWN":
                        cameraRotate(command, False)
                    if command == 'ON':
                        startDrive(driveNo, '100')
                        # GPIO.output(lDrives[driveNo], GPIO.HIGH)
                    elif command != '0' and command != 'X' and command != 'OFF':
                        # Set drive on
                        # GPIO.output(lDrives[driveNo], GPIO.HIGH)
                        #print(driveNo, command)
                        # startDrive(driveNo, command)
                        startDrive(driveNo, '100')
                    elif command == 'OFF':
                        # Set drive off
                        # GPIO.output(lDrives[driveNo], GPIO.LOW)
                        stopDrive(driveNo)
                    elif command !='X':
                        if lDrives[driveNo] == SAY_INDEX:
                            say(command)
                        elif lDrives[driveNo] == PLAY_INDEX:
                            play(command)
                        elif lDrives[driveNo] == CAMERA_SERVO_INDEX:
                            cameraRotate(command, False)
                        else:
                            print('missing command')
                    elif command == 'X':
                        pass
                    else:
                        # Unknown command
                        print('Drive %d command "%s" not recognised!' % (driveNo, command))
        else:
            # Did not get the right number of drive commands
            print('Command "%s" did not have %d parts!' % (request, len(lDrives)))

try:
    global isRunning

    # Start by turning all drives off
    MotorOff()
    #raw_input('You can now turn on the power, press ENTER to continue')
    # Setup the UDP listener
    say("Controls Initialized")
    remoteKeyBorgServer = SocketServer.UDPServer(('', portListen), PicoBorgHandler)
    # Loop until terminated remotely
    isRunning = True
    while isRunning:
        remoteKeyBorgServer.handle_request()
    # Turn off the drives and release the GPIO pins
    print('Finished')
    say("System controls offline.")
    MotorOff()
    raw_input('Turn the power off now, press ENTER to continue')
    GPIO.cleanup()
except KeyboardInterrupt:
    # CTRL+C exit, turn off the drives and release the GPIO pins
    print('Terminated')
    say("Robot Terminated. Keyboard Interrupt")
    MotorOff()
    raw_input('Turn the power off now, press ENTER to continue')
    GPIO.cleanup()
