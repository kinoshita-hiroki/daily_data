from game.domain.models.target_type import TargetType
from game.domain.skills.area_heal import AreaHeal
from game.domain.skills.attack import Attack
from game.domain.skills.brave_attack import BraveAttack
from game.domain.skills.concentrate import Concentrate
from game.domain.skills.enemy.curse import Curse
from game.domain.skills.enemy.enemy_attack import EnemyAttack
from game.domain.skills.enemy.poison_attack import PoisonAttack
from game.domain.skills.enemy.rampage import Rampage
from game.domain.skills.enemy.vengeance import Vengeance
from game.domain.skills.fireball import Fireball
from game.domain.skills.heal import Heal
from game.domain.skills.knowledge_eruption import KnowledgeEruption
from game.domain.skills.meditation import Meditation
from game.domain.skills.physical_buff import PhysicalBuff
from game.domain.skills.power_strike import PowerStrike
from game.domain.skills.skill_attack import SkillAttack
from game.domain.skills.spear import Spear
from game.domain.skills.yoga_strike import YogaStrike

SKILL_REGISTRY = {
    "攻撃": lambda: Attack(
        name="攻撃",
        mp_cost=0,
        target_type=TargetType.ENEMY_SINGLE
    ),
    "身体強化": lambda: PhysicalBuff(
        name="身体強化",
        mp_cost=10,
        target_type=TargetType.SELF
    ),
    "強打": lambda: PowerStrike(
        name="強打", 
        mp_cost=5, 
        target_type=TargetType.ENEMY_SINGLE
    ),
    "スピア": lambda: Spear(
        name="スピア", 
        mp_cost=8, 
        target_type=TargetType.ENEMY_SINGLE
    ),
    "ファイヤーボール": lambda: Fireball(
        name="ファイヤーボール", 
        mp_cost=8, 
        target_type=TargetType.ENEMY_SINGLE
    ),
    "ヒール": lambda: Heal(
        name="ヒール", 
        mp_cost=6, 
        target_type=TargetType.ALLY_SINGLE
    ),
    "エリアヒール": lambda: AreaHeal(
        name="エリアヒール",
        mp_cost=20,
        target_type=TargetType.ALLY_ALL
    ),
    "コンセントレイト": lambda: Concentrate(
        name="コンセントレイト",
        hp_cost=20,
        target_type=TargetType.SELF
    ),
    "勇者の切り込み": lambda: BraveAttack(
        name="勇者の切り込み",
        mp_cost=15,
        target_type=TargetType.ENEMY_SINGLE
    ),
    "スキルアタック": lambda: SkillAttack(
        name="スキルアタック",
        hp_cost=30,
        target_type=TargetType.ENEMY_SINGLE
    ),
    "ランページ": lambda: Rampage(
        name="ランページ",
        mp_cost=0,
        target_type=TargetType.ALLY_ALL
    ),
    "敵攻撃": lambda: EnemyAttack(
        name="敵攻撃",
        mp_cost=0,
        target_type=TargetType.ALLY_SINGLE
    ),
    "ポイズンアタック": lambda: PoisonAttack(
        name="ポイズンアタック",
        mp_cost=0,
        target_type=TargetType.ALLY_SINGLE
    ),
    "呪い": lambda: Curse(
        name="呪い",
        mp_cost=0,
        target_type=TargetType.ALLY_ALL
    ),
    "復讐": lambda: Vengeance(
        name="復讐",
        mp_cost=0,
        target_type=TargetType.ALLY_ALL
    ),
    "知識の噴火": lambda: KnowledgeEruption(
        name="知識の噴火",
        mp_cost=40,
        target_type=TargetType.ENEMY_SINGLE
    ),
    "ヨガストライク": lambda: YogaStrike(
        name="ヨガストライク",
        hp_cost=40,
        target_type=TargetType.ENEMY_SINGLE
    ),
    "瞑想の波動": lambda: Meditation(
        name="瞑想の波動",
        mp_cost=0,
        target_type=TargetType.ENEMY_SINGLE
    ),
}
def create_skills(skill_list):
    result = {}
    for skill in skill_list:
        result[skill] = create_skill(skill)
    return result

def create_skill(skill_key):
    return SKILL_REGISTRY[skill_key]()
