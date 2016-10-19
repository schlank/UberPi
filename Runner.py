import threading

from robot.Buttons import Buttons
from robot.Fan import Fan
from robot.Motors import gpio_cleanup, motor_off
from robot.ControlsHandler import *

# What messages to listen for (LEDB on an LCD)
portListen = 9038


def all_off():
    Motors.all_off()
    Lights.all_off()


def local_controls():
    global isRunning
    # Loop until terminated remotely
    # Infinite loop that will not end until the user presses the exit key

    while isRunning:
        buttons_pressed = Buttons.pressed_buttons()
        for pressedPin in buttons_pressed:
            print("Pin: ", pressedPin)
            # if pressedPin == 27:
            #     print("OFF Button Pressed.")
                # isRunning = False

try:
    global isRunning
    isRunning = True
    # Start by turning all drives off
    motor_off()
    # raw_input('You can now turn on the power, press ENTER to continue')
    # Setup the UDP listener
    # Say("Controls Initialized")

    Fan.start_fan()
    remoteKeyBorgServer = socketserver.UDPServer(('', portListen), ControlsHandler)

    remoteThread = threading.Thread(None, remoteKeyBorgServer.serve_forever)
    remoteThread.daemon = True
    remoteThread.start()

    local_controls_thread = threading.Thread(None, local_controls)
    local_controls_thread.daemon = True
    local_controls_thread.start()

    input('threads running')

    # Turn off the drives and release the GPIO pins
    all_off()
    gpio_cleanup()

except KeyboardInterrupt:
    # CTRL+C exit, turn off the drives and release the GPIO pins
    print('Terminated')
    # Say("Robot Terminated. Keyboard Interrupt")
    all_off()
    input('Turn the power off now, press ENTER to continue')
    gpio_cleanup()
    exit()
