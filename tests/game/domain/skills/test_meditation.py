from unittest.mock import MagicMock, patch

import pytest

from game.domain.effect.buff_effect import StatBuffEffect
from game.domain.skills.meditation import Meditation


@pytest.fixture
def mock_actor():
    actor = MagicMock()
    actor.name = "Monk"

    class StatsMock:
        def __init__(self):
            self.hp = 100
            self.max_hp = 100
            self.mp = 10
            self.max_mp = 50
            self.magic_atk = 20
    actor.stats = StatsMock()
    actor.is_alive.return_value = True
    return actor

@pytest.fixture
def mock_enemy():
    enemy = MagicMock()
    enemy.name = "Slime"

    class StatsMock:
        def __init__(self):
            self.magic_resistance = 20
    enemy.stats = StatsMock()
    enemy.is_alive.return_value = True
    enemy.effects = []
    def add_effect(effect):
        enemy.effects.append(effect)
    enemy.add_effect = MagicMock(side_effect=add_effect)
    return enemy

@pytest.fixture
def battle():
    b = MagicMock()
    b.log = []
    return b

def test_meditation_effect(mock_actor, mock_enemy, battle):
    skill = Meditation(name="瞑想", mp_cost=0)

    with patch("game.domain.skills.meditation.calculate_meditation_total_time", return_value=120):
        skill.apply(mock_actor, mock_enemy, battle)

        # MP recovery calculation: base(10) + bonus(120 // 10 = 12) = 22
        mock_actor.get_mp_heal.assert_called_once_with(22)

        # Damage calculation check
        # base_dmg = 20 * 1.5 + 120 / 2 = 30 + 60 = 90
        # Damage formula: base_dmg * (3 * magic_atk) / (2 * magic_atk + target_magic_resistance)
        # = 90 * 60 / 60 = 90
        mock_enemy.take_damage.assert_called_once_with(90.0)

        # Debuff calculation: 10 + min(120 // 20 = 6, 30) = 16
        # Initial magic_resistance = 20 - 16 = 4
        assert mock_enemy.stats.magic_resistance == 4
        assert any(isinstance(e, StatBuffEffect) for e in mock_enemy.effects)

        # Effect check
        effect = mock_enemy.effects[0]
        assert effect.stat_name == "magic_resistance"
        assert effect.amount == -16
        assert effect.duration == 5

        # Log check
        assert any("深く瞑想し" in msg for msg in battle.log)
        assert any("MPが 22 回復" in msg for msg in battle.log)
        assert any("魔法ダメージ" in msg for msg in battle.log)
        assert any("魔法防御力が下がった" in msg for msg in battle.log)
