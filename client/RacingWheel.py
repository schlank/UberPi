from client.Wheel import Wheel
from robot.Buttons import Button

STEERING_TURBO = 0

class RacingWheel(object):

    leftWheel = None
    rightWheel = None
    leftButton = None
    rightButton = None

    def __init__(self):
        self.leftWheel = Wheel()
        self.rightWheel = Wheel()
        self.leftButton = Button()
        self.rightButton = Button()
        super().__init__()

    def moveRight(self, power):
        power = abs(power)
        if power >= 1:
            power = 100
        else:
            power = (power * 100) + STEERING_TURBO
        self.leftWheel.status = "F"
        self.leftWheel.power = power
        print("moveRight", power)

    def moveLeft(self, power):
        power = abs(power)
        if power >= 1:
            power = 100
        else:
            power = (power * 100) + STEERING_TURBO
        self.rightWheel.status = "F"
        self.rightWheel.power = power
        print("moveLeft", power)

    def moveUp(self, power):
        power *= 100
        power = abs(power)
        self.rightWheel.status = "F"
        self.rightWheel.power = power
        self.leftWheel.status = "F"
        self.leftWheel.power = power
        print("moveUp", power)

    def moveBack(self, power):
        power *= 100
        power = abs(power)
        self.rightWheel.status = "B"
        self.rightWheel.power = power
        self.leftWheel.status = "B"
        self.leftWheel.power = power
        print("moveBack", power)

    def stop(self):
        self.leftWheel.reset()
        self.rightWheel.reset()

    def has_commands(self):
        return self.leftWheel.has_command() or self.rightWheel.has_command()

    def log(self):
        return "LEFT: " + self.leftWheel.log() + "\nRIGHT:" + self.rightWheel.log()