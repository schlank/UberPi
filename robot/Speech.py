import os


class Say:
    def __init__(self, something):
        self.say(something)

    def say(something):
        os.system('espeak -ven+f3 "{0}"'.format(something))


def say(something):
    Say(something)