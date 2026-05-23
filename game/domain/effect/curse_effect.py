from dataclasses import dataclass

from game.domain.effect.effect import Effect


@dataclass
class CurseEffect(Effect):
    def on_turn_start(self, target, battle):
        # 審判状態自体はターン開始時に何もしない（マーカーとしての役割）
        pass

    def on_remove(self, target, battle):
        # 効果が切れた時の表示
        battle.log.append(f"{target.name}の呪いが解除された")
