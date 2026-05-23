from dataclasses import dataclass

from game.domain.factory.skill_factory import create_skill
from game.domain.models.character import Character
from game.domain.models.job import Job


@dataclass
class Player(Character):
    job: Job
    level: int = 1
    exp: int = 0
    next_exp: int = 10
        

    def apply_exp(self, gained_exp: int):
        level_ups = 0
        self.exp += gained_exp
        while self.exp >= self.next_exp:
            self.exp -= self.next_exp
            self.level += 1
            level_ups += 1

            self.stats = self.job.grow(self.stats)
        self.job.unlock_skills(self)
        return level_ups


