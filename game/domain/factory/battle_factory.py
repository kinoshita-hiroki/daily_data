from game.domain.factory.enemy_factory import create_enemy
from game.domain.factory.player_factory import create_player
from game.domain.models.battle import Battle


def create_battle(jobs: list[str], enemies: list[str]) -> Battle:
    players = [create_player(job) for job in jobs]
    enemies = [create_enemy(enemy) for enemy in enemies]
    return Battle(players=players, enemies=enemies, turn=0)
