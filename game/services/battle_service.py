from game.domain.models.command import Command
from game.domain.models.enemy import Enemy


class BattleService:
    @staticmethod
    def execute_player_turn(
        battle,
        actor,
        skill,
        target
    ):
        battle.process_turn_start(actor)
        if not skill.check_cost(actor, battle):
            return

        command = Command(
            actor=actor,
            target=target,
            skill=skill
        )

        battle.execute(command)
        BattleService.next_turn(battle)
        battle.check_battle_end()


    @staticmethod
    def execute_enemy_turn(battle,enemy:Enemy) -> None:
        battle.process_turn_start(enemy)
        targets = battle.alive_players()
        if not targets:
            battle.log.append("💀 全滅…")
            return
        command = enemy.decide_command()
        battle.execute(command)

    @staticmethod
    def next_turn(battle) -> None:
        # 次の行動者へ
        battle.actor_index += 1

        # 行動者がいなくなったら
        if battle.actor_index >= len(battle.players) + len(battle.enemies):
            battle.actor_index = 0
    @staticmethod
    def execute_turn(battle,actor):
        battle.process_turn_start(actor)

    @staticmethod
    def prepare_player_input(battle):
        while True:
            actor = battle.current_actor()

            if isinstance(actor, Enemy):
                BattleService.execute_enemy_turn(battle,actor)
                BattleService.next_turn(battle)
                continue
            if not actor.is_alive():
                BattleService.next_turn(battle)
                continue
            if not actor.can_act():
                BattleService.next_turn(battle)
                continue
            return actor

