from dataclasses import dataclass

from game.domain.factory.skill_factory import create_skill
from game.domain.skills.skill import Skill


@dataclass(frozen=True)
class Job:
    name: str
    default_skills:[]
    learnable_skills: dict[int, list[type[Skill]]]
    base_stats: dict[str, float]
    grow_stats: dict[str, float]

    def unlock_skills(self, character):
        for k, v in self.learnable_skills.items():
            if character.level >= k:
                for skill in v:
                    if skill not in character.skills.keys():
                        character.skills[skill] = create_skill(skill)

    def grow(self, stats):
        for k, v in self.grow_stats.items():
            if not hasattr(stats, k):
                raise ValueError(f"Stats に '{k}' は存在しません")
            setattr(stats, k, getattr(stats, k) + v)
        return stats
