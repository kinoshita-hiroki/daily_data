from enum import Enum, auto


class TargetType(Enum):
    OPPONENT_SINGLE = auto()
    ALLY_SINGLE = auto()
    SELF = auto()
    OPPONENT_ALL = auto()
    ALLY_ALL = auto()
    ALLY_RANDOM = auto()


    def requires_target(self):
        if self in [self.OPPONENT_SINGLE , self.ALLY_SINGLE] :
            return True

