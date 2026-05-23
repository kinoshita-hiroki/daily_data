# domain/factory/player_factory.py
import imp

from game.domain.factory.job_factory import create_job
from game.domain.factory.skill_factory import create_skills
from game.domain.models.player import Player
from game.domain.models.stats import Stats


def create_player(job_name:str) -> Player:
    job = create_job(job_name)
    stats = Stats(
        **job.base_stats,
    )
    skills = create_skills(job.default_skills)
    return Player(
        name=job.name,
        job=job,
        level=1,
        exp=0,
        stats=stats,
        skills=skills,
        effects=[]
    )
