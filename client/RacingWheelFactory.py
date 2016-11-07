import os

# make sure pygame doesn't try to open an output window
import pygame

from client.RacingWheel import RacingWheel

# Not screenpygame
os.environ["SDL_VIDEODRIVER"] = "dummy"
# Setup pygame and key states
pygame.init()

WHEEL = "G27 Racing Wheel"

PEDAL_THRESHOLD = 0
DEBUG = True
axis_mode = 1

PEDAL_DEAD_ZONE = .4
STEERING_DEAD_ZONE = 20

gear_lever_positions = {
    -1: "reverse",
    0: "neutral",
    1: "first",
    2: "second",
    3: "third",
    4: "fourth",
    5: "fifth",
    6: "sixth"
}

status_buttons = {
    10: "parking_brake_status",
    1: "headlamp_status",
    3: "high_beam_status",
    2: "windshield_wiper_status"
}

gear_lever_position = 0
parking_brake_status = False
headlamp_status = False
high_beam_status = False
windshield_wiper_status = False


class RacingWheelFactory:
    @staticmethod
    def create_racing_wheel_w_keyboard():
        global had_keyboard_event
        global move_quit

        had_keyboard_event = False
        racing_wheel = RacingWheel()
        events = pygame.event.get()
        # Handle each event individually
        for event in events:
            if event.type == pygame.QUIT:
                # User exit
                had_keyboard_event = True
                move_quit = True
            elif event.type == pygame.KEYDOWN:
                # A key has been pressed, see if it is one we want
                had_keyboard_event = True
                if event.key == pygame.K_UP:
                    racing_wheel.leftWheel.power = 100
                    racing_wheel.leftWheel.status = "F"
                    racing_wheel.rightWheel.power = 100
                    racing_wheel.rightWheel.status = "F"
                elif event.key == pygame.K_DOWN:
                    racing_wheel.leftWheel.power = 100
                    racing_wheel.leftWheel.status = "B"
                    racing_wheel.rightWheel.power = 100
                    racing_wheel.rightWheel.status = "B"
                elif event.key == pygame.K_LEFT:
                    racing_wheel.leftWheel.power = 100
                    racing_wheel.leftWheel.status = "B"
                    racing_wheel.rightWheel.power = 100
                    racing_wheel.rightWheel.status = "F"
                elif event.key == pygame.K_RIGHT:
                    racing_wheel.leftWheel.power = 100
                    racing_wheel.leftWheel.status = "F"
                    racing_wheel.rightWheel.power = 100
                    racing_wheel.rightWheel.status = "B"
                elif event.key == pygame.K_ESCAPE:
                    move_quit = True
            elif event.type == pygame.KEYUP:
                had_keyboard_event = True
                # A key has been released, see if it is one we want
                if event.key == pygame.K_UP:
                    racing_wheel.stop()
                elif event.key == pygame.K_DOWN:
                    racing_wheel.stop()
                elif event.key == pygame.K_LEFT:
                    racing_wheel.stop()
                elif event.key == pygame.K_RIGHT:
                    racing_wheel.stop()
                elif event.key == pygame.K_ESCAPE:
                    racing_wheel.stop()
        return racing_wheel

    @staticmethod
    def create_racing_wheel_w_buttons():
        racing_wheel = RacingWheel()
        for event in pygame.event.get(pygame.QUIT):
            exit(0)
        for event in pygame.event.get(pygame.JOYBUTTONUP):
            if DEBUG:
                print("Released button is", event.button)
            if (12 <= event.button <= 17) or event.button == 22:
                gear = 0
                print("a Gear")
                # send_data("gear_lever_position", gear_lever_positions[gear])
        for event in pygame.event.get(pygame.JOYBUTTONDOWN):
            if DEBUG:
                print("Pressed button is", event.button)
            if event.button == 0:
                print("pressed button 0 - bye...")
                # stop()
                exit(0)
            elif event.button == 4:
                print("Camera Up")
            elif event.button == 5:
                print("Camera Down")
            elif event.button == 11:
                # send_data("ignition_status", "start")
                print("Start Button")
            elif 12 <= event.button <= 17:
                gear = event.button - 11
                print("gear")
                # send_data("gear_lever_pgear_lever_position", gear_lever_positions[gear])
            elif event.button == 22:
                print("button 22")
                gear = -1
                # send_data("gear_lever_position", gear_lever_positions[gear])
            elif event.button in status_buttons:
                print(status_buttons[event.button])
            print(event.button)
            print(event)
        return racing_wheel

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
                    if power_value < STEERING_DEAD_ZONE:
                        racingWheel.moveRight(0)
                    else:
                        racingWheel.moveRight(event.value)
                elif event.value < 0:
                    if power_value < STEERING_DEAD_ZONE:
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
                if DEBUG:
                    print(event.value)
            # BRAKE PEDAL AXIS
            elif event.axis == 2:
                if DEBUG:
                    print("Brake Pedal")
                if event.value < 0:
                    if DEBUG:
                        print("BRAKE ON")
                else:
                    if DEBUG:
                        print("BRAKE OFF")
            # CLUTCH PEDAL AXIS
            elif event.axis == 3:
                if DEBUG:
                    print("Clutch")
            else:
                if DEBUG:
                    print("Event", event)
                racingWheel.stop()
        for event in pygame.event.get(pygame.JOYBUTTONDOWN):
            if DEBUG:
                if DEBUG:
                    print("Pressed button is", event.button)
            if event.button == 0:
                if DEBUG:
                    print("pressed button 0 - bye...")
                exit(0)
            elif event.button == 6:
                racingWheel.rightButton.on = True
            elif event.button == 7:
                racingWheel.leftButton.on = True
            elif event.button == 4:
                racingWheel.rightShiftButton.on = True
            elif event.button == 5:
                racingWheel.leftShiftButton.on = True

        return racingWheel
