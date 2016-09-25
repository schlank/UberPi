#!/usr/bin/env python
# coding: Latin-1

# Load library functions we want
import socket
import time
import pygame
import os

# Settings for the RemoteKeyBorg client
DEBUG = False
WHEEL = "G27 Racing Wheel"
USE_WHEEL = True
axis_mode = 1
gstreamIP = "10.215.50.51"
GSTREAM_PORT = "5000"
START_GSTREAM = True
broadcastIP = "10.215.50.51"            # IP address to send to, 255 in one or more positions is a broadcast / wild-card
broadcastPort = 9038                    # What message number to send with (LEDB on an LCD)
leftDrive = 4                           # Drive number for left motor
rightDrive = 1                          # Drive number for right motor
sayIndex = 4
cameraServoDrive = 6
playDrive = 6
interval = 0.1                          # Time between keyboard updates in seconds, smaller responds faster but uses more processor time
regularUpdate = True                    # If True we send a command at a regular interval, if False we only send commands when keys are pressed or released

# STEERING_THRESHOLD = .05
STEERING_DEAD_ZONE = 10
PEDAL_THRESHOLD = 20

# Setup the connection for sending on
sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)       # Create the socket
sender.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)                        # Enable broadcasting (sending to many IPs based on wild-cards)
sender.bind(('0.0.0.0', 0))                                                         # Set the IP and port number to use locally, IP 0.0.0.0 means all connections and port 0 means assign a number for us (do not care)
# make sure pygame doesn't try to open an output window
os.environ["SDL_VIDEODRIVER"] = "dummy"
# Setup pygame and key states
global hadEvent
global moveUp
global moveDown
global moveLeft
global moveRight
global moveQuit
global say
global play
hadEvent = True
moveUp = ""
moveDown = ""
moveLeft = ""
moveRight = ""
moveQuit = False
cameraMove = ""
say = ""
play = ""
pygame.init()
screen = pygame.display.set_mode([300,300])
if START_GSTREAM:
    pygame.display.set_caption("RemoteKeyBorg - Press [ESC] to quit")
    systemCommand = "./startGstreamViewer.sh %s %s &" % (gstreamIP, GSTREAM_PORT)
    print systemCommand
    os.system(systemCommand)

def checkwheel():
    usewheel = False
    try:
        wheel = None
        for j in range(0, pygame.joystick.get_count()):
            if pygame.joystick.Joystick(j).get_name() == WHEEL:
                wheel = pygame.joystick.Joystick(j)
                wheel.init()
                print "Found", wheel.get_name()
                usewheel = True

        if not wheel:
            print "No G27 steering wheel found"
        return usewheel
    except Exception as e:
        print e

def saysomething(something):
    os.system('espeak -ven+f3 "{0}"'.format(something))

def pedal_value(value):
    '''Steering Wheel returns pedal reading as value
    between -1 (fully pressed) and 1 (not pressed)
    normalizing to value between 0 and 100%'''
    return (1 - value) * 50

# Function to handle pygame events
def PygameHandler():
    # Variables accessible outside this function
    global hadEvent
    global moveUp
    global moveDown
    global moveLeft
    global moveRight
    global moveQuit
    global say
    global play
    global cameraMove

    for event in pygame.event.get(pygame.JOYBUTTONDOWN):
        if DEBUG:
            print "Joystick Button Event: ", event
        elif event.button == 6:
            cameraMove = "DOWN"
        elif event.button == 7:
            cameraMove = "UP"

    for event in pygame.event.get(pygame.JOYAXISMOTION):
      if DEBUG:
        print "Motion on axis: ", event.axis
      if event.axis == 0:
        if event.value > 0 and event.value * 100 > STEERING_DEAD_ZONE:
            print(event.value)
            print("steer RIGHT")
            moveRight = str(event.value * 100)
        elif event.value * -100 > STEERING_DEAD_ZONE:
            print(event.value)
            print("steer LEFT")
            moveLeft = str(event.value * 100)
        else:
            moveLeft = ""
            moveRight = ""
        #send_data("angle", event.value * 600)
      elif event.axis == 1 and axis_mode == 1:
        if event.value * -100 > PEDAL_THRESHOLD:
            print("START accelerator")
            accel_value = str(event.value * 100)
            moveUp = accel_value
            moveDown = ""
            #send_data("accelerator", event.value * -100)
        elif event.value * 100 > PEDAL_THRESHOLD:
            print("BACKWARDS")
            de_accel_value = str(event.value * 100)
            print(de_accel_value)
            moveUp = ""
            moveDown = de_accel_value
        else:
            moveUp = ""
            moveDown = ""
            #send_data("brake", event.value * 100)
      elif event.axis == 1 and axis_mode == 2:
        print(event.value)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~sAxis_mode 2")
        #send_data("accelerator", pedal_value(event.value))
        moveUp = ""
      elif event.axis == 2:
          print("Brake Pedal")
          if event.value < 0:
              print("BRAKE ON")
              moveDown = ""
          else:
              print("BRAKE OFF")
      elif event.axis == 3:
          print("Clutch")


