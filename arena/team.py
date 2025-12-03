from typing import Optional

from arena.base_view import GameEntity
from arena.sprite import Sprite
from arena.settings import Settings


class Team:
    BLUE = "blue"
    RED = "red"

    def __init__(self, roster: list[GameEntity], positions: tuple[int, int], name):
        assert len(roster) == len(positions), "The roster must have same length as positions"

        self.name = name
        self.champion_positions = []
        self.champion_sprite_map = {}
        available_positions: Optional[tuple[int, int]] = list(positions)

        # handle champs with explicit positions
        for champ in roster:
            if hasattr(champ, "Team") and hasattr(champ.Team, "position"):
                requested_position = champ.Team.position
                if available_positions[requested_position] is not None:
                    position = available_positions[requested_position]
                    available_positions[requested_position] = None
                    self.champion_sprite_map[champ] = Sprite(champ, position, Settings.cellsize)

        # then handle those without or champs who requested a taken position
        position_cursor = 0
        available_positions = [pos for pos in available_positions if pos is not None]
        for champ in roster:
            if champ not in self.champion_sprite_map.keys():
                position = available_positions[position_cursor]
                self.champion_sprite_map[champ] = Sprite(champ, position, Settings.cellsize)
                position_cursor += 1

    
    def get_sprites(self) -> tuple[Sprite]:
        return tuple(self.champion_sprite_map.values())
            
    def get_champs(self) -> tuple[GameEntity]:
        return tuple(self.champion_sprite_map.keys())