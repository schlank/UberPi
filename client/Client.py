#!/usr/bin/env python

# Load library functions we want
import socket
import threading
import time

# Settings for the RemoteKeyBorg client
import pickle

from client import check_wheel
from client.LightStatusFactory import LightStatusFactory
from client.RacingWheelFactory import RacingWheelFactory
from client.ServoStatusFactory import ServoStatusFactory

DEBUG = True
WHEEL_NAME = "G27 Racing Wheel"
USE_WHEEL = False
axis_mode = 1
gstreamIP = "10.215.50.56"
GSTREAM_PORT = "5000"
START_GSTREAM = False
broadcastIP = "10.215.50.56"  # IP address to send to, 255 in one or more positions is a broadcast / wild-card
broadcastPort = 9038  # What message number to send with (LEDB on an LCD)

LEFT_DRIVE_REVERSE = 3
LEFT_DRIVE_FORWARD = 2
RIGHT_DRIVE_FORWARD = 1
RIGHT_DRIVE_REVERSE = 0
sayIndex = 4
cameraServoDrive = 6
playIndex = 5

interval = 0.1  # Time between keyboard updates in seconds, smaller responds faster but uses more processor time
regularUpdate = True  # If True we send a command at a regular interval, if False we only send commands when keys are pressed or released

# Setup the connection for sending on
# Create the socket3
sender = socket.socket(socket.AF_INET, socket.SOCK_DGRAM, socket.IPPROTO_UDP)

# Enable broadcasting (sending to many IPs based on wild-cards)
sender.setsockopt(socket.SOL_SOCKET, socket.SO_BROADCAST, 1)

# Set the IP and port number to use locally, IP 0.0.0.0 means all connections and port 0 means assign a number for us (do not care)
sender.bind(('0.0.0.0', 0))

global motors_stopped
global globalWheel

def all_stop():
    global motors_stopped
    send_wheels(None)
    motors_stopped = True
    print("allStop")


def send_wheels(robot_wheels):
    if robot_wheels is None:
        robot_wheels = RacingWheelFactory.createRacingWheel()
    picked_wheels = pickle.dumps(robot_wheels, -1)
    sender.sendto(picked_wheels, (broadcastIP, broadcastPort))


def send_data(pickles):
    if len(pickles) > 0 or regularUpdate:
        pickled_controls = pickle.dumps(pickles, -1)
        sender.sendto(pickled_controls, (broadcastIP, broadcastPort))
        if len(pickles) > 0:
            print("pickles Sending", len(pickles))


def check_controls():
    pickles = []
    # Get the currently pressed keys on the keyboard
    # Handle Inputs from G27 Racing Wheel and pedal
    racing_wheel = RacingWheelFactory.createRacingWheel()
    if racing_wheel.has_commands():
        pickles.append(racing_wheel)

    # LED Headlamp is turned on and off from racing wheel buttons.

    lights = LightStatusFactory.create_light_status_from_wheel_buttons(racing_wheel)
    if lights:
        pickles.append(lights)

    servo_status = ServoStatusFactory.create_servo_status_w_racing_wheel(racing_wheel)
    if servo_status:
        pickles.append(servo_status)

    # racingWheelTest = RacingWheelFactory.create_racing_wheel_w_buttons()
    # if racingWheelTest.has_commands():
    #     pickles.append(racingWheelTest)

    # Keyboard input is used to create the same object as the wheel.
    keyboard_controls = RacingWheelFactory.create_racing_wheel_w_keyboard()
    if keyboard_controls.has_commands():
        pickles.append(keyboard_controls)

    send_data(pickles)

try:

    global motors_stopped
    motors_stopped = False
    print('Press [ESC] to quit')
    # Is the racing wheel connected?
    if check_wheel(WHEEL_NAME) and USE_WHEEL:
        print("Wheel not found: " + WHEEL_NAME)
        all_stop()

    # Loop indefinitely
    while not motors_stopped:
        check_controls()

        # threading.Timer(interval, check_controls).start()
        # time.sleep(interval)

    # Inform the server to stop
    # all_stop()
except KeyboardInterrupt:
    # CTRL+C exit, inform the server to stop
    all_stop()
