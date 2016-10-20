#!/usr/bin/env python

# Load library functions we want
import socket
import time

# Settings for the RemoteKeyBorg client
import pickle

from client import check_wheel
from client.LightStatusFactory import LightStatusFactory
from client.RacingWheelFactory import RacingWheelFactory

DEBUG = True
WHEEL_NAME = "G27 Racing Wheel"
USE_WHEEL = True
axis_mode = 1
gstreamIP = "10.215.50.46"
GSTREAM_PORT = "5000"
START_GSTREAM = False
broadcastIP = "10.215.50.46"            # IP address to send to, 255 in one or more positions is a broadcast / wild-card
broadcastPort = 9038                    # What message number to send with (LEDB on an LCD)

LEFT_DRIVE_REVERSE = 3
LEFT_DRIVE_FORWARD = 2
RIGHT_DRIVE_FORWARD = 1
RIGHT_DRIVE_REVERSE = 0
sayIndex = 4
cameraServoDrive = 6
playIndex = 5

interval = 0.3                          # Time between keyboard updates in seconds, smaller responds faster but uses more processor time
regularUpdate = True                    # If True we send a command at a regular interval, if False we only send commands when keys are pressed or released

# Setup the connection for sending on
sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)       # Create the socket3
sender.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)                        # Enable broadcasting (sending to many IPs based on wild-cards)
sender.bind(('0.0.0.0', 0))                                                         # Set the IP and port number to use locally, IP 0.0.0.0 means all connections and port 0 means assign a number for us (do not care)

def sendWheels(robotWheels):
    if robotWheels is None:
        robotWheels = RacingWheelFactory.createRacingWheel()
    pickedWheels = pickle.dumps(robotWheels, -1)
    sender.sendto(pickedWheels, (broadcastIP, broadcastPort))


def allStop():
    sendWheels(None)
    print("allStop")

try:

    global motorsStopped
    motorsStopped = False
    print('Press [ESC] to quit')
    # Is the racing wheel connected?
    if check_wheel(WHEEL_NAME):
        print("Wheel not found: " + WHEEL_NAME)
        allStop()
        pass

    # Loop indefinitely
    while True:
        # Get the currently pressed keys on the keyboard
        # Handle Inputs from G27 Racing Wheel and pedal
        racingWheel = RacingWheelFactory.createRacingWheel()

        racingWheelTest = RacingWheelFactory.create_racing_wheel_w_buttons()

        # Keyboard input is used to create the same object as the wheel.
        keyboardControls = RacingWheelFactory.create_racing_wheel_w_keyboard()

        # LED Headlamp is turned on and off from racing wheel buttons.
        lights = LightStatusFactory.create_light_status_from_wheel_buttons(racingWheel)

        pickles = [racingWheel, racingWheelTest, keyboardControls, lights]

        if regularUpdate or racingWheel.has_commands() or keyboardControls.has_commands():
            pickled_controls = pickle.dumps(pickles, -1)
            sender.sendto(pickled_controls, (broadcastIP, broadcastPort))
            # Wait for the interval period
            time.sleep(interval)

    # Inform the server to stop
    allStop()
except KeyboardInterrupt:
    # CTRL+C exit, inform the server to stop
    allStop()
