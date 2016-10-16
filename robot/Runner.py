from robot import ControlsHandler
from robot.Motors import *
from robot.Speech import *

# Settings for the RemoteKeyBorg server
portListen = 9038 # What messages to listen for (LEDB on an LCD)
isRunning = False

try:
    global isRunning

    # Start by turning all drives off
    MotorOff()
    # raw_input('You can now turn on the power, press ENTER to continue')
    # Setup the UDP listener
    Say("Controls Initialized")
    remoteKeyBorgServer = socketserver.UDPServer(('', portListen), ControlsHandler)
    # Loop until terminated remotely
    isRunning = True
    while isRunning:
        remoteKeyBorgServer.handle_request()
    # Turn off the drives and release the GPIO pins
    print('Finished')
    Say("System controls offline.")
    MotorOff()
    #raw_input('Turn the power off now, press ENTER to continue')
    GPIOCleanup()

except KeyboardInterrupt:
    # CTRL+C exit, turn off the drives and release the GPIO pins
    print('Terminated')
    Say("Robot Terminated. Keyboard Interrupt")
    MotorOff()
    # raw_input('Turn the power off now, press ENTER to continue')
    GPIOCleanup()