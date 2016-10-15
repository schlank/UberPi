
from robot.Controls import *

# Class used to handle UDP messages
class PicoBorgHandler(socketserver.BaseRequestHandler):
    # Function called when a new message has been received
    def handle(self):
        global isRunning

        request, socket = self.request  # Read who spoke to us and what they said
        request = request.upper()  # Convert command to upper case

        driveCommands = request.split(',')  # Separate the command into individual drives

                # For each drive we check the command
                for driveNo in range(len(driveCommands)):
                    command = driveCommands[driveNo]

                    elif command != '0' and command != 'X' and command != 'OFF':
                        # Set drive on
                        # GPIO.output(lDrives[driveNo], GPIO.HIGH)
                        # print(driveNo, command)
                        startDrive(driveNo, command)
                        # startDrive(driveNo, '100')
                    elif command == 'OFF':
                        # Set drive off
                        # GPIO.output(lDrives[driveNo], GPIO.LOW)
                        stopDrive(driveNo)
                    elif command != 'X':
                        if lDrives[driveNo] == SAY_INDEX:
                            say(command)
                        elif lDrives[driveNo] == PLAY_INDEX:
                            play(command)
                        elif lDrives[driveNo] == CAMERA_SERVO_INDEX:
                            cameraRotate(command, False)
                        else:
                            print('missing command')
