from dataclasses import dataclass
from typing import Optional

from game.domain.models.character import Character
from game.domain.skills.skill import Skill


@dataclass(frozen=True)
class Command:
    actor: Character
    target: Optional[Character] = None
    skill: Optional[Skill] = None

