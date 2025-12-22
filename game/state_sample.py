

# game/state.py
SKILLS = {
    "attack": {
        "name": "たたかう",
        "mp": 0,
        "target": "enemy",
        "effect": "attack",
    },
    "strong_attack": {
        "name": "強打",
        "mp": 5,
        "target": "enemy",
        "effect": "strong_attack",
    },
    "heal": {
        "name": "ヒール",
        "mp": 6,
        "target": "ally",
        "effect": "heal",
    },
    "fireball": {
        "name": "ファイア",
        "mp": 8,
        "target": "enemy",
        "effect": "fireball",
    },
}

def create_battle_state():
    return {
        "party": [
            {
                "name": "勇者",
                "hp": 50,
                "max_hp": 50,
                "mp": 10,
                "max_mp": 10,
                "attack": 10,
                "skills": ["attack", "strong_attack"],
            },
            {
                "name": "戦士",
                "hp": 60,
                "max_hp": 60,
                "mp": 5,
                "max_mp": 5,
                "attack": 12,
                "skills": ["attack"],
            },
            {
                "name": "魔法使い",
                "hp": 35,
                "max_hp": 35,
                "mp": 20,
                "max_mp": 20,
                "attack": 6,
                "skills": ["attack", "fireball"],
            },
            {
                "name": "僧侶",
                "hp": 40,
                "max_hp": 40,
                "mp": 18,
                "max_mp": 18,
                "attack": 5,
                "skills": ["attack", "heal"],
            },
        ],
        "enemy": {
            "name": "ボス",
            "hp": 200,
            "max_hp": 200,
            "attack": 10,
            "skills": ["attack"],
        },

        "turn": 0,
        "log": [],
        "finished": False,
    }
