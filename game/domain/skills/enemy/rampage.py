import random

from game.domain.models.damage_calculator import DamageCalculator
from game.domain.skills.skill import Skill


class Rampage(Skill):
    def use(self, actor, targets, battle):
        if not self.check_cost(actor, battle):
            return

        self.pay_cost(actor)

        # targets は list で統一

        for i in range(3):
            target = random.choice(targets)
            self.apply(actor, target, battle)
    def apply(self, actor, target, battle):
        target = target

        dmg = DamageCalculator.physical(actor, target, base_damage=actor.stats.atk * 0.7)
        target.take_damage(dmg)

        battle.log.append(
            f"{actor.name}の攻撃！ {target.name}に {int(dmg)} ダメージ"
        )
