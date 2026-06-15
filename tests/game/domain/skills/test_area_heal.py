from unittest.mock import MagicMock

import pytest

from game.domain.skills.area_heal import AreaHeal


@pytest.fixture
def mock_char():
    char = MagicMock()
    char.name = "Healer"
    char.stats.hp = 100
    char.stats.max_hp = 100
    char.stats.mp = 20
    char.stats.magic_atk = 30
    char.is_alive.return_value = True
    return char

@pytest.fixture
def mock_targets():
    t1 = MagicMock()
    t1.name = "Target1"
    t1.stats.hp = 50
    t1.stats.max_hp = 100
    t1.is_alive.return_value = True

    t2 = MagicMock()
    t2.name = "Target2"
    t2.stats.hp = 30
    t2.stats.max_hp = 100
    t2.is_alive.return_value = True

    return [t1, t2]

@pytest.fixture
def battle():
    b = MagicMock()
    b.log = []
    return b

def test_area_heal_success(mock_char, mock_targets, battle):
    skill = AreaHeal(name="AreaHeal", mp_cost=12)

    skill.use(mock_char, mock_targets, battle)

    # MP consumption
    assert mock_char.stats.mp == 8  # 20 - 12

    # Healing logic check
    # Target1: base(30) + (100-50)*0.1 = 35
    # Target2: base(30) + (100-30)*0.1 = 37
    mock_targets[0].get_heal.assert_called_once_with(35)
    mock_targets[1].get_heal.assert_called_once_with(37)

    assert any("Target1は 35 回復" in msg for msg in battle.log)
    assert any("Target2は 37 回復" in msg for msg in battle.log)

def test_area_heal_insufficient_mp(mock_char, mock_targets, battle):
    skill = AreaHeal(name="AreaHeal", mp_cost=30)

    skill.use(mock_char, mock_targets, battle)

    assert mock_char.stats.mp == 20  # No change
    assert any("MPが足りない" in msg for msg in battle.log)
    mock_targets[0].get_heal.assert_not_called()
    mock_targets[1].get_heal.assert_not_called()
