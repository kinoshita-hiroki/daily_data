from dataclasses import dataclass


@dataclass
class Stats:
    hp: float = 0.0
    max_hp: float = 0.0
    mp: float = 0.0
    max_mp: float = 0.0
    atk: float = 0.0
    defense: float = 0.0
    magic_atk: float = 0.0
    magic_resistance: float = 0.0
