class Wheel:
    def __init__(self):
        self.status = "X"
        self.power = 0
        super().__init__()

    def getStatus(self):
        return self.status

    def getPower(self):
        return self.power

    def reset(self):
        self.status = "X"
        self.power = 0

    def stop(self):
        self.status = "S"
        self.power = 0

    def has_command(self):
        return self.status != "X"

    def log(self):
        return "Status:" + \
               self.status + \
               "Power: " + \
               str(self.power)
