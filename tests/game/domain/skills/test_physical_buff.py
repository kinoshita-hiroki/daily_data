from unittest.mock import MagicMock, patch

import pytest

from game.domain.skills.physical_buff import PhysicalBuff


@pytest.fixture
def mock_char():
    char = MagicMock()
    char.name = "Warrior"
    char.stats.hp = 100
    char.stats.mp = 20
    char.stats.atk = 10
    char.stats.defense = 10
    char.effects = []

    def add_effect(effect):
        char.effects.append(effect)
    char.add_effect = MagicMock(side_effect=add_effect)
    return char

@pytest.fixture
def battle():
    b = MagicMock()
    b.log = []
    return b

def test_physical_buff_cumulative_logic(mock_char, battle):
    skill = PhysicalBuff()

    with patch("game.domain.skills.physical_buff.calculate_workout_done_sum", return_value=150):
        skill.apply(mock_char, mock_char, battle)

    # buff_amount should be 15
    assert mock_char.stats.atk == 25 # 10 + 15
    assert mock_char.stats.defense == 25
    assert any("上昇量: 15" in msg for msg in battle.log)

def test_physical_buff_no_cumulative_workout(mock_char, battle):
    skill = PhysicalBuff()

    with patch("game.domain.skills.physical_buff.calculate_workout_done_sum", return_value=0):
        skill.apply(mock_char, mock_char, battle)

    assert mock_char.stats.atk == 10
    assert mock_char.stats.defense == 10
    assert any("十分な鍛錬を積んでいない" in msg for msg in battle.log)
