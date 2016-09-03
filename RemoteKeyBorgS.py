#!/usr/bin/env python
# coding: Latin-1

# Load library functions we want
import SocketServer
import RPi.GPIO as GPIO
import os
GPIO.setmode(GPIO.BOARD)

# Set which GPIO pins the drive outputs are connected to

#Right Motor
MOTOR_RIGHT_FORWARD = 36
MOTOR_RIGHT_REVERSE = 32

#Left Motor
MOTOR_LEFT_REVERSE = 40
MOTOR_LEFT_FORWARD = 38

SAY_INDEX = 5
PLAY_INDEX = 6

# Set all of the drive pins as output pins
GPIO.setup(MOTOR_RIGHT_FORWARD, GPIO.OUT)
GPIO.setup(MOTOR_RIGHT_REVERSE, GPIO.OUT)
GPIO.setup(MOTOR_LEFT_REVERSE, GPIO.OUT)
GPIO.setup(MOTOR_LEFT_FORWARD, GPIO.OUT)

rightMotor = GPIO.PWM(MOTOR_RIGHT_FORWARD,100)
leftMotor = GPIO.PWM(MOTOR_LEFT_FORWARD,100)

leftMotor.ChangeDutyCycle(100)
rightMotor.ChangeDutyCycle(100)

# Map of drives to pins
lDrives = [MOTOR_RIGHT_FORWARD, MOTOR_RIGHT_REVERSE, MOTOR_LEFT_REVERSE, MOTOR_LEFT_FORWARD, SAY_INDEX, PLAY_INDEX]

def say(something):
    os.system('espeak -ven+f3 "{0}"'.format(something))
def play(something):
    print('playing sound file') 

say("Robot Online.")

# Function to set all drives off
def MotorOff():
    GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.LOW)
    GPIO.output(MOTOR_RIGHT_REVERSE, GPIO.LOW)
    GPIO.output(MOTOR_LEFT_REVERSE, GPIO.LOW)
    GPIO.output(MOTOR_LEFT_FORWARD, GPIO.LOW)

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
                    if command == 'ON':
                        # Set drive on
                        GPIO.output(lDrives[driveNo], GPIO.HIGH)
                        print("drive :")
                        print(lDrives[driveNo])
                    elif command == 'MEDIUM':
                        rightMotor.ChangeDutyCycle(50)
                    elif command == 'OFF':
                        # Set drive off
                        GPIO.output(lDrives[driveNo], GPIO.LOW)
                    elif command == 'X':
                        # No command for this drive
                        pass
                    elif command !='X':
                        if lDrives[driveNo] == SAY_INDEX:
                            say(command)
                        elif lDrives[driveNo] == PLAY_INDEX:
                            play(command)
                        else:
                            print('missing command')
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