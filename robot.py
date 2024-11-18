from controller import Controller
from io_interface import IR
from flags import SteeringFlags as Flags
from flags import States
import time


class Robot:
    def __init__(self):
        self._frequency = 100
        self._right_ir = IR(1)
        self._left_ir = IR(2)
        self._mid_ir = IR(3)
        self._state = States.IDLE

    def _transition(self, state):
        self._state = state

    def _machine(self):
        while True:
            if self._state == States.LINE_FOLLOWING:
                self._line_following()
            elif self._state == States.IDLE:
                self._idle()
            elif self._state == States.GETTING_BACK:
                self._getting_back()
            else:
                print("Invalid state")
                self._idle()

    def run(self):
        self._transition(States.LINE_FOLLOWING)
        self._machine()

    def _idle(self):
        Controller.stop()
        # TODO: Implement idle behavior here

    def _getting_back(self):
        while True:
            start_time = time.time()
            right_value = self._right_ir.get_value()
            left_value = self._left_ir.get_value()
            mid_value = self._mid_ir.get_value()
            if right_value or mid_value or left_value:
                Controller.stop()
                self._transition(States.LINE_FOLLOWING)
                break
            else:
                Controller.adjust_steer(Flags.REVERSE)

            end_time = time.time()
            elapsed_time = end_time - start_time
            if elapsed_time < 1 / self._frequency:
                time.sleep(1 / self._frequency - elapsed_time)

    def _line_following(self):
        # Implement line following algorithm here
        pre_state = Flags.STRAIGHT
        no_result_counter = 0
        while True:
            start_time = time.time()

            right_value = self._right_ir.get_value()
            left_value = self._left_ir.get_value()
            mid_value = self._mid_ir.get_value()

            # Implement line following algorithm here
            if left_value and not right_value and not mid_value:
                Controller.adjust_steer(Flags.SLOW_LEFT)
                pre_state = Flags.SLOW_LEFT

            elif right_value and not left_value and not mid_value:
                Controller.adjust_steer(Flags.SLOW_RIGHT)
                pre_state = Flags.SLOW_RIGHT

            elif mid_value and not right_value and not left_value:
                Controller.adjust_steer(Flags.STRAIGHT)
                pre_state = Flags.STRAIGHT

            elif left_value and mid_value and not right_value:
                Controller.adjust_steer(Flags.SLOW_LEFT)
                pre_state = Flags.SLOW_LEFT

            elif right_value and mid_value and not left_value:
                Controller.adjust_steer(Flags.SLOW_RIGHT)
                pre_state = Flags.SLOW_RIGHT

            else:
                Controller.adjust_steer(pre_state)
                no_result_counter += 1
                if no_result_counter > 10:
                    self._transition(States.GETTING_BACK)
                    break
            end_time = time.time()
            elapsed_time = end_time - start_time
            if elapsed_time < 1 / self._frequency:
                time.sleep(1 / self._frequency - elapsed_time)

    @staticmethod
    def cleanup():
        Controller.cleanup()

    @staticmethod
    def test_hardware():
        print("servo set to 90")
        Controller.set_steer_angle(90)
        time.sleep(1)

        print("servo set to 60")
        Controller.set_steer_angle(60)
        time.sleep(1)

        print("servo set to 120")
        Controller.set_steer_angle(120)
        time.sleep(1)

        print("servo set to 90")
        Controller.set_steer_angle(90)
        print("left motor set to +100")
        Controller.set_speed(100, 0)
        time.sleep(1)
        print("left motor set to -100")
        Controller.set_speed(-100, 0)
        time.sleep(1)
        print("left motor set to 0")
        Controller.set_speed(0, 0)
        time.sleep(1)

        print("right motor set to +100")
        Controller.set_speed(0, 100)
        time.sleep(1)
        print("right motor set to -100")
        Controller.set_speed(0, -100)
        time.sleep(1)
        print("right motor set to 0")
        Controller.set_speed(0, 0)
        time.sleep(1)

        print("done!!!")
        Robot.cleanup()
