from client.LightStatus import LightStatus


class LightStatusFactory:
    @staticmethod
    def create_light_status_from_wheel(racing_wheel):
        print(racing_wheel)
        if racing_wheel.leftButton.on:
            return LightStatus(True)
        elif racing_wheel.rightButton.on:
            return LightStatus(False)
