from game.domain.models.command import Command


class BattleService:

    def execute_player_turn(
        self,
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

        battle.execute(command)
        battle.check_battle_end()
