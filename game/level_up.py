import copy

from game.state import SKILL_UNLOCKS


def apply_weekly_exp(player, job_grouth, gained_exp):
    new_player = copy.deepcopy(player)
    new_player["exp"] += gained_exp

    level_ups = 0

    while new_player["exp"] >= new_player["next_exp"]:
        new_player["exp"] -= new_player["next_exp"]
        new_player["level"] += 1

        for k,v in job_grouth.items():
            new_player[k] += v

        level_ups += 1
    unlock_skills(new_player)
    return new_player, level_ups

def unlock_skills(character):
    unlocked = []

    unlock_table = SKILL_UNLOCKS.get(character["name"], [])

    for entry in unlock_table:
        if (
            character["level"] >= entry["level"]
            and entry["skill"] not in character["skills"]
        ):
            character["skills"].append(entry["skill"])
            unlocked.append(entry["skill"])

    return unlocked
