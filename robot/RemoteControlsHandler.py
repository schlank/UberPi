import pickle
import socketserver
import os

from robot.Lights import Lights
from robot.Motors import Motors


def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return res.replace("temp=", "").replace("'C\n", "")


# Class used to handle UDP messages
class RemoteControlsHandler(socketserver.BaseRequestHandler):
    # Function called when a new message has been received
    def handle(self):
        global isRunning

        request, socket = self.request  # Read who spoke to us and what they said

        pickles = pickle.loads(request)
        racing_wheel = pickles[0]
        Motors.command(racing_wheel)

        racing_wheel_button_test = pickles[1]
        Motors.command(racing_wheel_button_test)

        keyboard_controls = pickles[2]
        Motors.command(keyboard_controls)

        light_status = pickles[3]
        Lights.command(light_status)


        #cpu_temp = getCPUtemperature()
        # print("CPU", cpu_temp)



