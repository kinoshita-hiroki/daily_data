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


def enemy_turn(battle):
    enemy = battle["enemy"]
    targets = alive_members(battle["party"])
    if not targets:
        battle["finished"] = True
        battle["log"].append("💀 全滅…")
        return


    target = random.choice(targets)
    if (enemy["hp"] / enemy["max_hp"]) < 0.3:
        battle["log"].append(
            f"{enemy['name']}は怒っている！"
        )
        rate = 1.5
    else:
        rate = 1
    dmg = int((random.randint(enemy["attack"] - 4, enemy["attack"] + 4)) * rate)
    target["hp"] -= dmg
    battle["log"].append(
        f"{enemy['name']}の攻撃！ {target['name']}に {dmg} ダメージ"
    )


def check_battle_end(battle):
    if battle["enemy"]["hp"] <= 0:
        battle["log"].append("🎉 勝利！")
        battle["finished"] = True
# game/battle.py


def use_skill(battle, skill_key, target_idx=None):
    actor = battle["party"][battle["turn"]]
    skill = SKILLS[skill_key]

    # MPチェック
    if actor["mp"] < skill["mp"]:
        battle["log"].append(f"{actor['name']}はMPが足りない！")
        return

    actor["mp"] -= skill["mp"]

    if skill["effect"] == "attack":
        dmg = random.randint(actor["attack"] - 2, actor["attack"] + 2)
        battle["enemy"]["hp"] -= dmg
        battle["log"].append(f"{actor['name']}の攻撃！ {dmg} ダメージ")

    elif skill["effect"] == "strong_attack":
        base = int(actor["attack"] * 1.8)
        dmg = random.randint(base - 3, base + 3)
        battle["enemy"]["hp"] -= dmg
        battle["log"].append(f"{actor['name']}の強打！ {dmg} ダメージ")

    elif skill["effect"] == "heal":
        target = battle["party"][target_idx]
        heal = random.randint(15, 20)
        target["hp"] = min(target["hp"] + heal, target["max_hp"])
        battle["log"].append(
            f"{actor['name']}のヒール！ {target['name']}は {heal} 回復"
        )

    elif skill["effect"] == "fireball":
        dmg = random.randint(18, 25)
        battle["enemy"]["hp"] -= dmg
        battle["log"].append(
            f"{actor['name']}のファイア！ {dmg} ダメージ"
        )

    next_turn(battle)

