import pickle
import socketserver

from robot.Motors import Motors

# Class used to handle UDP messages
class ControlsHandler(socketserver.BaseRequestHandler):
    # Function called when a new message has been received
    def handle(self):
        global isRunning

        request, socket = self.request  # Read who spoke to us and what they said
        robot_wheels = pickle.loads(request)
        Motors.command(robot_wheels)
