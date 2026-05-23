
from game.domain.skills.skill import Skill


class AreaHeal(Skill):
    def apply(self, actor, target, battle):
        base = actor.stats.magic_atk
        decrease =(target.stats.max_hp - target.stats.hp) * 0.1
        heal = base + decrease
        target.get_heal(heal)
        battle.log.append(
            f"{actor.name}のエリアヒール！ {target.name}は {int(heal)} 回復"
        )
