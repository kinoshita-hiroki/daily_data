from dataclasses import dataclass

from game.domain.effect.effect import Effect
from game.domain.models.damage_calculator import DamageCalculator
from game.domain.models.stats import Stats
from game.domain.skills.skill import Skill


@dataclass
class Character:
    name: str
    stats: Stats
    skills: dict[str, Skill]
    effects: list[Effect]


    def add_effect(self, effect: Effect):
        self.effects.append(effect)

    def can_act(self) -> bool:
        from game.domain.effect.stun_effect import StunEffect
        return not any(isinstance(e, StunEffect) for e in self.effects)

    def get_skill(self, skill_key):
        return self.skills[skill_key]

    def is_alive(self) -> bool:
        return self.stats.hp > 0

    def take_damage(self, dmg: float):
        self.stats.hp = max(0.0, self.stats.hp - dmg)

    def get_heal(self, amount: float):
        self.stats.hp = min(self.stats.max_hp, self.stats.hp + amount)

    def get_mp_heal(self, amount: float):
        self.stats.mp = min(self.stats.max_mp, self.stats.mp + amount)

    def take_physical_damage(self, attacker, base_damage):
        dmg = DamageCalculator.physical(attacker, self, base_damage=base_damage)
        self.take_damage(dmg)
        return dmg

    def take_magical_damage(self, attacker, base_damage):
        dmg = DamageCalculator.magical(attacker, self, base_damage=base_damage)
        self.take_damage(dmg)
        return dmg
