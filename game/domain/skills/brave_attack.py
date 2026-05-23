from dataclasses import dataclass

from game.domain.effect.buff_effect import StatBuffEffect
from game.domain.models.damage_calculator import DamageCalculator
from game.domain.models.target_type import TargetType
from game.domain.skills.skill import Skill
from game.skill_util import calculate_task_sum


@dataclass
class BraveAttack(Skill):
    name: str = "勇者の切り込み"
    duration: int = 3

    def apply(self, actor, target, battle):
        # バフ量計算
        buff_amount = calculate_task_sum() // 20
        
        # 1. 敵単体への攻撃
        dmg = DamageCalculator.physical(actor, target, base_damage=actor.stats.atk * 1.5)
        target.take_damage(dmg)
        battle.log.append(f"{actor.name}の勇者の号令！ {target.name}に {int(dmg)} のダメージ！")

        # 2. 味方全員へのバフ (攻撃力 & 魔法攻撃力)
        battle.log.append(f"{actor.name}の号令で味方の士気が上がった！ (上昇量: {buff_amount})")
        for player in battle.alive_players():
            # Apply Atk Buff
            player.stats.atk += buff_amount
            atk_effect = StatBuffEffect(
                name="攻撃上昇(勇者の切込み)",
                duration=self.duration,
                stat_name="atk",
                amount=buff_amount
            )
            player.add_effect(atk_effect)

            # Apply Magic Atk Buff
            player.stats.magic_atk += buff_amount
            matk_effect = StatBuffEffect(
                name="魔力上昇(勇者の切り込み)",
                duration=self.duration,
                stat_name="magic_atk",
                amount=buff_amount
            )
            player.add_effect(matk_effect)

            battle.log.append(f"{player.name}の能力が上がった！")
