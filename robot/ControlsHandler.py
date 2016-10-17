import pickle
import socketserver
import os

from robot.Motors import Motors


def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return(res.replace("temp=","").replace("'C\n",""))


# Class used to handle UDP messages
class ControlsHandler(socketserver.BaseRequestHandler):
    # Function called when a new message has been received
    def handle(self):
        global isRunning

        request, socket = self.request  # Read who spoke to us and what they said
        robot_wheels = pickle.loads(request)
        Motors.command(robot_wheels)
        #cpu_temp = getCPUtemperature()
        # print("CPU", cpu_temp)

