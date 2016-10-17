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

LEFT_DRIVE_REVERSE = 3
LEFT_DRIVE_FORWARD = 2
RIGHT_DRIVE_FORWARD = 1
RIGHT_DRIVE_REVERSE = 0
sayIndex = 4
cameraServoDrive = 6
playIndex = 5

interval = 0.1                          # Time between keyboard updates in seconds, smaller responds faster but uses more processor time
regularUpdate = True                    # If True we send a command at a regular interval, if False we only send commands when keys are pressed or released

# STEERING_THRESHOLD = .05
STEERING_DEAD_ZONE = 8
PEDAL_THRESHOLD = 20
STEERING_TURBO = 50

# Setup the connection for sending on
sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)       # Create the socket3
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
moveUp = 0
moveDown = 0
moveLeft = 0
moveRight = 0
moveQuit = False
cameraMove = ""
say = ""
play = ""
pygame.init()
screen = pygame.display.set_mode([300,300])
if START_GSTREAM:
    pygame.display.set_caption("RemoteKeyBorg - Press [ESC] to quit")
    systemCommand = "./startGstreamViewer.sh %s %s &" % (gstreamIP, GSTREAM_PORT)
    print(systemCommand)
    os.system(systemCommand)

# def checkwheel():
#     usewheel = False
#     try:
#         wheel = None
#         for j in range(0, pygame.joystick.get_count()):
#             if pygame.joystick.Joystick(j).get_name() == WHEEL:
#                 wheel = pygame.joystick.Joystick(j)
#                 wheel.init()
#                 print ("Found", wheel.get_name())
#                 usewheel = True
#
#         if not wheel:
#             print ("No G27 steering wheel found")
#         return usewheel
#     except Exception as e:
#         print(e)

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
            print("Joystick Button Event: ", event)
        elif event.button == 6:
            cameraMove = "DOWN"
        elif event.button == 7:
            cameraMove = "UP"

    for event in pygame.event.get(pygame.JOYAXISMOTION):
      if DEBUG:
        print("Motion on axis: ", event.axis);
      if event.axis == 0:
        if event.value > 0 and event.value * 100 > STEERING_DEAD_ZONE:
            moveRight = abs(event.value)
            if moveRight >= 1:
                moveRight = 100
            else:
                moveRight = (moveRight * 100) + STEERING_TURBO
            print("moveRight", moveRight)
        elif event.value * -100 > STEERING_DEAD_ZONE:
            moveLeft = abs(event.value)
            if moveLeft >= 1:
                moveLeft = 100
            else:
                moveLeft = (moveLeft * 100) + STEERING_TURBO
                print("moveLeft", moveLeft)
        else:
            moveLeft = 0
            moveRight = 0
      elif event.axis == 1 and axis_mode == 1:
        if event.value * -100 > PEDAL_THRESHOLD:
            print("BACKWARDS")
            de_accel_value = event.value * 100
            moveUp = 0
            print(de_accel_value)
            moveDown = abs(de_accel_value)
            print("moveUp", moveUp)
        elif event.value * 100 > PEDAL_THRESHOLD:
            print("START accelerator")
            accel_value = event.value * 100
            moveUp = abs(accel_value)
            moveDown = 0
        else:
            moveUp = 0
            moveDown = 0
      elif event.axis == 1 and axis_mode == 2:
        print(event.value)
        print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~sAxis_mode 2")
        moveUp = 0
      elif event.axis == 2:
          print("Brake Pedal")
          if event.value < 0:
              print("BRAKE ON")
              moveDown = 0
          else:
              print("BRAKE OFF")
      elif event.axis == 3:
          print("Clutch")


