from client.ServoStatus import ServoStatus


class ServoStatusFactory:

    @staticmethod
    def create_servo_status_w_racing_wheel(racing_wheel):
        direction = None
        if racing_wheel.leftShiftButton:
            direction = "DOWN"
        elif racing_wheel.rightShiftButton:
            direction = "UP"
        if direction is not None:
            print(racing_wheel)
            return ServoStatus(direction)
        return None




