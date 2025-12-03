from typing import Type

import pytest

from arena.base_view import Champion
from arena.battle_view import BattleView
from arena.team import Team


class TestChampNoTeam:
    pass


class TestChampTeamA:
    class Team:
        name = "A"


class TestChampTeamB:
    class Team:
        name = "B"


class TestBattleScenario(BattleView):
    def __init__(self, champion_classes: list[Type[Champion]]):

        team_colors = (Team.Blue, Team.Red)

        team_positions = {
            Team.BLUE: ((1, 1), (2, 2)),
            Team.RED: ((-1, -1), (-2, -2))
        }

        team_objectives = {
            Team.BLUE: "objectives",
            Team.RED: "objectives",
        }

        sorted_champions = Team.sort_into_team_name_champ_list_map(champion_classes)
        teams = {}
        for (color, positions), (name, champs) in zip(team_positions.items(), sorted_champions.items()):
            team = Team(champs, positions, name, color)
            teams[color] = (team, team_objectives[color])

        super().__init__(teams)

# TODO: consider symmetrical maps where depending on team, you can rotate movements
#       to accomodate teams running practice in BLUE. ISSUE: how can absolute positioning be
#       accurately reported in the battle sense? Don't all positions have to be rotated for that
#       particular team?  w

def test_battle_view():
    champion_classes = [
        TestChampTeamA,
        TestChampTeamA,
        TestChampTeamB,
        TestChampTeamB,
    ]
    
    payload = {
        Team.BLUE: "team_one_name",
        Team.RED: "team_two_name",
        "extra": None,
        "champions": champion_classes
    }

    battle_scenario = TestBattleScenario(payload)
