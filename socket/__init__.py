import os, time, socketserver


try:
    global isRunning

    # Start by turning all drives off
    MotorOff()
    # raw_input('You can now turn on the power, press ENTER to continue')
    # Setup the UDP listener
    say("Controls Initialized")
    remoteKeyBorgServer = socketserver.UDPServer(('', portListen), PicoBorgHandler)
    # Loop until terminated remotely
    isRunning = True
    while isRunning:
        remoteKeyBorgServer.handle_request()
    # Turn off the drives and release the GPIO pins
    print('Finished')
    say("System controls offline.")
    MotorOff()
    raw_input('Turn the power off now, press ENTER to continue')
    GPIO.cleanup()

except KeyboardInterrupt:
    # CTRL+C exit, turn off the drives and release the GPIO pins
    print('Terminated')
    say("Robot Terminated. Keyboard Interrupt")
    MotorOff()
    # raw_input('Turn the power off now, press ENTER to continue')
    GPIO.cleanup()