try:
    print('Press [ESC] to quit')
    # checkwheel()
    # Loop indefinitely
    while True:
        # Get the currently pressed keys on the keyboard
        PygameHandler()

        if hadEvent or regularUpdate:

            # Keys have changed, generate the command list based on keys
            hadEvent = False
            driveCommands = ['0', '0', '0', '0', 'X', 'X', 'X'] # Default to do not change
            # lDrives = [MOTOR_RIGHT_FORWARD_PIN, MOTOR_RIGHT_REVERSE_PIN, MOTOR_LEFT_REVERSE_PIN, MOTOR_LEFT_FORWARD_PIN,
            #            SAY_INDEX, PLAY_INDEX, CAMERA_SERVO_INDEX]

            LEFT_DRIVE_REVERSE = 2
            RIGHT_DRIVE_FORWARD = 0
            LEFT_DRIVE_FORWARD = 3
            RIGHT_DRIVE_REVERSE = 1

            if moveUp > 100:
                moveUp = 100
            if moveDown > 100:
                moveDown = 100
            if moveRight > 100:
                moveRight = 100
            if moveLeft > 100:
                moveLeft = 100

            if moveQuit:
                break
            elif (moveUp > 0 and moveLeft > 0):
                driveCommands[RIGHT_DRIVE_FORWARD] = str(moveUp)
                driveCommands[LEFT_DRIVE_FORWARD] = str(moveUp - moveLeft)
                driveCommands[LEFT_DRIVE_REVERSE] = 'OFF'
                driveCommands[RIGHT_DRIVE_REVERSE] = 'OFF'
            elif (moveUp > 0 and moveRight > 0):
                driveCommands[RIGHT_DRIVE_FORWARD] = str(moveUp - moveRight)
                driveCommands[LEFT_DRIVE_FORWARD] = str(moveUp)
                driveCommands[LEFT_DRIVE_REVERSE] = 'OFF'
                driveCommands[RIGHT_DRIVE_REVERSE] = 'OFF'
            elif (moveDown > 0 and moveLeft > 0):
                driveCommands[RIGHT_DRIVE_FORWARD] = 'OFF'
                driveCommands[LEFT_DRIVE_FORWARD] = 'OFF'
                driveCommands[LEFT_DRIVE_REVERSE] = str(moveDown - moveLeft)
                driveCommands[RIGHT_DRIVE_REVERSE] = str(moveDown)
            elif (moveDown > 0 and moveRight > 0):
                driveCommands[RIGHT_DRIVE_FORWARD] = 'OFF'
                driveCommands[LEFT_DRIVE_FORWARD] = 'OFF'
                driveCommands[LEFT_DRIVE_REVERSE] = str(moveDown)
                driveCommands[RIGHT_DRIVE_REVERSE] = str(moveDown - moveRight)
            elif moveUp > 0:
                driveCommands[RIGHT_DRIVE_FORWARD] = str(moveUp)
                driveCommands[LEFT_DRIVE_FORWARD] = str(moveUp)
            elif moveDown > 0:
                driveCommands[LEFT_DRIVE_REVERSE] = str(moveDown)
                driveCommands[RIGHT_DRIVE_REVERSE] = str(moveDown)
            elif moveLeft > 0:
                driveCommands[LEFT_DRIVE_REVERSE] = str(moveLeft)
                driveCommands[RIGHT_DRIVE_FORWARD] = str(moveLeft)
            elif moveRight > 0:
                driveCommands[RIGHT_DRIVE_REVERSE] = str(moveRight)
                driveCommands[LEFT_DRIVE_FORWARD] = str(moveRight)
                driveCommands[RIGHT_DRIVE_FORWARD] = 'OFF'
                driveCommands[LEFT_DRIVE_REVERSE] = 'OFF'
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
            #
            # elif moveLeft > 0:
            #     if moveDown > 0:
            #         driveCommands[RIGHT_DRIVE_FORWARD] = 'OFF'
            #         driveCommands[LEFT_DRIVE_FORWARD] = 'OFF'
            #         driveCommands[LEFT_DRIVE_REVERSE] = 'ON'
            #         driveCommands[RIGHT_DRIVE_REVERSE] = 'OFF'
            #     elif moveUp > 0:
            #         driveCommands[RIGHT_DRIVE_FORWARD] = str(moveUp)
            #         driveCommands[LEFT_DRIVE_FORWARD] = str(moveUp - moveLeft)
            #         driveCommands[LEFT_DRIVE_REVERSE] = 'OFF'
            #         driveCommands[RIGHT_DRIVE_REVERSE] = 'OFF'
            #     else:
            #         driveCommands[LEFT_DRIVE_FORWARD] = 'ON'
            #         driveCommands[RIGHT_DRIVE_FORWARD] = 'OFF'
            #         driveCommands[LEFT_DRIVE_REVERSE] = 'OFF'
            #         driveCommands[RIGHT_DRIVE_REVERSE] = 'ON'
            # elif moveRight > 0:
            #     if moveDown > 0:
            #         driveCommands[RIGHT_DRIVE_FORWARD] = 'OFF'
            #         driveCommands[LEFT_DRIVE_FORWARD] = 'OFF'
            #         driveCommands[LEFT_DRIVE_REVERSE] = 'OFF'
            #         driveCommands[RIGHT_DRIVE_REVERSE] = 'ON'
            #     elif moveUp > 0:
            #         driveCommands[RIGHT_DRIVE_FORWARD] = 'ON'
            #         driveCommands[LEFT_DRIVE_FORWARD] = 'OFF'
            #         driveCommands[RIGHT_DRIVE_REVERSE] = 'OFF'
            #         driveCommands[LEFT_DRIVE_REVERSE] = 'OFF'
            #     else:
            #         driveCommands[RIGHT_DRIVE_FORWARD] = 'ON'
            #         driveCommands[LEFT_DRIVE_FORWARD] = 'OFF'
            #         driveCommands[LEFT_DRIVE_REVERSE] = 'ON'
            #         driveCommands[RIGHT_DRIVE_REVERSE] = 'OFF'
            # elif moveUp > 0:
            #     print("moving up")
            #     driveCommands[LEFT_DRIVE_FORWARD] = str(moveUp)
            #     driveCommands[RIGHT_DRIVE_FORWARD] = str(moveUp)
            #     driveCommands[LEFT_DRIVE_REVERSE] = 'OFF'
            #     driveCommands[RIGHT_DRIVE_REVERSE] = 'OFF'
            # elif moveDown > 0:
            #     driveCommands[LEFT_DRIVE_REVERSE] = str(moveDown)     #Left Drive Reverse
            #     driveCommands[RIGHT_DRIVE_REVERSE] = str(moveDown)    #Right Drive Reverse
            #     driveCommands[LEFT_DRIVE_FORWARD] = 'OFF'
            #     driveCommands[RIGHT_DRIVE_FORWARD] = 'OFF'
            # elif say != "":
            #     driveCommands[sayIndex] = say
            #     say = ""
            # elif cameraMove != "":
            #     print("camera move")
            #     print("camera ", cameraMove)
            #     driveCommands[cameraServoDrive] = cameraMove
            #     cameraMove = ""
            # else:
            #     # None of our expected keys, stop
            #     driveCommands[LEFT_DRIVE_FORWARD] = 'OFF'
            #     driveCommands[RIGHT_DRIVE_FORWARD] = 'OFF'
            #     driveCommands[LEFT_DRIVE_REVERSE] = 'OFF'
            #     driveCommands[RIGHT_DRIVE_REVERSE] = 'OFF'

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