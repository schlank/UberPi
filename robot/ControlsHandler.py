import pickle

from client import RobotWheels
from robot.Motors import *


# Class used to handle UDP messages
class ControlsHandler(socketserver.BaseRequestHandler):
    # Function called when a new message has been received
    def handle(self):
        global isRunning

        request, socket = self.request  # Read who spoke to us and what they said

        robot_wheels = pickle.unpack(request)
        print(robot_wheels)