from dataclasses import dataclass

from game.domain.effect.effect import Effect


@dataclass
class StunEffect(Effect):
    def on_turn_start(self, target, battle):
        battle.log.append(f"{target.name}は集中している…！")
