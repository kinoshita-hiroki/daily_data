from unittest.mock import patch

from game.domain.models.battle import Battle
from game.domain.models.enemy import Enemy
from game.domain.models.player import Player
from game.domain.models.stats import Stats
from game.domain.skills.yoga_strike import YogaStrike


def test_yoga_strike_success():
    actor = Player(name="戦士", stats=Stats(hp=100, max_hp=100, mp=50, max_mp=50, atk=20, defense=10, magic_atk=10, magic_resistance=10), job=None, skills={}, effects=[])
    target = Enemy(name="スライム", stats=Stats(hp=100, max_hp=100, mp=50, max_mp=50, atk=10, defense=5, magic_atk=10, magic_resistance=10), skills={}, effects=[])
    battle = Battle(players=[actor], enemies=[target])

    skill = YogaStrike(name="ヨガストライク", hp_cost=30)

    # mock the yoga time to calculate a known damage
    with patch("game.domain.skills.yoga_strike.calculate_yoga_total_time", return_value=120):
        skill.use(actor, [target], battle)

    # HP decreases by 30
    assert actor.stats.hp == 70

    # Check that damage was log appended (damage itself depends on DamageCalculator specifics, 
    # but the logs would show it was processed).
    assert any("ヨガストライクを放った！(HP -30)" in log for log in battle.log)

def test_yoga_strike_insufficient_hp():
    actor = Player(name="戦士", stats=Stats(hp=20, max_hp=100, mp=50, max_mp=50, atk=20, defense=10, magic_atk=10, magic_resistance=10), job=None, skills={}, effects=[])
    target = Enemy(name="スライム", stats=Stats(hp=100, max_hp=100, mp=50, max_mp=50, atk=10, defense=5, magic_atk=10, magic_resistance=10), skills={}, effects=[])
    battle = Battle(players=[actor], enemies=[target])

    skill = YogaStrike(name="ヨガストライク", hp_cost=30)

    skill.use(actor, [target], battle)

    # HP should remain the same
    assert actor.stats.hp == 20

    # Ensure error message is logged
    assert any("体力が足りない！" in log for log in battle.log)
