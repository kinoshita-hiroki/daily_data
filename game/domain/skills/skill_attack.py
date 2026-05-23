from dataclasses import dataclass

from game.domain.models.damage_calculator import DamageCalculator
from game.domain.skills.skill import Skill
from game.skill_util import calculate_human_skill_last_value


@dataclass
class SkillAttack(Skill):

    def apply(self, actor, target, battle):
        human_skill = calculate_human_skill_last_value()

        # 式: (攻撃力 * 1.5) + (人間力 * 3)
        base_dmg = (actor.stats.atk * 1.5) + (human_skill * 3)

        dmg = DamageCalculator.physical(actor, target, base_damage=base_dmg)
        target.take_damage(dmg)

        battle.log.append(f"{actor.name}は体力を削り、スキルアタックを放った！(HP -{self.hp_cost})")
        battle.log.append(f"{target.name}に {int(dmg)} のダメージ！")
