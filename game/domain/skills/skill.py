from __future__ import annotations
from abc import ABC, abstractmethod
from dataclasses import dataclass
from typing import Optional, List, TYPE_CHECKING

from game.domain.models.target_type import TargetType

if TYPE_CHECKING:
    from game.domain.models.character import Character


@dataclass
class Skill(ABC):
    name: str
    mp_cost: int = 0
    hp_cost: int = 0
    target_type: TargetType = TargetType.OPPONENT_SINGLE

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

    def candidate_targets(self, actor, battle):
        match self.target_type:
            case TargetType.OPPONENT_SINGLE:
                enemies = battle.opponents_of(actor)
                return enemies
            case TargetType.OPPONENT_ALL:
                enemies = battle.opponents_of(actor)
                return enemies
            case TargetType.ALLY_SINGLE:
                players = battle.allies_of(actor)
                return players
            case TargetType.ALLY_ALL:
                players = battle.allies_of(actor)
                return players
            case TargetType.SELF:
                return [actor]
            case _:
                raise ValueError(f"Unknown target_type: {self.target_type}")


    def resolve_targets(self, battle, target: Optional[Character] = None, actor: Optional[Character] = None) -> List[Character]:
        """
        必ず list を返す
        """
        if self.target_type.requires_target():
            if target is None:
                return []
            return [target]

        if actor is None:
            return []
        return self.candidate_targets(actor, battle)

    @abstractmethod
    def apply(self, actor, target, battle):
        pass
