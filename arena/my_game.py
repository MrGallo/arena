from arena.base_game import BaseGame


class MyGame(BaseGame):
    def create(self) -> None:
        from arena.title_view import TitleView
        MyGame.set_current_view(TitleView())
