import pytest

from arena.team import Team
from arena.sprite import Sprite as Sprite

class TestChampionWithoutTeam:
    pass


class TestChampTeamPosition0:
    class Team:
        position = 0


class TestChampTeamPosition1:
    class Team:
        position = 1


class TestChampTeamPosition2:
    class Team:
        position = 2


def test_team_adds_champ():
    champ = TestChampionWithoutTeam()
    team = Team([champ], ((0, 0), ), "test team")
    assert len(team.get_sprites()) == 1
    assert len(team.get_champs()) == 1
    assert type(team.champion_sprite_map[champ]) == Sprite

def test_team_adds_champ_at_proper_spot():
    champ = TestChampionWithoutTeam()
    team = Team([champ], ((50, 70), ), "test team")
    assert team.get_sprites()[0].position == (50, 70)

def test_team_adds_in_proper_position():
    roster = [
        TestChampTeamPosition2(),
        TestChampTeamPosition0(),
        TestChampTeamPosition1(),
    ]

    positions = ((0, 0), (1, 1), (2, 2))

    team = Team(roster, positions, "test team")
    assert team.champion_sprite_map[roster[0]].position == (2, 2)
    assert team.champion_sprite_map[roster[1]].position == (0, 0)
    assert team.champion_sprite_map[roster[2]].position == (1, 1)

def test_team_adds_those_with_position_and_those_without():
    roster = [
        TestChampTeamPosition2(),
        TestChampionWithoutTeam(),  # should be pos 3 as other have explicit positions
        TestChampTeamPosition0(),
        TestChampTeamPosition1(),
    ]

    positions = ((0, 0), (1, 1), (2, 2), (3, 3))

    team = Team(roster, positions, "test team")
    assert team.champion_sprite_map[roster[0]].position == (2, 2)
    assert team.champion_sprite_map[roster[1]].position == (3, 3)
    assert team.champion_sprite_map[roster[2]].position == (0, 0)
    assert team.champion_sprite_map[roster[3]].position == (1, 1)

def test_team_adds_those_with_position_and_those_with_duplicate_positions():
    roster = [
        TestChampTeamPosition2(),
        TestChampTeamPosition2(),
        TestChampTeamPosition1(),
    ]

    positions = ((0, 0), (1, 1), (2, 2))

    team = Team(roster, positions, "test team")
    assert team.champion_sprite_map[roster[0]].position == (2, 2)
    assert team.champion_sprite_map[roster[1]].position == (0, 0), "Duplicate pos should go to back of line"
    assert team.champion_sprite_map[roster[2]].position == (1, 1)


def test_team_raises_value_error_when_roster_and_positions_not_same_size():
    with pytest.raises(AssertionError):
        Team([TestChampionWithoutTeam()], ((0, 0), (1, 1)), "test_test"), "Roster size and positions must be equal"