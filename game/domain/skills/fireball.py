
from game.domain.models.damage_calculator import DamageCalculator
from game.domain.skills.skill import Skill


class Fireball(Skill):
    def apply(self, actor, target, battle):
        decrease = (actor.stats.max_hp - actor.stats.hp) * 0.6
        dmg = DamageCalculator.magical(actor, target, base_damage=actor.stats.magic_atk * 1.5 + decrease)
        target.take_damage(dmg)
        battle.log.append(
            f"{actor.name}のファイア！ {int(dmg)} ダメージ"
        )
