# domain/factory/player_factory.py
from game.domain.models.job import Job


def create_job(job: str) -> Job:
    if job == "勇者":
        return Job(
            name="勇者",
            default_skills=["攻撃"],
            learnable_skills={3: ["スピア"], 12: ["勇者の切り込み"], 15:["スキルアタック"]},
            base_stats = {"hp": 50, "max_hp": 50, "mp": 10, "max_mp": 10, "atk": 10, "defense": 10, "magic_atk":10, "magic_resistance":10},
            grow_stats = {"hp": 9, "max_hp": 9, "mp": 4, "max_mp": 4,"atk": 4, "defense": 4, "magic_atk":3.5, "magic_resistance":3.5}
        )
    elif job == "戦士":
        return Job(
            name="戦士",
            default_skills=["攻撃"],
            learnable_skills={2: ["強打"], 13:["身体強化"], 16:["ヨガストライク"]},
            base_stats={"hp": 60, "max_hp": 60, "mp": 5, "max_mp": 5, "atk": 12, "defense": 12, "magic_atk":8, "magic_resistance":8},
            grow_stats={"hp": 10, "max_hp": 10, "mp": 3.5, "max_mp": 3.5, "atk": 4.5, "defense": 4.5, "magic_atk": 3, "magic_resistance": 3},
        )
    elif job == "魔法使い":
        return Job(
            name="魔法使い",
            default_skills=["攻撃"],
            learnable_skills={2: ["ファイヤーボール"], 10: ["コンセントレイト"], 18:["知識の噴火"]},
            base_stats={"hp": 40, "max_hp": 40, "mp": 20, "max_mp": 20, "atk": 8, "defense": 8, "magic_atk":12, "magic_resistance":12},
            grow_stats={"hp": 7.5, "max_hp":7.5, "mp": 6, "max_mp": 6, "atk": 2, "defense": 3.5, "magic_atk":4.5, "magic_resistance":4},
        )
    elif job == "僧侶":
        return Job(
            name="僧侶",
            default_skills=["攻撃"],
            learnable_skills={3: ["ヒール"], 11: ["エリアヒール"], 17:["瞑想の波動"]},
            base_stats={"hp": 40, "max_hp": 40, "mp": 22, "max_mp": 22, "atk": 8, "defense": 8, "magic_atk":10, "magic_resistance":14},
            grow_stats={"hp": 7.8, "max_hp": 7.8, "mp": 7, "max_mp": 7, "atk": 2, "defense": 3.5, "magic_atk":4, "magic_resistance":5},
        )