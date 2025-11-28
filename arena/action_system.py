class ActionSystem:
    MOVE = "move"

    @staticmethod
    def move(champion_sprite, displacement):
        champion_sprite.position += displacement