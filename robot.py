from controller import Controller
from io_interface import IR
from flags import SteeringFlags as Flags
from flags import States


class Robot:
    def __init__(self):

        self.right_ir = IR(1)
        self.left_ir = IR(2)
        self.mid_ir = IR(3)
        self.state = States.IDLE

    def transition(self, state):
        self.state = state

    def machine(self):
        while True:
            if self.state == States.LINE_FOLLOWING:
                self.line_following()
            elif self.state == States.IDLE:
                self.idle()
            elif self.state == States.GETTING_BACK:
                self.getting_back()
            else:
                print("Invalid state")
                self.idle()

    def run(self):
        self.transition(States.LINE_FOLLOWING)

    def idle(self):
        Controller.stop()
        # TODO: Implement idle behavior here

    def getting_back(self):
        while True:
            right_value = self.right_ir.get_value()
            left_value = self.left_ir.get_value()
            mid_value = self.mid_ir.get_value()
            if right_value or mid_value or left_value:
                Controller.stop()
                self.transition(States.LINE_FOLLOWING)
                break
            else:
                Controller.adjust_steer(Flags.REVERSE)

    def line_following(self):
        # Implement line following algorithm here
        pre_state = Flags.STRAIGHT
        no_result_counter = 0
        while True:
            right_value = self.right_ir.get_value()
            left_value = self.left_ir.get_value()
            mid_value = self.mid_ir.get_value()

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
                    self.transition(States.GETTING_BACK)
                    break

    @staticmethod
    def cleanup():
        Controller.cleanup()
