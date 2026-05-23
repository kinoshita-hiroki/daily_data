import random
from typing import TYPE_CHECKING, List

from game.domain.skills.skill import Skill

if TYPE_CHECKING:
    from game.domain.battle import Battle

    from game.domain.models.character import Character
from game.domain.models.damage_calculator import DamageCalculator


class EnemyAttack(Skill):

    def use(self, actor: "Character", targets: List["Character"], battle: "Battle") -> None:
        if not self.check_cost(actor, battle):
            return

        self.pay_cost(actor)

        # ランダムにターゲットを決定
        target = random.choice(targets)
        self.apply(actor, target, battle)

    def apply(self, actor: "Character", target: "Character", battle: "Battle") -> None:
        # ダメージ計算
        final_dmg = DamageCalculator.physical(actor, target, base_damage=actor.stats.atk)
        target.take_damage(final_dmg)

        battle.log.append(
            f"{actor.name}の攻撃！ {target.name}に {int(final_dmg)} ダメージ"
        )
