import pytest

from arena.battle_view import BattleView
from arena.team import Team


class TestChampTeamA:
    class Team:
        name = "A"


class TestChampTeamB:
    class Team:
        name = "B"

def test_battle_view():
    teams = [
        Team(),
        Team(),
    ]
    bv = BattleView(teams)