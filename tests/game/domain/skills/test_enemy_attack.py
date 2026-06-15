from unittest.mock import MagicMock

import pytest

from game.domain.skills.enemy.enemy_attack import EnemyAttack


@pytest.fixture
def mock_actor():
    actor = MagicMock()
    actor.name = "TestActor"
    actor.stats.atk = 20
    actor.stats.mp = 10
    actor.stats.hp = 100
    actor.stats.max_hp = 100
    return actor

@pytest.fixture
def mock_target():
    target = MagicMock()
    target.name = "TestTarget"
    target.take_damage.return_value = None
    return target

@pytest.fixture
def mock_battle():
    battle = MagicMock()
    battle.log = []
    return battle

def test_enemy_attack_use_success(mock_actor, mock_target, mock_battle):
    skill = EnemyAttack(name="TestAttack", mp_cost=5)
    targets = [mock_target]

    skill.use(mock_actor, targets, mock_battle)

    # Check MP consumption
    assert mock_actor.stats.mp == 5  # 10 - 5 = 5

    # Check damage application
    mock_target.take_damage.assert_called_once()

    # Check updated log
    assert len(mock_battle.log) > 0
    assert "TestActorの攻撃！" in mock_battle.log[0]

def test_enemy_attack_not_enough_mp(mock_actor, mock_target, mock_battle):
    skill = EnemyAttack(name="TestAttack", mp_cost=20)
    mock_actor.stats.mp = 10
    targets = [mock_target]

    skill.use(mock_actor, targets, mock_battle)

    # Check MP not consumed
    assert mock_actor.stats.mp == 10

    # Check no damage
    mock_target.take_damage.assert_not_called()

    # Check log message
    assert "MPが足りない" in mock_battle.log[0]
