class Wheel:

    def __init__(self):
        self.status = "X"
        self.power = 0
        super().__init__()

    def getStatus(self):
        return self.status

    def reset(self):
        self.status = "X"
        self.power = 0