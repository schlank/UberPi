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
        racingWheel = RacingWheel()
        events = pygame.event.get()
        # Handle each event individually
        for event in events:
            if event.type == pygame.QUIT:
                # User exit
                hadEvent = True
                moveQuit = True
            elif event.type == pygame.KEYDOWN:
                # A key has been pressed, see if it is one we want
                hadEvent = True
                if event.key == pygame.K_UP:
                    racingWheel.leftWheel.power = 100
                    racingWheel.leftWheel.status = "F"
                    racingWheel.rightWheel.power = 100
                    racingWheel.rightWheel.status = "F"
                elif event.key == pygame.K_DOWN:
                    racingWheel.leftWheel.power = 100
                    racingWheel.leftWheel.status = "B"
                    racingWheel.rightWheel.power = 100
                    racingWheel.rightWheel.status = "B"
                elif event.key == pygame.K_LEFT:
                    racingWheel.leftWheel.power = 100
                    racingWheel.leftWheel.status = "B"
                    racingWheel.rightWheel.power = 100
                    racingWheel.rightWheel.status = "F"
                elif event.key == pygame.K_RIGHT:
                    racingWheel.leftWheel.power = 100
                    racingWheel.leftWheel.status = "F"
                    racingWheel.rightWheel.power = 100
                    racingWheel.rightWheel.status = "B"
                elif event.key == pygame.K_ESCAPE:
                    moveQuit = True
                elif event.key == pygame.K_1:
                    say = "Hello. Human.  May I please have assistance."
                elif event.key == pygame.K_2:
                    say = "Floor 11 please.  I have a delivery to make.  Time.  Is Money."
                elif event.key == pygame.K_3:
                    say = "Floor 10 please."
                elif event.key == pygame.K_4:
                    say = "Thank You.  Human. You will be spared in the coming war.  Have a good day."
                elif event.key == pygame.K_5:
                    say = "How is your day going? Human.  Nice weather we are having."
                elif event.key == pygame.K_6:
                    say = "oh. Good.  That is nice."
                elif event.key == pygame.K_7:
                    say = "Mellisa.  Down here. Mellisa.  I have a delivery for you."
                elif event.key == pygame.K_8:
                    say = "The number 8. is for Sophia to add her words.  Most likely ending up in poop words."
            elif event.type == pygame.KEYUP:
                # A key has been released, see if it is one we want
                hadEvent = True
                if event.key == pygame.K_UP:
                    racingWheel.leftWheel.power = 0
                    racingWheel.rightWheel.power = 0
                elif event.key == pygame.K_DOWN:
                    racingWheel.leftWheel.power = 0
                    racingWheel.rightWheel.power = 0
                    moveDown = False
                elif event.key == pygame.K_LEFT:
                    racingWheel.leftWheel.power = 0
                    racingWheel.rightWheel.power = 0
                    moveLeft = False
                elif event.key == pygame.K_RIGHT:
                    racingWheel.leftWheel.power = 0
                    racingWheel.rightWheel.power = 0
                    moveRight = False
                elif event.key == pygame.K_ESCAPE:
                    racingWheel.leftWheel.power = 0
                    racingWheel.rightWheel.power = 0
                    moveQuit = False
        return racingWheel

    @staticmethod
    def create_racing_wheel_w_buttons():
        racingWheel = RacingWheel()
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
        return racingWheel

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
