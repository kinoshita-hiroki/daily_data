from dataclasses import dataclass

from game.domain.effect.buff_effect import StatBuffEffect
from game.domain.models.target_type import TargetType
from game.domain.skills.skill import Skill
from game.skill_util import calculate_workout_done_sum


@dataclass
class PhysicalBuff(Skill):
    name: str = "身体強化"
    target_type: TargetType = TargetType.SELF
    duration: int = 3

    def apply(self, actor, target, battle):
        buff_amount = calculate_workout_done_sum(actor.job) // 10

        battle.log.append(f"{actor.name}はこれまでの鍛錬を力に変えた！ (上昇量: {buff_amount})")

        if buff_amount > 0:
            # 攻撃力アップ
            target.stats.atk += buff_amount
            target.add_effect(StatBuffEffect(
                name="身体強化(攻)",
                duration=self.duration,
                stat_name="atk",
                amount=buff_amount
            ))

            # 防御力アップ
            target.stats.defense += buff_amount
            target.add_effect(StatBuffEffect(
                name="身体強化(防)",
                duration=self.duration,
                stat_name="defense",
                amount=buff_amount
            ))

            # 魔法防御力アップ
            target.stats.magic_resistance += buff_amount
            target.add_effect(StatBuffEffect(
                name="身体強化(魔防)",
                duration=self.duration,
                stat_name="magic_resistance",
                amount=buff_amount
            ))

            battle.log.append(f"{target.name}の攻撃力と防御力、魔法防御力が {buff_amount} 上がった！")
        else:
            battle.log.append("まだ十分な鍛錬を積んでいないようだ...")
