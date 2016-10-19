import threading

from robot.Buttons import Buttons
from robot.Motors import gpio_cleanup, motor_off
from robot.ControlsHandler import *

# What messages to listen for (LEDB on an LCD)
portListen = 9038

def local_controls():
    global isRunning
    # Loop until terminated remotely
    # Infinite loop that will not end until the user presses the exit key



    while isRunning:
        buttonsPressed = Buttons.pressed_buttons()
        for pressedPin in buttonsPressed:
            print("Pin: ", pressedPin)

try:
    global isRunning
    isRunning = True
    # Start by turning all drives off
    motor_off()
    # raw_input('You can now turn on the power, press ENTER to continue')
    # Setup the UDP listener
    # Say("Controls Initialized")
    remoteKeyBorgServer = socketserver.UDPServer(('', portListen), ControlsHandler)
    remoteKeyBorgServer.server_activate()

    # th = threading.Thread(None, remoteKeyBorgServer.serve_forever)
    # th.daemon = True
    # th.start()

    local_controls_thread = threading.Thread(None, local_controls)
    local_controls_thread.daemon = True
    local_controls_thread.start()

    input('threads running')

    # Turn off the drives and release the GPIO pins
    motor_off()
    gpio_cleanup()

except KeyboardInterrupt:
    # CTRL+C exit, turn off the drives and release the GPIO pins
    print('Terminated')
    # Say("Robot Terminated. Keyboard Interrupt")
    motor_off()
    input('Turn the power off now, press ENTER to continue')
    gpio_cleanup() 