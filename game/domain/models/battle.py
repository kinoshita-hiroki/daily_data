from dataclasses import dataclass, field
from typing import List, Optional

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

    def current_actor(self) -> Character:
        order = self.all_actors()
        if not order:
            raise ValueError("No characters in battle")
        return order[self.actor_index % len(order)]

    def is_finished(self) -> bool:
        return (
            not self.alive_players()
            or not self.alive_enemies()
        )

    def is_victory(self) -> bool:
        if len(self.alive_enemies()) <= 0:
            self.log.append("🎉 勝利！")
            return True
        return False

    def is_lose(self) -> bool:
        if len(self.alive_players()) <= 0:
            self.log.append("💀 全滅…")
            return True
        return False

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

    def advance_turn(self):
        self.actor_index = (
            self.actor_index + 1
        ) % len(self.all_actors())

    def process_turn_start(self, actor) -> None:
        if actor.is_alive():
            for effect in actor.effects[:]:
                effect.on_turn_start(actor, self)
                effect.tick()
                if effect.is_expired():
                    effect.on_remove(actor, self)
                    actor.effects.remove(effect)
                    self.log.append(
                        f"{actor.name}の{effect.name}が解除された"
                    )

