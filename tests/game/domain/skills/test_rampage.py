from unittest.mock import MagicMock

import pytest

from game.domain.skills.enemy.rampage import Rampage


@pytest.fixture
def mock_char():
    char = MagicMock()
    char.name = "TestChar"
    char.stats.hp = 100
    char.stats.max_hp = 100
    char.stats.mp = 10
    char.stats.atk = 50
    char.is_alive.return_value = True
    return char

@pytest.fixture
def mock_target():
    target = MagicMock()
    target.name = "Target"
    target.stats.hp = 100
    target.take_physical_damage.return_value = 10
    target.is_alive.return_value = True
    return target

@pytest.fixture
def battle():
    b = MagicMock()
    b.log = []
    return b

def test_rampage_mp_cost(mock_char, mock_target, battle):
    skill = Rampage(name="Rampage", mp_cost=5)
    targets = [mock_target]

    skill.use(mock_char, targets, battle)

    assert mock_char.stats.mp == 5  # 10 - 5
    # Rampage attacks 3 times, so apply should be called 3 times
    # In mock, we can check battle log or target damage calls
    assert len(battle.log) == 3 # 3 attacks

def test_rampage_insufficient_mp(mock_char, mock_target, battle):
    skill = Rampage(name="Rampage", mp_cost=20)
    targets = [mock_target]

    skill.use(mock_char, targets, battle)

    assert mock_char.stats.mp == 10  # No change
    assert any("MPが足りない" in msg for msg in battle.log)
    # Ensure no attacks happened
    assert mock_target.take_physical_damage.call_count == 0
