from enum import Enum, auto


class TargetType(Enum):
    ENEMY_SINGLE = auto()
    ALLY_SINGLE = auto()
    SELF = auto()
    ENEMY_ALL = auto()
    ALLY_ALL = auto()
    ALLY_RANDOM = auto()
    
    def requires_target(self):
        if self in [self.ENEMY_SINGLE , self.ALLY_SINGLE] :
            return True

 