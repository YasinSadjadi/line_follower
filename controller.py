import io_interface
import io_interface as io
from flags import SteeringFlags


class Controller:
    # initializing motors
    _LEFT_MOTOR = io.Motor(8, 10, 11)
    _RIGHT_MOTOR = io.Motor(29, 31, 33)
    _SERVO = io.Steer(32)

    # values for mapping speed and steer angle
    _MIN_SPEED = 30
    _MAX_SPEED = 100

    _MIN_STEER_ANGLE = 60
    _MAX_STEER_ANGLE = 120

    @staticmethod
    def adjust_steer(steer_value):
        if steer_value == SteeringFlags.STRAIGHT:
            Controller._SERVO.set_angle(90)
            Controller.set_speed(left_speed=Controller._MAX_SPEED,
                                 right_speed=Controller._MAX_SPEED)

        elif steer_value == SteeringFlags.SLOW_RIGHT:
            Controller._SERVO.set_angle(100)
            Controller.set_speed(left_speed=Controller._MAX_SPEED, right_speed=Controller._MIN_SPEED)

        elif steer_value == SteeringFlags.FAST_RIGHT:
            Controller._SERVO.set_angle(Controller._MAX_STEER_ANGLE)
            Controller.set_speed(left_speed=Controller._MAX_SPEED, right_speed=- Controller._MIN_SPEED)

        elif steer_value == SteeringFlags.SLOW_LEFT:
            Controller._SERVO.set_angle(80)
            Controller.set_speed(left_speed=Controller._MIN_SPEED, right_speed=Controller._MAX_SPEED)
        elif steer_value == SteeringFlags.FAST_LEFT:
            Controller._SERVO.set_angle(Controller._MIN_STEER_ANGLE)
            Controller.set_speed(left_speed=- Controller._MIN_SPEED, right_speed=Controller._MAX_SPEED)

        elif steer_value == SteeringFlags.REVERSE:
            Controller._SERVO.set_angle(90)
            Controller.set_speed(left_speed=- Controller._MAX_SPEED, right_speed=- Controller._MAX_SPEED)
        else:
            print("Invalid steering value")

    @staticmethod
    def _map_value(value, in_min, in_max, out_min, out_max):
        return (value - in_min) * (out_max - out_min) / (in_max - in_min) + out_min

    @staticmethod
    def _constrain_value(value, min_value, max_value):
        return max(min_value, min(value, max_value))

    @staticmethod
    def stop():
        Controller._LEFT_MOTOR.stop()
        Controller._RIGHT_MOTOR.stop()

    @staticmethod
    def set_speed(left_speed, right_speed):
        if left_speed < 0:
            left_speed = -left_speed
            if not Controller._LEFT_MOTOR.backward_flag:
                Controller._LEFT_MOTOR.backward()
        else:
            if not Controller._LEFT_MOTOR.forward_flag:
                Controller._LEFT_MOTOR.forward()

        if right_speed < 0:
            right_speed = -right_speed
            if not Controller._RIGHT_MOTOR.backward_flag:
                Controller._RIGHT_MOTOR.backward()
        else:
            if not Controller._RIGHT_MOTOR.forward_flag:
                Controller._RIGHT_MOTOR.forward()

        left_speed = Controller._constrain_value(left_speed, Controller._MIN_SPEED, Controller._MAX_SPEED)
        right_speed = Controller._constrain_value(right_speed, Controller._MIN_SPEED, Controller._MAX_SPEED)

        # setting motor speeds
        Controller._LEFT_MOTOR.set_speed(left_speed)
        Controller._RIGHT_MOTOR.set_speed(right_speed)

    @staticmethod
    def set_steer_angle(steer_angle):
        # validating input values
        steer_angle = Controller._constrain_value(steer_angle, Controller._MIN_STEER_ANGLE,
                                                  Controller._MAX_STEER_ANGLE)
        Controller._SERVO.set_angle(steer_angle)

    @staticmethod
    def cleanup():
        Controller._SERVO.set_angle(90)
        Controller.stop()
        Controller._SERVO.cleanup()
        Controller._LEFT_MOTOR.cleanup()
        Controller._RIGHT_MOTOR.cleanup()
        io_interface.cleanup()
