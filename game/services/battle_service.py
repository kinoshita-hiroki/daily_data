from game.domain.models.command import Command


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

        battle.execute(command)
        BattleService.next_turn(battle)
        battle.check_battle_end()

    @staticmethod
    def check_turn_status(battle, actor):
        if not actor.is_alive():
            battle.log.append(f"{actor.name}は倒れている…")
            BattleService.next_turn(battle)
            return False

        if not actor.can_act():
            # battle.log.append(f"{actor.name}は動けない！") # Effect.on_turn_start でメッセージを出している想定
            BattleService.next_turn(battle)
            return False

        return True


    @staticmethod
    def enemy_turn(battle) -> None:
        for enemy in battle.alive_enemies():

            targets = battle.alive_players()
            if not targets:
                battle.log.append("💀 全滅…")
                return


            command = enemy.decide_command()
            battle.execute(command)
            BattleService.next_turn(battle)

    @staticmethod
    def next_turn(battle) -> None:
        # 次の行動者へ
        battle.actor_index += 1

        # 行動者がいなくなったら
        if battle.actor_index >= len(battle.players) + len(battle.enemies):
            battle.actor_index = 0
            battle.process_turn_start()
        # 敵ターン
        if battle.actor_index >= len(battle.players):
            BattleService.enemy_turn(battle)

    # @staticmethod
    # def prepare_player_input(battle):
    #     actor = battle.current_actor()

    #     if actor.is_alive() and actor.can_act():
    #         return actor
    #     else:
    #         battle.next_turn()
    #         return None

