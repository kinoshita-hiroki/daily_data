
import random
from dataclasses import dataclass

from typing_extensions import List

from game.domain.models.character import Character
from game.domain.models.command import Command


@dataclass
class Enemy(Character):
    ai_type: str = "random"
    def choose_skill(self):
        # とりあえずランダム
        skill = random.choice(list(self.skills.values()))
        return skill
    
    def decide_command(self) -> Command:
        skill = self.choose_skill()
        return Command(
            actor=self,
            target=None,
            skill=skill,
        )