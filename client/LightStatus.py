

class LightStatus:

    is_light_on = False


class LightStatusFactory:

    @staticmethod
    def create_lights():
        lights = LightStatus()
        lights.is_light_on = True
        return lights