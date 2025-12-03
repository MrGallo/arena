import argparse
import sys
from pathlib import Path
import importlib.util


from arena.team import Team


def load_champion_from_file(path: Path):
    spec = importlib.util.spec_from_file_location(path.stem, path)
    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)
    return module.Champion


def load_all_champions(folder: Path):
    champs = []
    for file in folder.iterdir():
        if file.is_file() and file.name.endswith("_champion.py"):
            champs.append(load_champion_from_file(file))
    return champs


def parse_args():
    parser = argparse.ArgumentParser()
    parser.add_argument("level")
    parser.add_argument("extra", nargs="*")
    parser.add_argument("--blue")
    parser.add_argument("--red")
    parser.add_argument("--path")
    return parser.parse_args()


def main():
    args = parse_args()

    # resolve folder
    folder = Path(args.path).resolve() if args.path else Path.cwd()

    # single champion file?
    if len(args.extra) == 1 and Path(args.extra[0]).is_file():
        payload = load_champion_from_file(Path(args.extra[0]))

    else:
        all_champs = load_all_champions(folder)
        payload = {
            Team.BLUE: args.blue,
            Team.RED: args.red,
            "extra": args.extra,  # could be team_name or nothing
            "champions": all_champs,
        }

    from arena.battle_view import VIEW_MAP
    from arena.my_game import MyGame

    level_cls = VIEW_MAP[args.level]
    level = level_cls(payload=payload)
    game = MyGame(level)
    game.run()


if __name__ == "__main__":
    main()

"""
# run a SINGLE champion directly from a file
python -m arena showcase ./champions/rogue_champion.py

# team vs team (explicit folder path)
python -m arena battle_01 --blue knights --red goblins --path ./all_champs/

# team vs team (run inside folder, no --path)
cd all_champs/
python -m arena battle_02 --blue blue_dragons --red red_wolves

# single team challenge (explicit folder path)
python -m arena training_01 blue_dragons --path ./all_champs/

# single team challenge (run inside folder)
cd all_champs/
python -m arena training_02 red_wolves

# free-for-all style level (uses ALL champions in folder)
python -m arena ffa_arena

# multiple extra args (level-specific parameters)
python -m arena debug_level knights speed=2 difficulty=hard
"""