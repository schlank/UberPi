class LightStatus:

    on = False

    def __init__(self, on):
        self.on = on
        super().__init__()


class LightStatusFactory:

    @staticmethod
    def create_light_status():
        return LightStatus(True)
