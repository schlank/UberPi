import os

# make sure pygame doesn't try to open an output window
import pygame

from client.RacingWheel import RacingWheel

os.environ["SDL_VIDEODRIVER"] = "dummy"
# Setup pygame and key states
pygame.init()

WHEEL = "G27 Racing Wheel"

PEDAL_THRESHOLD = 0
DEBUG = True
axis_mode = 1

PEDAL_DEADZONE = .4
STEERING_DEADZONE = 20


class RacingWheelFactory:

    @staticmethod
    def createRacingWheel():
        racingWheel = RacingWheel()

        for event in pygame.event.get(pygame.JOYAXISMOTION):
            if DEBUG:
                print("Motion on axis: ", event.axis)

            # WHEEL AXIS
            if event.axis == 0:
                power_value = abs(event.value) * 100
                # Steering Wheel - Move right
                if event.value > 0:
                    if power_value < STEERING_DEADZONE:
                        racingWheel.moveRight(0)
                    else:
                        racingWheel.moveRight(event.value)
                elif event.value < 0:
                    if power_value < STEERING_DEADZONE:
                        racingWheel.moveLeft(0)
                    else:
                        racingWheel.moveLeft(event.value)

            # GAS PEDAL
            elif event.axis == 1 and axis_mode == 1:
                if event.value * -100 > PEDAL_THRESHOLD:
                    racingWheel.moveUp(event.value)
                elif event.value * 100 > PEDAL_THRESHOLD:
                    racingWheel.moveBack(event.value)
            elif event.axis == 1 and axis_mode == 2:
                print(event.value)
                print("~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~~sAxis_mode 2")
            # BRAKE PEDAL AXIS
            elif event.axis == 2:
                print("Brake Pedal")
                if event.value < 0:
                    print("BRAKE ON")
                    moveDown = 0
                else:
                    print("BRAKE OFF")
            # CLUTCH PEDAL AXIS
            elif event.axis == 3:
                print("Clutch")
            else:
                print("Event", event)
                racingWheel.stop()
        for event in pygame.event.get(pygame.JOYBUTTONDOWN):
            if DEBUG:
                print("Pressed button is", event.button)
            if event.button == 0:
                print("pressed button 0 - bye...")
                exit(0)
            elif event.button == 6:
                racingWheel.rightButton.on = True
                print("Button", 6)
            elif event.button == 7:
                racingWheel.leftButton.on = True
                print("Button", 7)

        return racingWheel
