import pickle
import socketserver
import os

from client.LightStatus import LightStatus
from client.RacingWheel import RacingWheel
from robot.Lights import Lights
from robot.Motors import Motors


def getCPUtemperature():
    res = os.popen('vcgencmd measure_temp').readline()
    return res.replace("temp=", "").replace("'C\n", "")

def run_pickle(pickl):
    if type(pickl) is RacingWheel:
        Motors.command(pickl)
    elif type(pickl) is LightStatus:
        Lights.command(pickl)
    else:
        print("Unhandled Pickle")

# Class used to handle UDP messages
class RemoteControlsHandler(socketserver.BaseRequestHandler):
    # Function called when a new message has been received
    def handle(self):
        global isRunning

        request, socket = self.request  # Read who spoke to us and what they said

        pickles = pickle.loads(request)


        if pickles is not list:
            run_pickle(pickles)
        else:
            for one_pickle in pickles:
                run_pickle(one_pickle)

        #cpu_temp = getCPUtemperature()
        # print("CPU", cpu_temp)



