# game/battle.py
import random

from game.state import SKILLS


def alive_members(party):
    return [m for m in party if m["hp"] > 0]


def next_turn(battle):
    battle["turn"] += 1
    if battle["turn"] >= len(battle["party"]):
        enemy_turn(battle)
        battle["turn"] = 0

def check_battle_end(battle):
    if battle["enemy"]["hp"] <= 0:
        battle["log"].append("🎉 勝利！")
        battle["finished"] = True

def enemy_turn(battle):
    enemy = battle["enemy"]
    targets = alive_members(battle["party"])
    if not targets:
        battle["finished"] = True
        battle["log"].append("💀 全滅…")
        return

    skill = choose_enemy_skill(enemy)
    if (enemy["hp"] / enemy["max_hp"]) < 0.3:
        battle["log"].append(
            f"{enemy['name']}は怒っている！"
        )
        rate = 1.3
    else:
        rate = 1
    if skill == "attack":
        target = random.choice(targets)
        dmg = int((random.randint(int(enemy["attack"] * 0.9), int(enemy["attack"] * 1.1))) * rate)
        target["hp"] -= dmg
        battle["log"].append(
            f"{enemy['name']}の攻撃！ {target['name']}に {dmg} ダメージ"
        )
    if skill == "rampage":
        for i in range(3):
            target = random.choice(targets)
            dmg = int((random.randint(int(enemy["attack"] * 0.9), int(enemy["attack"] * 1.1))) * rate)
            target["hp"] -= dmg
            battle["log"].append(
                f"{enemy['name']}の攻撃！ {target['name']}に {dmg} ダメージ"
            )


# game/battle.py
def use_skill(battle, skill_key, target_idx=None):
    actor = battle["party"][battle["turn"]]
    skill = SKILLS[skill_key]
    print("====================")
    print(skill["effect"])

    # MPチェック
    if actor["mp"] < skill["mp"]:
        battle["log"].append(f"{actor['name']}はMPが足りない!")
        return

    actor["mp"] -= skill["mp"]

    if skill["effect"] == "attack":
        dmg = random.randint(actor["attack"] - 2, actor["attack"] + 2)
        battle["enemy"]["hp"] -= dmg
        battle["log"].append(f"{actor['name']}の攻撃！ {dmg} ダメージ")

    elif skill["effect"] == "power_strike":
        print("====================")
        decrease = int((actor["max_hp"] - actor["hp"]) * 0.5)
        base = actor["attack"] * 1.5
        dmg = random.randint(base - 3, base + 3) + decrease
        battle["enemy"]["hp"] -= dmg
        battle["log"].append(f"{actor['name']}の強打！ {dmg} ダメージ")

    elif skill["effect"] == "heal":
        target = battle["party"][target_idx]
        base = actor["mind"]
        decrease = int((actor["max_hp"] - actor["hp"]) * 0.2)
        heal = random.randint(base , base * 1.1) + decrease
        target["hp"] = min(target["hp"] + heal, target["max_hp"])
        battle["log"].append(
            f"{actor['name']}のヒール！ {target['name']}は {heal} 回復"
        )

    elif skill["effect"] == "fireball":
        base = actor["int"]
        decrease = int((actor["max_hp"] - actor["hp"]) * 0.7)
        dmg = random.randint(base + 5, base + 7) + decrease
        battle["enemy"]["hp"] -= dmg
        battle["log"].append(
            f"{actor['name']}のファイア！ {dmg} ダメージ"
        )
    elif skill["effect"] == "spear":
        base = int(actor["attack"] * 1.5)
        decrease = int((actor["max_hp"] - actor["hp"]) * 0.5)
        dmg = random.randint(base - 3, base + 3) + decrease
        battle["enemy"]["hp"] -= dmg
        battle["log"].append(
            f"{actor['name']}のspear！ {dmg} ダメージ"
        )
    next_turn(battle)



def choose_enemy_skill(enemy):
    skills = enemy["skills"]  # ["power_attack", "all_attack", ...]

    for skill, prob in skills.items():
        if random.random() <  prob:
            return skill

    return "attack"  # 何も発動しなかった（通常攻撃など）
