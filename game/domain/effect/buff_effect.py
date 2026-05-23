from dataclasses import dataclass

from game.domain.effect.effect import Effect


@dataclass
class StatBuffEffect(Effect):
    stat_name: str
    amount: int

    def on_turn_start(self, target, battle):
        pass

    def on_remove(self, target, battle):
        current_val = getattr(target.stats, self.stat_name)
        setattr(target.stats, self.stat_name, current_val - self.amount)
        battle.log.append(f"{target.name}の{self.name}効果が切れた")
