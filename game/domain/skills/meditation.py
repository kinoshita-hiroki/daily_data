from dataclasses import dataclass

from game.domain.effect.buff_effect import StatBuffEffect
from game.domain.models.damage_calculator import DamageCalculator
from game.domain.models.target_type import TargetType
from game.domain.skills.skill import Skill
from game.skill_util import calculate_meditation_total_time


@dataclass
class Meditation(Skill):
    name: str = "瞑想の波動"
    target_type: TargetType = TargetType.ENEMY_SINGLE
    buff_duration: int = 5
    # Meditation shouldn't cost MP to use since it recovers MP.
    # We will override mp_cost directly in initialization if needed,
    # or just assume it is 0.

    def apply(self, actor, target, battle):
        meditation_time = calculate_meditation_total_time()

        # 瞑想時間に応じてMP回復量とデバフ量、ダメージ量を決定
        base_recover = 10
        bonus_recover = min(meditation_time // 10, 50) # 最大50ボーナス
        mp_recover = base_recover + bonus_recover

        # 魔法防御力デバフ (最大40)
        debuff_amount = 10 + min(meditation_time // 20, 30)

        # ダメージ計算: actorの魔法攻撃力と瞑想時間に依存
        base_dmg = (actor.stats.magic_atk * 1.5) + (meditation_time / 2)
        dmg = DamageCalculator.magical(actor, target, base_damage=base_dmg)

        # 1. 自身のMP回復
        actor.get_mp_heal(mp_recover)

        battle.log.append(f"{actor.name}は深く瞑想し、精神を統一した！")
        battle.log.append(f"{actor.name}のMPが {mp_recover} 回復した！")

        # 2. 敵にダメージ
        target.take_damage(dmg)
        battle.log.append(f"{target.name}に {int(dmg)} の魔法ダメージ！")

        # 3. 敵のデバフ効果の適用 (magic_resistance を下げる)
        # Note: 物理的に現時点のステータスから引く
        target.stats.magic_resistance -= debuff_amount
        battle.log.append(f"{target.name}の魔法防御力が下がった！")

        # 効果を追加（amountをマイナスにすることでon_remove時に加算して元に戻す）
        effect = StatBuffEffect(
            name="精神統一",
            duration=self.buff_duration,
            stat_name="magic_resistance",
            amount=-debuff_amount
        )
        target.add_effect(effect)
