from client.ServoStatus import ServoStatus


class ServoStatusFactory:

    @staticmethod
    def create_servo_status_w_racing_wheel(racing_wheel):
        direction = None
        if racing_wheel.leftShiftButton.on:
            direction = "DOWN"
        elif racing_wheel.rightShiftButton.on:
            direction = "UP"
        if direction is not None:
            print(direction)
            return ServoStatus(direction)
        return None




