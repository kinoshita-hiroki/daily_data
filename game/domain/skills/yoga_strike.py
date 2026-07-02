from dataclasses import dataclass

from game.domain.models.damage_calculator import DamageCalculator
from game.domain.skills.skill import Skill
from game.domain.skills.skill_util import calculate_yoga_total_time


@dataclass
class YogaStrike(Skill):
    def apply(self, actor, target, battle):
        yoga_time = calculate_yoga_total_time()

        # 式: (攻撃力 * 1.5) + (ヨガの合計時間 * 1)
        # Yoga時間が増えるほど固定ダメージが増加していくイメージ
        base_dmg = (actor.stats.atk * 1.7) + (yoga_time / 2)

        dmg = DamageCalculator.physical(actor, target, base_damage=base_dmg)
        target.take_damage(dmg)

        battle.log.append(f"{actor.name}は精神を統一し、ヨガストライクを放った！(HP -{self.hp_cost})")
        battle.log.append(f"{target.name}に {int(dmg)} のダメージ！")
