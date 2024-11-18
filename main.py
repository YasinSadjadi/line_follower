from robot import Robot
import argparse


def main():
    parser = argparse.ArgumentParser(description='Parser for different test modes')
    parser.add_argument("--test", "-t", action="store_true", help="Execute Testing")

    args = parser.parse_args()
    robot = Robot()
    if args.test:
        # robot.test()
        pass
    else:
        try:
            robot.run()
        except KeyboardInterrupt:
            print("KeyboardInterrupt")
            robot.cleanup()
        finally:
            robot.cleanup()
