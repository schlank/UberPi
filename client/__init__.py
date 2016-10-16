import pygame


def checkwheel(wheel_name):
    usewheel = False
    try:
        wheel = None
        for j in range(0, pygame.joystick.get_count()):
            if pygame.joystick.Joystick(j).get_name() == wheel_name:
                wheel = pygame.joystick.Joystick(j)
                wheel.init()
                print ("Found", wheel.get_name())
                usewheel = True

        if not wheel:
            print ("No G27 steering wheel found")
        return usewheel
    except Exception as e:
        print(e)