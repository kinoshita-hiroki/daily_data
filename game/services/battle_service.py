from game.domain.models.command import Command


class BattleService:
    @staticmethod
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

    @staticmethod
    def check_turn_status(battle, actor):
        if not(actor.is_alive()):
            battle.log.append(f"{actor.name}は倒れている…")
            battle.next_turn()
            return False

        if not actor.can_act():
            # battle.log.append(f"{actor.name}は動けない！") # Effect.on_turn_start でメッセージを出している想定
            battle.next_turn()
            return False

        return True