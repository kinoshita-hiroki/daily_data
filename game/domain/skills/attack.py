
from game.domain.models.damage_calculator import DamageCalculator
from game.domain.skills.skill import Skill


class Attack(Skill):
    def apply(self, actor, target, battle):
        target = target

        dmg = DamageCalculator.physical(actor, target, base_damage=actor.stats.atk)
        target.take_damage(dmg)

        battle.log.append(
            f"{actor.name}の攻撃！ {target.name}に {int(dmg)} ダメージ"
        )
