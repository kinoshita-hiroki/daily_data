
import random
from dataclasses import dataclass

from game.domain.models.character import Character
from game.domain.models.command import Command


@dataclass
class Enemy(Character):
    ai_type: str = "random"
    def choose_skill(self):
        # とりあえずランダム
        skill = random.choice(list(self.skills.values()))
        return skill

    def choose_target(self, skill, battle):
        targets = skill.candidate_targets(self,battle)
        return random.choice(targets)

    def decide_command(self, battle) -> Command:
        skill = self.choose_skill()
        if skill.target_type.requires_target():
            target = self.choose_target(skill, battle)
        else:
            target = None
        return Command(
            actor=self,
            target=target,
            skill=skill,
        )

