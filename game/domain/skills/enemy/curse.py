from game.domain.effect.curse_effect import CurseEffect
from game.domain.skills.skill import Skill
from game.skill_util import calculate_condition_avg
import random

class Curse(Skill):
    def apply(self, actor, target, battle):
        if  random.randint(0, 10) > calculate_condition_avg():
            # 審判エフェクトを付与（4ターン持続）
            curse = CurseEffect(
                name="呪い",
                duration=4
            )
            target.add_effect(curse)
            battle.log.append(f"{actor.name}は{target.name}を呪った！")
            battle.log.append(f"{target.name}は呪い状態になった！")
