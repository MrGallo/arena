from typing import Dict, Any
import sys
from pathlib import Path
import importlib


from arena.my_game import MyGame
from arena.battle_view import ChampionShowcase, TestBattle_ReachGoal


def main():
    if len(sys.argv) < 3:
        print("Usage: python -m arena <view_name> <champion_dir>")
        sys.exit(1)

    view_name = sys.argv[1]
    champion_dir = Path(sys.argv[2]).resolve()

    if not champion_dir.exists() or not champion_dir.is_dir():
        print(f"Invalid champion directory: {champion_dir}")
        sys.exit(1)

    # print(f"View: {view_name}")
    # print(f"Champion directory: {champion_dir}")

    champion_classes = load_champion_classes(champion_dir)
    
    if view_name == "showcase":
        game = MyGame(ChampionShowcase, champion_classes=champion_classes)
    elif view_name == "test_reach_goal":
        game = MyGame(TestBattle_ReachGoal, champion_classes=champion_classes)
    else:
        print(f"Invalid view name '{view_name}'")
        sys.exit(1)
    game.run()


def load_champion_classes(champion_dir: Path):
    champions = []

    for py_file in champion_dir.glob("*_champion.py"):
        module_name = f"_arena_dynamic_.{py_file.stem}"

        spec = importlib.util.spec_from_file_location(module_name, py_file)
        module = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(module)

        if hasattr(module, "Champion"):
            champions.append(module.Champion)

    return champions


if __name__ == "__main__":
    main()



