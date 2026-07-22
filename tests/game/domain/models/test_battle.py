from unittest.mock import MagicMock

import pytest

from game.domain.models.battle import Battle
from game.domain.models.target_type import TargetType
from game.domain.skills.skill import Skill


@pytest.fixture
def mock_player():
    player = MagicMock()
    player.name = "Hero"
    player.is_alive.return_value = True
    player.stats.hp = 100
    player.stats.max_hp = 100
    return player

@pytest.fixture
def mock_enemy():
    enemy = MagicMock()
    enemy.name = "Monster"
    enemy.is_alive.return_value = True
    enemy.stats.hp = 100
    enemy.stats.max_hp = 100
    enemy.stats.atk = 50
    # Mock choose_skill to return a skill with a name
    mock_skill = MagicMock()
    mock_skill.name = "Attack"
    enemy.choose_skill.return_value = mock_skill
    return enemy

def test_battle_initialization(mock_player, mock_enemy):
    battle = Battle(players=[mock_player], enemies=[mock_enemy])
    assert battle.actor_index == 0
    assert len(battle.all_actors()) == 2

def test_battle_is_finished(mock_player, mock_enemy):
    battle = Battle(players=[mock_player], enemies=[mock_enemy])
    assert battle.is_finished() is False

    mock_player.is_alive.return_value = False
    assert battle.is_finished() is True


class DummySkill(Skill):
    def apply(self, actor, target, battle):
        pass


def test_resolve_targets_enemy_single(mock_player, mock_enemy):
    battle = Battle(players=[mock_player], enemies=[mock_enemy])
    skill = DummySkill(name="TestSkill", target_type=TargetType.OPPONENT_SINGLE)

    targets = skill.resolve_targets(battle, target=mock_enemy)
    assert len(targets) == 1
    assert targets[0] == mock_enemy

def test_resolve_targets_enemy_all(mock_player, mock_enemy):
    battle = Battle(players=[mock_player], enemies=[mock_enemy])
    skill = DummySkill(name="TestSkill", target_type=TargetType.OPPONENT_ALL)

    targets = skill.resolve_targets(battle, actor=mock_player)
    assert len(targets) == 1
    assert targets[0] == mock_enemy

def test_resolve_targets_self(mock_player, mock_enemy):
    battle = Battle(players=[mock_player], enemies=[mock_enemy])
    skill = DummySkill(name="TestSkill", target_type=TargetType.SELF)

    targets = skill.resolve_targets(battle, actor=mock_player)
    assert len(targets) == 1
    assert targets[0] == mock_player

def test_resolve_targets_no_target(mock_player, mock_enemy):
    battle = Battle(players=[mock_player], enemies=[mock_enemy])
    skill = DummySkill(name="TestSkill", target_type=TargetType.OPPONENT_SINGLE)

    targets = skill.resolve_targets(battle, target=None)
    assert len(targets) == 0

