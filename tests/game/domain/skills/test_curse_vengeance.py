from unittest.mock import MagicMock, patch

import pytest
from game.domain.effect.curse_effect import CurseEffect
from game.domain.skills.enemy.curse import Curse

from game.domain.models.stats import Stats
from game.domain.skills.enemy.vengeance import Vengeance


@pytest.fixture
def mock_char():
    char = MagicMock()
    char.name = "Hero"
    char.stats = Stats(
        hp=100,
        mp=50,
        atk=20,
        defense=0,
        magic_atk=20
    )
    char.is_alive.return_value = True
    char.effects = []
    def add_effect(effect):
        char.effects.append(effect)
    char.add_effect = MagicMock(side_effect=add_effect)
    return char

@pytest.fixture
def mock_target():
    target = MagicMock()
    target.name = "Enemy"
    target.stats = Stats(
        hp=100,
        mp=50,
        atk=10,
        defense=0,
        magic_resistance=0
    )
    target.is_alive.return_value = True
    target.effects = []
    def add_effect(effect):
        target.effects.append(effect)
    target.add_effect = MagicMock(side_effect=add_effect)
    target.take_damage.side_effect = lambda dmg: dmg
    return target

@pytest.fixture
def battle():
    b = MagicMock()
    b.log = []
    return b

def test_curse_applies_effect(mock_char, mock_target, battle):
    skill = Curse(name="呪い", mp_cost=10)
    with patch("random.randint", return_value=10):
        with patch("game.domain.skills.enemy.curse.calculate_condition_avg", return_value=5):
            skill.use(mock_char, [mock_target], battle)

    assert mock_char.stats.mp == 40
    assert any(isinstance(e, CurseEffect) for e in mock_target.effects)
    assert any("呪い状態になった！" in msg for msg in battle.log)

def test_vengeance_bonus_damage(mock_char, mock_target, battle):
    # Apply curse first
    curse = CurseEffect(name="呪い", duration=3)
    mock_target.effects.append(curse)

    skill = Vengeance(name="復讐", mp_cost=15)
    skill.use(mock_char, [mock_target], battle)

    assert mock_char.stats.mp == 35
    # Actor magic_atk 20, Target magic_resistance 0, base_dmg = 20 * 1.3 = 26
    # Damage calculation: base_dmg * (3 * 20) / (2 * 20 + 0) = 26 * 1.5 = 39
    assert any("Enemyへの復讐！" in msg for msg in battle.log)
    assert any("Enemyに 39 の痛恨のダメージ！" in msg for msg in battle.log)
    # Effect should be removed
    assert not any(isinstance(e, CurseEffect) for e in mock_target.effects)

def test_vengeance_normal_damage(mock_char, mock_target, battle):
    # No curse effect
    skill = Vengeance(name="復讐", mp_cost=15)
    skill.use(mock_char, [mock_target], battle)

    assert mock_char.stats.mp == 35
    # Actor magic_atk 20, base_dmg = 20 * 0.8 = 16
    # Damage: 16 * 1.5 = 24
    assert any("Heroの復讐！ Enemyに 24 ダメージ" in msg for msg in battle.log)
    assert not any("Enemyへの復讐！" in msg for msg in battle.log)
