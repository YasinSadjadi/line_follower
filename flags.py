from enum import Enum


class SteeringFlags(Enum):
    STRAIGHT = 0
    SLOW_RIGHT = 1
    FAST_RIGHT = 2
    SLOW_LEFT = -1
    FAST_LEFT = -2
    REVERSE = 5


class States(Enum):
    IDLE = 0
    LINE_FOLLOWING = 1
    GETTING_BACK = 2
