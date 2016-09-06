#!/usr/bin/env python
# coding: Latin-1

# Load library functions we want
import socket
import time
import pygame
import os

# Settings for the RemoteKeyBorg client
gstreamIP = "10.215.50.45"
broadcastIP = "10.215.50.255"            # IP address to send to, 255 in one or more positions is a broadcast / wild-card
broadcastPort = 9038                    # What message number to send with (LEDB on an LCD)
leftDrive = 4                           # Drive number for left motor
rightDrive = 1                          # Drive number for right motor
sayDrive = 5
playDrive = 6
interval = 0.1                          # Time between keyboard updates in seconds, smaller responds faster but uses more processor time
regularUpdate = True                    # If True we send a command at a regular interval, if False we only send commands when keys are pressed or released

# Setup the connection for sending on
sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)       # Create the socket
sender.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)                        # Enable broadcasting (sending to many IPs based on wild-cards)
sender.bind(('0.0.0.0', 0))                                                         # Set the IP and port number to use locally, IP 0.0.0.0 means all connections and port 0 means assign a number for us (do not care)

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
moveUp = False
moveDown = False
moveLeft = False
moveRight = False
moveQuit = False
say = ""
play = ""
pygame.init()
screen = pygame.display.set_mode([300,300])
pygame.display.set_caption("RemoteKeyBorg - Press [ESC] to quit")
systemCommand = "./startGstreamViewer.sh %s &" % gstreamIP
print systemCommand

os.system(systemCommand)

# Function to handle pygame events
def PygameHandler(events):
    # Variables accessible outside this function
    global hadEvent
    global moveUp
    global moveDown
    global moveLeft
    global moveRight
    global moveQuit
    global say
    global play
    # Handle each event individually
    for event in events:
        if event.type == pygame.QUIT:
            # User exit
            hadEvent = True
            moveQuit = True
        elif event.type == pygame.KEYDOWN:
            # A key has been pressed, see if it is one we want
            hadEvent = True
            if event.key == pygame.K_UP:
                print "UP"
                moveUp = True
            elif event.key == pygame.K_DOWN:
                moveDown = True
            elif event.key == pygame.K_LEFT:
                moveLeft = True
            elif event.key == pygame.K_RIGHT:
                moveRight = True
            elif event.key == pygame.K_ESCAPE:
                moveQuit = True
            elif event.key == pygame.K_1:
                say = "Hello. Human.  May I please have assistance."
            elif event.key == pygame.K_2:
                say = "Floor 11 please.  I have a delivery to make.  Time.  Is Money."
            elif event.key == pygame.K_3:
                say = "Floor 10 please."
            elif event.key == pygame.K_4:
                say = "Thank You.  Human. You will be spared in the coming war.  Have a good day."
            elif event.key == pygame.K_5:
                say = "How is your day going? Human.  Nice weather we are having."
            elif event.key == pygame.K_6:
                say = "oh. Good.  That is nice."
            elif event.key == pygame.K_7:
                say = "Mellisa.  Down here. Mellisa.  I have a delivery for you."
            elif event.key == pygame.K_8:
                say = "The number 8. is for Sophia to add her words.  Most likely ending up in poop words."
        elif event.type == pygame.KEYUP:
            # A key has been released, see if it is one we want
            hadEvent = True
            if event.key == pygame.K_UP:
                print "UP KEYUP"
                moveUp = False
            elif event.key == pygame.K_DOWN:
                moveDown = False
            elif event.key == pygame.K_LEFT:
                moveLeft = False
            elif event.key == pygame.K_RIGHT:
                moveRight = False
            elif event.key == pygame.K_ESCAPE:
                moveQuit = False

try:
    print 'Press [ESC] to quit'
    # Loop indefinitely
    while True:
        # Get the currently pressed keys on the keyboard
        PygameHandler(pygame.event.get())
        if hadEvent or regularUpdate:
            # Keys have changed, generate the command list based on keys
            hadEvent = False
            driveCommands = ['X', 'X', 'X', 'X', 'X', 'X']                    # Default to do not change

            LEFT_DRIVE_REVERSE = leftDrive - 2;
            LEFT_DRIVE_FORWARD = leftDrive - 1;
            RIGHT_DRIVE_FORWARD = rightDrive - 1;
            RIGHT_DRIVE_REVERSE = rightDrive;

            if moveQuit:
                break
            elif moveLeft:
                if moveUp:
                    driveCommands[LEFT_DRIVE_FORWARD] = 'MEDIUM'
                    driveCommands[RIGHT_DRIVE_FORWARD] = 'ON'
                    print("moving up and left")
                else:
                    driveCommands[LEFT_DRIVE_REVERSE] = 'ON'
                    driveCommands[RIGHT_DRIVE_FORWARD] = 'ON'
            elif moveRight:
                if moveUp:
                    print("moving up and right")
                    driveCommands[LEFT_DRIVE_FORWARD] = 'ON'
                    driveCommands[RIGHT_DRIVE_FORWARD] = 'MEDIUM'
                else:
                    driveCommands[LEFT_DRIVE_FORWARD] = 'ON'
                    driveCommands[RIGHT_DRIVE_REVERSE] = 'ON'
            elif moveUp:
                print("moving up")
                driveCommands[LEFT_DRIVE_FORWARD] = 'ON'
                driveCommands[RIGHT_DRIVE_FORWARD] = 'ON'
                driveCommands[LEFT_DRIVE_REVERSE] = 'OFF'
                driveCommands[RIGHT_DRIVE_REVERSE] = 'OFF'
            elif moveDown:
                driveCommands[LEFT_DRIVE_REVERSE] = 'ON' #Left Drive Reverse
                driveCommands[RIGHT_DRIVE_REVERSE] = 'ON'    #Right Drive Reverse
                driveCommands[LEFT_DRIVE_FORWARD] = 'OFF'
                driveCommands[RIGHT_DRIVE_FORWARD] = 'OFF'
            elif say != "":
                driveCommands[sayDrive] = say
                say = ""
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