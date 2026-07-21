# domain/factory/player_factory.py
from game.domain.factory.skill_factory import create_skills
from game.domain.models.enemy import Enemy
from game.domain.models.stats import Stats

ENEMY_DEFINITIONS = {
    "タイラント": {
        "base_stats": {"hp": 500, "max_hp": 500, "atk": 40, "defense":40, "magic_atk":40, "magic_resistance": 40},
        "skills": ["攻撃", "ランページ"]
    },
    "ハートレス": {
        "base_stats": {"hp": 2000, "max_hp": 2000, "atk": 60, "defense":70, "magic_atk":85, "magic_resistance": 70},
        "skills": ["攻撃", "ランページ", "ポイズンアタック"]
    },
    "怨霊": {
        "base_stats": {"hp": 5000, "max_hp": 5000, "atk": 80, "defense":80, "magic_atk":100, "magic_resistance": 80},
        "skills": ["攻撃", "呪い", "復讐"]
    }
}

def create_enemy(name: str) -> Enemy:
    stats = Stats(**ENEMY_DEFINITIONS[name]["base_stats"])
    skills = create_skills(ENEMY_DEFINITIONS[name]["skills"])
    return Enemy(
        name=name,
        stats=stats,
        skills=skills,
        effects=[]
    )
