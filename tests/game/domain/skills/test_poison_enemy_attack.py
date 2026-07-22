from unittest.mock import MagicMock

import pytest

from game.domain.skills.poison_attack import PoisonAttack


@pytest.fixture
def mock_char():
    char = MagicMock()
    char.name = "TestChar"
    char.stats.hp = 100
    char.stats.max_hp = 100
    char.stats.mp = 10
    char.stats.atk = 50
    char.is_alive.return_value = True
    char.effects = []
    # Implement add_effect manually since MagicMock doesn't
    def add_effect(effect):
        char.effects.append(effect)
    char.add_effect = list().append # simpler mock 
    char.add_effect = MagicMock(side_effect=add_effect)
    return char

@pytest.fixture
def mock_target():
    target = MagicMock()
    target.name = "Target"
    target.stats.hp = 100
    target.take_magical_damage.return_value = 10
    target.take_physical_damage.return_value = 10
    target.is_alive.return_value = True
    target.effects = []
    def add_effect(effect):
        target.effects.append(effect)
    target.add_effect = MagicMock(side_effect=add_effect)
    return target

@pytest.fixture
def battle():
    b = MagicMock()
    b.log = []
    return b

def test_poison_attack_mp_cost(mock_char, mock_target, battle):
    skill = PoisonAttack(name="Poison", mp_cost=5)
    targets = [mock_target]

    skill.use(mock_char, targets, battle)

    assert mock_char.stats.mp == 5  # 10 - 5
    # Check if effect applied (indirectly via log or mock calls)
    assert any("毒状態になった" in msg for msg in battle.log)

def test_poison_attack_insufficient_mp(mock_char, mock_target, battle):
    skill = PoisonAttack(name="Poison", mp_cost=20)
    targets = [mock_target]

    skill.use(mock_char, targets, battle)

    assert mock_char.stats.mp == 10  # No change
    assert any("MPが足りない" in msg for msg in battle.log)
    assert len(mock_target.effects) == 0


