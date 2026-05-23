from dataclasses import dataclass

from game.domain.effect.effect import Effect


@dataclass
class DotEffect(Effect):
    damage: int

    def on_turn_start(self, target, battle):
        target.take_damage(self.damage)
        battle.log.append(
            f"{target.name}は{self.name}で{self.damage}のダメージ！"
        )
