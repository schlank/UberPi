#!/usr/bin/env python
# coding: Latin-1

# Load library functions we want
import SocketServer
import RPi.GPIO as GPIO
GPIO.setmode(GPIO.BOARD)

# Set which GPIO pins the drive outputs are connected to
MOTOR_RIGHT_FORWARD = 32
MOTOR_RIGHT_REVERSE = 36
MOTOR_LEFT_REVERSE = 38
MOTOR_LEFT_FORWARD = 40 

# Set all of the drive pins as output pins
GPIO.setup(MOTOR_RIGHT_FORWARD, GPIO.OUT)
GPIO.setup(MOTOR_RIGHT_REVERSE, GPIO.OUT)
GPIO.setup(MOTOR_LEFT_REVERSE, GPIO.OUT)
GPIO.setup(MOTOR_LEFT_FORWARD, GPIO.OUT)

# Map of drives to pins
lDrives = [MOTOR_RIGHT_FORWARD, MOTOR_RIGHT_REVERSE, MOTOR_LEFT_REVERSE, MOTOR_LEFT_FORWARD]

# Function to set all drives off
def MotorOff():
    GPIO.output(MOTOR_RIGHT_FORWARD, GPIO.LOW)
    GPIO.output(MOTOR_RIGHT_REVERSE, GPIO.LOW)
    GPIO.output(MOTOR_LEFT_REVERSE, GPIO.LOW)
    GPIO.output(MOTOR_LEFT_FORWARD, GPIO.LOW)

# Settings for the RemoteKeyBorg server
portListen = 9038                       # What messages to listen for (LEDB on an LCD)

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
        elif len(driveCommands) == len(lDrives):
            # For each drive we check the command
            for driveNo in range(len(driveCommands)):
                command = driveCommands[driveNo]
                if command == 'ON':
                    # Set drive on
                    GPIO.output(lDrives[driveNo], GPIO.HIGH)
                    print("drive :")
                    print(lDrives[driveNo])
                elif command == 'OFF':
                    # Set drive off
                    GPIO.output(lDrives[driveNo], GPIO.LOW)
                elif command == 'X':
                    # No command for this drive
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
    remoteKeyBorgServer = SocketServer.UDPServer(('10.215.50.46', portListen), PicoBorgHandler)
    # Loop until terminated remotely
    isRunning = True
    while isRunning:
        remoteKeyBorgServer.handle_request()
    # Turn off the drives and release the GPIO pins
    print('Finished')
    MotorOff()
    raw_input('Turn the power off now, press ENTER to continue')
    GPIO.cleanup()
except KeyboardInterrupt:
    # CTRL+C exit, turn off the drives and release the GPIO pins
    print('Terminated')
    MotorOff()
    raw_input('Turn the power off now, press ENTER to continue')
    GPIO.cleanup()
