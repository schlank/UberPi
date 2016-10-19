import os


class Say(object):
    def __init__(self, something):
        self.say(something)

    def say(self, something):
        os.system('espeak -ven+f3 "{0}"'.format(something))


def say(something):
    Say(something)