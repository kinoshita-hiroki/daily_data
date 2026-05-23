import random

from game.domain.models.damage_calculator import DamageCalculator
from game.domain.skills.skill import Skill


class Spear(Skill):
    def apply(self, actor, target, battle):
        decrease = (actor.stats.max_hp - actor.stats.hp) * 0.5
        dmg = DamageCalculator.physical(actor, target, base_damage=actor.stats.atk * 1.5 + decrease)
        target.take_damage(dmg)

        battle.log.append(
            f"{actor.name}のspear! {target.name}に {int(dmg)} ダメージ"
        )
