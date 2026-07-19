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
        if not skill.check_cost(actor, battle):
            return
        command = Command(
            actor=actor,
            target=target,
            skill=skill
        )
        BattleService.execute_turn(
            battle,
            command
        )


    @staticmethod
    def execute_enemy_turn(battle,enemy:Enemy) -> None:
        command = enemy.decide_command()
        BattleService.execute_turn(
            battle,
            command
        )

    @staticmethod
    def execute_turn(battle,command:Command):
        actor = command.actor
        battle.process_turn_start(actor)
        battle.execute(command)
        BattleService.next_turn(battle)


    @staticmethod
    def next_turn(battle) -> None:
        # 次の行動者へ
        battle.advance_turn()

    @staticmethod
    def update(battle):
        while True:
            if battle.is_finished():
                return 
            actor = battle.current_actor()
            if not actor.is_alive():
                BattleService.next_turn(battle)
                continue
            if not actor.can_act():
                BattleService.next_turn(battle)
                continue
            if isinstance(actor, Enemy):
                BattleService.execute_enemy_turn(battle,actor)
                continue
            return


