
from game.domain.skills.skill import Skill


class Heal(Skill):
    def apply(self, actor, target, battle):
        base = actor.stats.magic_atk
        decrease =  (actor.stats.max_hp - actor.stats.hp) * 0.2
        heal = base + decrease
        target.get_heal(heal)
        battle.log.append(
            f"{actor.name}のヒール！ {target.name}は {int(heal)} 回復"
        )
