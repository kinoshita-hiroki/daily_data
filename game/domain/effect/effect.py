from abc import ABC, abstractmethod
from dataclasses import dataclass


@dataclass
class Effect(ABC):
    name: str
    duration: int  # 残りターン数

    @abstractmethod
    def on_turn_start(self, target, battle):
        pass

    def on_remove(self, target, battle):
        pass

    def tick(self):
        self.duration -= 1

    def is_expired(self):
        return self.duration <= 0
