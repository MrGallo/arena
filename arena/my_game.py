from typing import Optional, Any

from arena.base_game import BaseGame
from arena.base_view import GameEntity


class MyGame(BaseGame):
    def create(self, ViewClass: Optional[type[GameEntity]] = None, *args: Any, **kwargs: Any) -> None:
        if ViewClass is None:
            from arena.battle_view import BattleView
            ViewClass = BattleView

        MyGame.set_current_view(ViewClass(*args, **kwargs))
