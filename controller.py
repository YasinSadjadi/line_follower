import io_interface
import io_interface as io
from flags import SteeringFlags


class Controller:
    # initializing motors
    _left_motor = io.Motor(8, 10, 11)
    _right_motor = io.Motor(29, 31, 33)
    _steer = io.Steer(32)

    # values
    _MAX_SPEED = 100
    _MIN_SPEED = 50
    _MAX_STEER = 120
    _MIN_STEER = 60

    @staticmethod
    def adjust_steer(steer_value):
        if steer_value == SteeringFlags.STRAIGHT:
            Controller._steer.set_angle(90)
            Controller.set_forward(True, True)
            Controller.set_speed(left_speed=Controller._MAX_SPEED,
                                 right_speed=Controller._MAX_SPEED)

        elif steer_value == SteeringFlags.SLOW_RIGHT:
            Controller._steer.set_angle(100)
            Controller.set_forward(True, True)
            Controller.set_speed(left_speed=Controller._MAX_SPEED,
                                 right_speed=Controller._MIN_SPEED)

        elif steer_value == SteeringFlags.FAST_RIGHT:
            Controller._steer.set_angle(Controller._MAX_STEER)
            Controller.set_forward(True, False)
            Controller.set_speed(left_speed=Controller._MAX_SPEED,
                                 right_speed=Controller._MIN_SPEED)

        elif steer_value == SteeringFlags.SLOW_LEFT:
            Controller._steer.set_angle(80)
            Controller.set_forward(True, True)
            Controller.set_speed(left_speed=Controller._MIN_SPEED,
                                 right_speed=Controller._MAX_SPEED)

        elif steer_value == SteeringFlags.FAST_LEFT:
            Controller._steer.set_angle(Controller._MIN_STEER)
            Controller.set_forward(False, True)
            Controller.set_speed(left_speed=Controller._MAX_SPEED,
                                 right_speed=Controller._MIN_SPEED)

        elif steer_value == SteeringFlags.REVERSE:
            Controller._steer.set_angle(90)
            Controller.set_forward(False, False)
            Controller.set_speed(left_speed=Controller._MIN_SPEED,
                                 right_speed=Controller._MIN_SPEED)
        else:
            print("Invalid steering value")

    @staticmethod
    def stop():
        Controller._left_motor.stop()
        Controller._right_motor.stop()

    @staticmethod
    def set_speed(left_speed, right_speed):
        Controller._left_motor.set_speed(left_speed)
        Controller._right_motor.set_speed(right_speed)

    @staticmethod
    def set_forward(left_motor: bool = True, right_motor: bool = True):
        """
        in this method we can set the direction of the motors
        True means forward and False means backward
        :param left_motor: left motor direction
        :param right_motor: right motor direction
        :return:
        """
        if left_motor:
            Controller._left_motor.forward()
        else:
            Controller._left_motor.backward()
        if right_motor:
            Controller._right_motor.forward()
        else:
            Controller._right_motor.backward()

    @staticmethod
    def cleanup():
        Controller._steer.set_angle(90)
        Controller.stop()
        Controller._steer.cleanup()
        Controller._left_motor.cleanup()
        Controller._right_motor.cleanup()
        io_interface.cleanup()
