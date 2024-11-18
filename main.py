from robot import Robot
import argparse


def main():
    parser = argparse.ArgumentParser(description='Parser for different test modes')
    parser.add_argument("--test", "-t", action="store_true", help="Execute Testing")

    args = parser.parse_args()
    robot = Robot()
    if args.test:
        try:
            print("Testing Hardware...")
            Robot.test_hardware()
        except KeyboardInterrupt:
            print("KeyboardInterrupt")
        finally:
            robot.cleanup()
    else:
        try:
            print("Running Robot...")
            robot.run()
        except KeyboardInterrupt:
            print("KeyboardInterrupt")
        finally:
            robot.cleanup()
