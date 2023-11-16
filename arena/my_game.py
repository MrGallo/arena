from arena.base_game import BaseGame


class MyGame(BaseGame):
    def create(self) -> None:
        from arena.battle_view import BattleView
        MyGame.set_current_view(BattleView())
