from dataclasses import dataclass
from game.domain.effect.effect import Effect

@dataclass
class DelayedDamageEffect(Effect):
    damage: float = 0.0

    def on_turn_start(self, target, battle):
        battle.log.append(f"{target.name}の周囲の魔力が渦巻いている… (残り {self.duration} ターン)")

    def on_remove(self, target, battle):
        target.take_damage(self.damage)
        battle.log.append(f"💥 知識が噴火した！ {target.name}に {int(self.damage)} のダメージ！")
