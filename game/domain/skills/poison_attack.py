
from game.domain.effect.dot_effect import DotEffect
from game.domain.models.damage_calculator import DamageCalculator
from game.domain.skills.skill import Skill


class PoisonAttack(Skill):
    def apply(self, actor, target, battle):
        dmg = DamageCalculator.magical(actor, target, base_damage=actor.stats.magic_atk)
        target.take_damage(dmg)
        dot = actor.stats.atk / 3

        poison = DotEffect(
            name="毒",
            duration=4,
            damage=dot
        )
        target.add_effect(poison)
        battle.log.append(
            f"{actor.name}のポイズンアタック！ {target.name}に {int(dmg)} ダメージ！"
        )
        battle.log.append(f"{target.name}は毒状態になった！")
