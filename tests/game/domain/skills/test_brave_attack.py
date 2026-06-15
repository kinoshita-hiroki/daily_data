from unittest.mock import MagicMock, patch

import pytest

from game.domain.models.stats import Stats
from game.domain.skills.brave_attack import BraveAttack


@pytest.fixture
def mock_actor():
    actor = MagicMock()
    actor.name = "Hero"
    actor.stats = Stats(
        atk=20,
        magic_atk=15,
        hp=100,
        max_hp=100,
        mp=50
    )
    return actor

@pytest.fixture
def mock_target():
    target = MagicMock()
    target.name = "Enemy"
    target.stats = Stats(
        hp=100,
        defense=0
    )
    target.take_damage = MagicMock()
    return target

@pytest.fixture
def mock_battle():
    battle = MagicMock()
    battle.log = []
    # Mock players
    p1 = MagicMock()
    p1.name = "Hero"
    p1.stats.atk = 20
    p1.stats.magic_atk = 15
    p1.effects = []
    def add_effect_p1(effect):
        p1.effects.append(effect)
    p1.add_effect = MagicMock(side_effect=add_effect_p1)

    p2 = MagicMock()
    p2.name = "Mage"
    p2.stats.atk = 10
    p2.stats.magic_atk = 30
    p2.effects = []
    def add_effect_p2(effect):
        p2.effects.append(effect)
    p2.add_effect = MagicMock(side_effect=add_effect_p2)

    battle.alive_players.return_value = [p1, p2]
    return battle

def test_brave_attack_apply(mock_actor, mock_target, mock_battle):
    # Mock task sum as 80 -> buff amount 10
    with patch("game.domain.skills.brave_attack.calculate_task_sum", return_value=80):
        skill = BraveAttack()
        skill.apply(mock_actor, mock_target, mock_battle)

        # Check damage log
        # Actor Atk 20, Target Def 0, base_damage = 20 * 1.5 = 30. 
        # Formula: 30 * (3 * 20) / (2 * 20 + 0) = 30 * 1.5 = 45
        assert any("勇者の号令！" in msg and "Enemyに 45 のダメージ！" in msg for msg in mock_battle.log)

        # Check buffs on players
        p1 = mock_battle.alive_players()[0]
        p2 = mock_battle.alive_players()[1]

        assert p1.stats.atk == 24 # 20 + 4
        assert p1.stats.magic_atk == 19 # 15 + 4
        assert len(p1.effects) == 2
        assert any(e.stat_name == "atk" and e.amount == 4 for e in p1.effects)
        assert any(e.stat_name == "magic_atk" and e.amount == 4 for e in p1.effects)

        assert p2.stats.atk == 14 # 10 + 4
        assert p2.stats.magic_atk == 34 # 30 + 4
        assert len(p2.effects) == 2
