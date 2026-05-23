from dataclasses import dataclass

from game.domain.effect.buff_effect import StatBuffEffect
from game.domain.models.target_type import TargetType
from game.domain.skills.skill import Skill


@dataclass
class Concentrate(Skill):
    name: str = "Concentrate"
    target_type: TargetType = TargetType.ALLY_SINGLE
    buff_amount: int = 30
    duration: int = 3

    def apply(self, actor, target, battle):
        battle.log.append(f"{actor.name}は体力を削って精神を統一した！(HP -{self.hp_cost})")

        # Apply Buff
        target.stats.magic_atk += self.buff_amount
        battle.log.append(f"{target.name}の魔法攻撃力が上がった！")

        # Add Buff Effect (for tracking duration and removal)
        effect = StatBuffEffect(
            name="集中",
            duration=self.duration,
            stat_name="magic_atk",
            amount=self.buff_amount
        )
        target.add_effect(effect)
