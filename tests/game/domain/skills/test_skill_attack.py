from unittest.mock import MagicMock, patch

import pytest
from game.domain.skills.skill_attack import SkillAttack


@pytest.fixture
def mock_actor():
    actor = MagicMock()
    actor.name = "Hero"
    actor.stats.atk = 20
    actor.stats.hp = 100
    actor.is_alive.return_value = True
    return actor

@pytest.fixture
def mock_target():
    target = MagicMock()
    target.name = "Enemy"
    target.is_alive.return_value = True
    target.stats.hp = 100
    target.stats.defense = 10
    return target

@pytest.fixture
def battle():
    b = MagicMock()
    b.log = []
    return b

def test_skill_attack_damage_calculation(mock_actor, mock_target, battle):
    skill = SkillAttack(name="スキルアタック", hp_cost=30)

    # human_skill = 40 を想定
    # (atk * 1.5) + (human_skill * 3) = (20 * 1.5) + (40 * 3) = 30 + 120 = 150
    # DamageCalculator.physical は標準的な計算を行う (150 - target.defense/2) など。
    # ここでは apply が呼ばれた際にダメージが正しく渡されるかをモックで確認する

    with patch("game.domain.skills.skill_attack.calculate_human_skill_last_value", return_value=40):
        with patch("game.domain.models.damage_calculator.DamageCalculator.physical", return_value=145) as mock_calc:
            skill.apply(mock_actor, mock_target, battle)

            # 正しいダメージ値が計算機に渡されているか
            mock_calc.assert_called_once_with(mock_actor, mock_target, base_damage=150.0)

            # ターゲットがダメージを受けているか
            mock_target.take_damage.assert_called_once_with(145)

            # ログの確認
            assert any("スキルアタックを放った！" in msg for msg in battle.log)
            assert any("145 のダメージ" in msg for msg in battle.log)

def test_skill_attack_hp_cost_reporting(mock_actor, mock_target, battle):
    skill = SkillAttack(name="スキルアタック", hp_cost=30)
    with patch("game.domain.skills.skill_attack.calculate_human_skill_last_value", return_value=10):
        skill.apply(mock_actor, mock_target, battle)
        assert any("HP -30" in msg for msg in battle.log)
