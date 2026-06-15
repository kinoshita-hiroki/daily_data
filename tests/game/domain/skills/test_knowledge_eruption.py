from unittest.mock import MagicMock, patch

import pytest

from game.domain.effect.delayed_damage_effect import DelayedDamageEffect
from game.domain.effect.stun_effect import StunEffect
from game.domain.skills.knowledge_eruption import KnowledgeEruption


@pytest.fixture
def mock_actor():
    actor = MagicMock()
    actor.name = "Mage"
    actor.stats.mp = 100
    actor.effects = []
    def add_effect(e):
        actor.effects.append(e)
    actor.add_effect = MagicMock(side_effect=add_effect)
    return actor

@pytest.fixture
def mock_target():
    target = MagicMock()
    target.name = "Enemy"
    target.effects = []
    def add_effect(e):
        target.effects.append(e)
    target.add_effect = MagicMock(side_effect=add_effect)
    return target

@pytest.fixture
def battle():
    b = MagicMock()
    b.log = []
    return b

def test_knowledge_eruption_applies_effects(mock_actor, mock_target, battle):
    skill = KnowledgeEruption()

    with patch("game.domain.skills.knowledge_eruption.calculate_study_time_ma", return_value=15.0):
        with patch("game.domain.models.damage_calculator.DamageCalculator.magical", return_value=150):
            skill.apply(mock_actor, mock_target, battle)

        # Caster should have StunEffect
        assert any(isinstance(e, StunEffect) for e in mock_actor.effects)

        # Target should have DelayedDamageEffect
        assert any(isinstance(e, DelayedDamageEffect) for e in mock_target.effects)

        # Check damage logic in effect
        effect = next(e for e in mock_target.effects if isinstance(e, DelayedDamageEffect))
        assert effect.damage == 150 # 15 * 10

def test_delayed_damage_effect_triggers_on_remove(mock_target, battle):
    effect = DelayedDamageEffect(name="Test", duration=1, damage=100)
    effect.on_remove(mock_target, battle)

    mock_target.take_damage.assert_called_once_with(100)
    assert any("knowledge が噴火" in msg.lower() or "知識が噴火" in msg for msg in battle.log)

def test_stun_effect_prevents_action(mock_actor):
    # This test assumes Character.can_act is already implemented and uses isinstance(e, StunEffect)
    from game.domain.models.character import Character
    from game.domain.models.stats import Stats

    stats = Stats(hp=100, max_hp=100, mp=10, max_mp=10)
    char = Character(name="Mage", stats=stats, skills={}, effects=[])

    assert char.can_act() is True

    char.add_effect(StunEffect(name="Stun", duration=3))
    assert char.can_act() is False
