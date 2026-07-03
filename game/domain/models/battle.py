from dataclasses import dataclass, field
from typing import List, Optional, Tuple

from game.domain.models.character import Character
from game.domain.models.command import Command
from game.domain.models.enemy import Enemy
from game.domain.models.player import Player
from game.domain.models.target_type import TargetType
from game.domain.skills.skill import Skill


@dataclass
class Battle:
    players: List[Player]
    enemies: List[Enemy]
    actor_index: int = 0
    log: list = field(default_factory=list)

    def all_actors(self) -> List[Character]:
        return self.players + self.enemies

    def alive_players(self) -> List[Player]:
        return [
            p for p in self.players
            if p.is_alive()
        ]

    def alive_enemies(self) -> List[Enemy]:
        return [
            p for p in self.enemies
            if p.is_alive()
        ]

    def execute(self, command: Command) -> None:
        actor = command.actor
        skill = command.skill
        targets = self.resolve_targets(skill, command.target, actor)

        skill.use(actor, targets, self)
        self.next_turn()

    def next_actor(self) -> Tuple[int, Character]:
        order = self.all_actors()
        if not order:
            raise ValueError("No characters in battle")
        return (self.actor_index % len(order)), order[self.actor_index % len(order)]

    def get_actor(self, actor_id: int) -> Character:
        actors = self.players + self.enemies
        if 0 <= actor_id < len(actors):
            return actors[actor_id]
        raise IndexError(f"Actor id {actor_id} out of range")

    def next_turn(self) -> None:
        self.actor_index += 1
        if self.actor_index >= len(self.players) + len(self.enemies):
            self.actor_index = 0
            self.process_turn_start()
        if self.actor_index >= len(self.players):
            self.enemy_turn()

    def enemy_turn(self) -> None:
        for i in range(len(self.enemies)):
            enemy = self.enemies[i]
            if not enemy.is_alive():
                continue

            targets = self.alive_players()
            if not targets:
                self.log.append("💀 全滅…")
                return


            command = enemy.decide_command()
            self.execute(command)


    def process_turn_start(self) -> None:
        for c in self.all_actors():
            if c.is_alive():
                for effect in c.effects[:]:
                    effect.on_turn_start(c, self)
                    effect.tick()
                    if effect.is_expired():
                        effect.on_remove(c, self)
                        c.effects.remove(effect)
                        self.log.append(
                            f"{c.name}の{effect.name}が解除された"
                        )


    def is_finished(self) -> bool:
        return (
            not self.alive_players()
            or not self.alive_enemies()
        )

    def check_battle_end(self) -> None:
        if len(self.alive_enemies()) <= 0:
            self.log.append("🎉 勝利！")

    def resolve_targets(self, skill: Skill, target: Optional[Character] = None, actor: Optional[Character] = None) -> List[Character]:
        """
        必ず list を返す
        """
        match skill.target_type:
            case TargetType.ENEMY_SINGLE:
                # ターゲット指定がなくても動くようにガード
                if target is None:
                     return []
                return [target]

            case TargetType.ENEMY_ALL:
                enemies = self.alive_enemies()
                return enemies

            case TargetType.ALLY_SINGLE:
                 if target is None:
                     return []
                 return [target]

            case TargetType.ALLY_ALL:
                players = self.alive_players()
                return players

            case TargetType.SELF:
                if actor is None:
                    return []
                return [actor]

            case _:
                raise ValueError(f"Unknown target_type: {skill.target_type}")



