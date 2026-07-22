from game.domain.effect.curse_effect import CurseEffect
from game.domain.models.damage_calculator import DamageCalculator
from game.domain.skills.skill import Skill


class Vengeance(Skill):

    def apply(self, actor, target, battle):
        # 審判状態かチェック
        curse_effect = next((e for e in target.effects if isinstance(e, CurseEffect)), None)


        if curse_effect:
            # 審判状態なら大ダメージ
            dmg = DamageCalculator.magical(actor, target, base_damage=actor.stats.magic_atk * 1.3)
            battle.log.append(f"{target.name}への復讐！")
            target.take_damage(dmg)
            battle.log.append(f"{target.name}に {int(dmg)} の痛恨のダメージ！")

            # 審判状態を解除
            target.effects.remove(curse_effect)
            battle.log.append(f"{target.name}の呪い状態が解除された")
        else:
            # 通常ダメージ
            dmg = DamageCalculator.magical(actor, target, base_damage=actor.stats.magic_atk * 0.8)
            target.take_damage(dmg)
            battle.log.append(f"{actor.name}の復讐！ {target.name}に {int(dmg)} ダメージ")
