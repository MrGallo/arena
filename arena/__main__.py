from typing import Dict, Any
import sys


from arena.my_game import MyGame
from arena.battle_view import ChampionShowcase

args = sys.argv

try:
    requested_view = args[1].lower()
except IndexError:
    requested_view = ""


view = None
if requested_view == "championshowcase":
    game = MyGame(ChampionShowcase, champions=[])
else:
    game = MyGame()

game.run()