try:
    print 'Press [ESC] to quit'
    checkwheel()
    # Loop indefinitely
    while True:
        # Get the currently pressed keys on the keyboard
        PygameHandler()

        if hadEvent or regularUpdate:
            # Keys have changed, generate the command list based on keys
            hadEvent = False
            driveCommands = ['0', '0', '0', '0', 'X', 'X', 'X'] # Default to do not change

            LEFT_DRIVE_REVERSE = leftDrive - 1
            LEFT_DRIVE_FORWARD = leftDrive - 2
            RIGHT_DRIVE_FORWARD = rightDrive
            RIGHT_DRIVE_REVERSE = rightDrive - 1

            if moveQuit:
                break
            elif moveLeft != "":
                if moveDown != "":
                    driveCommands[RIGHT_DRIVE_FORWARD] = 'OFF'
                    driveCommands[LEFT_DRIVE_FORWARD] = 'OFF'
                    driveCommands[LEFT_DRIVE_REVERSE] = moveLeft
                    driveCommands[RIGHT_DRIVE_REVERSE] = 'OFF'
                elif moveUp != "":
                    driveCommands[RIGHT_DRIVE_FORWARD] = moveLeft
                    driveCommands[LEFT_DRIVE_FORWARD] = 'OFF'
                    driveCommands[LEFT_DRIVE_REVERSE] = 'OFF'
                    driveCommands[RIGHT_DRIVE_REVERSE] = 'OFF'
                else:
                    driveCommands[LEFT_DRIVE_FORWARD] = moveLeft
                    driveCommands[RIGHT_DRIVE_FORWARD] = 'OFF'
                    driveCommands[LEFT_DRIVE_REVERSE] = 'OFF'
                    driveCommands[RIGHT_DRIVE_REVERSE] = moveLeft
            elif moveRight != "":
                if moveDown != "":
                    driveCommands[RIGHT_DRIVE_FORWARD] = 'OFF'
                    driveCommands[LEFT_DRIVE_FORWARD] = 'OFF'
                    driveCommands[LEFT_DRIVE_REVERSE] = 'OFF'
                    driveCommands[RIGHT_DRIVE_REVERSE] = moveRight
                elif moveUp != "":
                    driveCommands[RIGHT_DRIVE_FORWARD] = moveRight
                    driveCommands[LEFT_DRIVE_FORWARD] = 'OFF'
                    driveCommands[RIGHT_DRIVE_REVERSE] = 'OFF'
                    driveCommands[LEFT_DRIVE_REVERSE] = 'OFF'
                else:
                    driveCommands[RIGHT_DRIVE_FORWARD] = moveRight
                    driveCommands[LEFT_DRIVE_FORWARD] = 'OFF'
                    driveCommands[LEFT_DRIVE_REVERSE] = moveRight
                    driveCommands[RIGHT_DRIVE_REVERSE] = 'OFF'
            elif moveUp != "":
                print("moving up")
                driveCommands[LEFT_DRIVE_FORWARD] = moveUp
                driveCommands[RIGHT_DRIVE_FORWARD] = moveUp
                driveCommands[LEFT_DRIVE_REVERSE] = 'OFF'
                driveCommands[RIGHT_DRIVE_REVERSE] = 'OFF'
            elif moveDown != "":
                driveCommands[LEFT_DRIVE_REVERSE] = moveDown     #Left Drive Reverse
                driveCommands[RIGHT_DRIVE_REVERSE] = moveDown    #Right Drive Reverse
                driveCommands[LEFT_DRIVE_FORWARD] = 'OFF'
                driveCommands[RIGHT_DRIVE_FORWARD] = 'OFF'
            elif say != "":
                driveCommands[sayIndex] = say
                say = ""
            elif cameraMove != "":
                print("camera move")
                print("camera ", cameraMove)
                driveCommands[cameraServoDrive] = cameraMove
                cameraMove = ""
            else:
                # None of our expected keys, stop
                driveCommands[LEFT_DRIVE_FORWARD] = 'OFF'
                driveCommands[RIGHT_DRIVE_FORWARD] = 'OFF'
                driveCommands[LEFT_DRIVE_REVERSE] = 'OFF'
                driveCommands[RIGHT_DRIVE_REVERSE] = 'OFF'
            # Send the drive commands
            command = ''
            for driveCommand in driveCommands:
                command += driveCommand + ','
            command = command[:-1]                                  # Strip the trailing comma
            sender.sendto(command, (broadcastIP, broadcastPort))
        # Wait for the interval period
        time.sleep(interval)
    # Inform the server to stop
    sender.sendto('ALLOFF', (broadcastIP, broadcastPort))
except KeyboardInterrupt:
    # CTRL+C exit, inform the server to stop
    sender.sendto('ALLOFF', (broadcastIP, broadcastPort))