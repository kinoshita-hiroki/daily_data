from abc import ABC, abstractmethod
from dataclasses import dataclass

from game.domain.models.target_type import TargetType


@dataclass
class Skill(ABC):
    name: str
    mp_cost: int = 0
    hp_cost: int = 0
    target_type: TargetType = TargetType.ENEMY_SINGLE

    def check_cost(self, actor, battle) -> bool:
        if actor.stats.mp < self.mp_cost:
            battle.log.append(f"{actor.name}はMPが足りない!")
            return False
        if actor.stats.hp <= self.hp_cost:
             battle.log.append(f"{actor.name}は体力が足りない！")
             return False
        return True

    def pay_cost(self, actor):
        actor.stats.mp -= self.mp_cost
        actor.stats.hp -= self.hp_cost

    def use(self, actor, targets, battle):
        if not self.check_cost(actor, battle):
            return

        self.pay_cost(actor)

        # targets は list で統一
        for target in targets:
            if target.is_alive():
                self.apply(actor, target, battle)

    @abstractmethod
    def apply(self, actor, target, battle):
        pass
