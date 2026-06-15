from unittest.mock import MagicMock

import pytest

from game.domain.effect.buff_effect import StatBuffEffect
from game.domain.skills.concentrate import Concentrate


@pytest.fixture
def mock_char():
    char = MagicMock()
    char.name = "TestChar"
    char.stats.hp = 100
    char.stats.max_hp = 100
    char.stats.mp = 10
    char.stats.magic_atk = 50
    char.effects = []
    char.is_alive.return_value = True
    # Implement add_effect manually since MagicMock doesn't
    def add_effect(effect):
        char.effects.append(effect)
    char.add_effect = list().append # simpler mock 
    char.add_effect = MagicMock(side_effect=add_effect)
    return char

@pytest.fixture
def battle():
    b = MagicMock()
    b.log = []
    return b

def test_concentrate_hp_cost(mock_char, battle):
    skill = Concentrate(name="コンセントレイト", hp_cost=20)
    targets = [mock_char]

    skill.use(mock_char, targets, battle)

    assert mock_char.stats.hp == 80  # 100 - 20
    assert any("体力を削って" in msg for msg in battle.log)

def test_concentrate_insufficient_hp(mock_char, battle):
    skill = Concentrate(name="コンセントレイト", hp_cost=20)
    mock_char.stats.hp = 10
    targets = [mock_char]

    skill.use(mock_char, targets, battle)

    assert mock_char.stats.hp == 10  # No change
    assert any("体力が足りない！" in msg for msg in battle.log)
    # Ensure apply was not called (magic_atk not changed)
    assert mock_char.stats.magic_atk == 50

def test_concentrate_apply_buff(mock_char, battle):
    skill = Concentrate(name="コンセントレイト", hp_cost=20)
    # Assume cost paid
    mock_char.stats.hp = 100 

    skill.apply(mock_char, mock_char, battle)

    assert mock_char.stats.magic_atk == 80 # 50 + 30
    assert len(mock_char.effects) == 1
    effect = mock_char.effects[0]
    assert isinstance(effect, StatBuffEffect)
    assert effect.stat_name == "magic_atk"
    assert effect.amount == 30
    assert effect.duration == 3

def test_buff_removal(mock_char, battle):
    # Test StatBuffEffect behavior directly
    effect = StatBuffEffect(
        name="TestBuff",
        duration=0,
        stat_name="magic_atk",
        amount=30
    )
    # Set init state
    mock_char.stats.magic_atk = 80

    effect.on_remove(mock_char, battle)

    assert mock_char.stats.magic_atk == 50 # 80 - 30
