from robot.Buttons import Buttons
from robot.Motors import gpio_cleanup, motor_off
from robot.ControlsHandler import *

portListen = 9038 # What messages to listen for (LEDB on an LCD)

try:
    global isRunning

    # Start by turning all drives off
    motor_off()
    # raw_input('You can now turn on the power, press ENTER to continue')
    # Setup the UDP listener
    # Say("Controls Initialized")
    remoteKeyBorgServer = socketserver.UDPServer(('', portListen), ControlsHandler)
    # Loop until terminated remotely
    isRunning = True
    # Infinite loop that will not end until the user presses the exit key

    remoteKeyBorgServer.handle_request()

    while isRunning:
        buttonsPressed = Buttons.pressed_buttons()
        for pressedPin in buttonsPressed:
            if pressedPin == 23:
                isRunning = False
            print("Pin: ", pressedPin)

    # Turn off the drives and release the GPIO pins
    print('Finished')
    # Say("System controls offline.")
    motor_off()
    input('Turn the power off now, press ENTER to continue')
    gpio_cleanup()

except KeyboardInterrupt:
    # CTRL+C exit, turn off the drives and release the GPIO pins
    print('Terminated')
    # Say("Robot Terminated. Keyboard Interrupt")
    motor_off()
    input('Turn the power off now, press ENTER to continue')
    gpio_cleanup() 