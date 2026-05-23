from dataclasses import dataclass

from game.domain.effect.delayed_damage_effect import DelayedDamageEffect
from game.domain.effect.stun_effect import StunEffect
from game.domain.models.target_type import TargetType
from game.domain.skills.skill import Skill
from game.skill_util import calculate_study_time_ma
from game.domain.models.damage_calculator import DamageCalculator


@dataclass
class KnowledgeEruption(Skill):
    name: str = "知識の噴火"
    mp_cost: int = 30
    duration: int = 3
    target_type: TargetType = TargetType.ENEMY_SINGLE

    def apply(self, actor, target, battle):
        study_time_ma = calculate_study_time_ma()
        print("study_time_ma", study_time_ma)
        damage = actor.stats.magic_atk * 4.5 + study_time_ma * 5
        
        battle.log.append(f"{actor.name}は膨大な知識を魔力に圧縮し始めた！")
        
        # 自身に行動不能を付与 (3ターン)
        stun = StunEffect(name="精神集中", duration=self.duration)
        actor.add_effect(stun)
        
        dmg = DamageCalculator.magical(actor, target, base_damage=damage)
        # 敵に時限ダメージを付与
        delayed_dmg = DelayedDamageEffect(
            name="知識の噴火(予兆)", 
            duration=self.duration,
            damage=dmg
        )
        
        target.add_effect(delayed_dmg)
