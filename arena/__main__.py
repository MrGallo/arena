from typing import List, Optional
import sys
from pathlib import Path
import importlib.util

from arena.my_game import MyGame
from arena.battle_view import (
    ChampionShowcase,
    TrainingMoveWithinRangeOfPoint,
    TrainingMoveWithRangeAndStop,
    TrainingReachTwoLocationsAndStop,
)


VIEW_MAP = {
    "main_menu": None,
    "showcase": ChampionShowcase,
    "training_movement_01": TrainingMoveWithinRangeOfPoint,
    "training_movement_02": TrainingMoveWithRangeAndStop,
    "training_movement_03": TrainingReachTwoLocationsAndStop,
}


# ------------------------------------------------------
# Helpers
# ------------------------------------------------------

def load_champion_class_from(py_file: Path):
    module_name = f"_arena_dynamic_.{py_file.stem}"

    spec = importlib.util.spec_from_file_location(module_name, py_file)
    if spec is None or spec.loader is None:
        print(f"Could not load champion file: {py_file}")
        return None

    module = importlib.util.module_from_spec(spec)
    spec.loader.exec_module(module)

    champ_cls = getattr(module, "Champion", None)

    if champ_cls is None:
        print(f"File '{py_file.name}' does not contain a Champion class.")
        return None

    return champ_cls


def load_champion_classes(path: Path):
    champions = []

    # Single-file mode
    if path.is_file():
        if path.name.endswith("_champion.py"):
            cls = load_champion_class_from(path)
            if cls:
                champions.append(cls)
        else:
            print(f"File '{path}' is not a *_champion.py file.")
        return champions

    # Directory mode
    if path.is_dir():
        for py_file in path.glob("*_champion.py"):
            cls = load_champion_class_from(py_file)
            if cls:
                champions.append(cls)
        return champions

    print(f"Invalid champion path: {path}")
    return champions


# ------------------------------------------------------
# Entry Point
# ------------------------------------------------------

def main():
    if len(sys.argv) < 3:
        print("Usage: python -m arena <view_name> <champion_path>")
        sys.exit(1)

    view_name = sys.argv[1]
    champion_path = Path(sys.argv[2]).resolve()

    # Validate view
    if view_name not in VIEW_MAP:
        print(f"Invalid view name '{view_name}'. Valid options:")
        for k in VIEW_MAP:
            print("  -", k)
        sys.exit(1)

    # Validate path exists
    if not champion_path.exists():
        print(f"Champion path does not exist: {champion_path}")
        sys.exit(1)

    champion_classes = load_champion_classes(champion_path)

    if not champion_classes:
        print("No valid champion classes found.")
        sys.exit(1)

    game = MyGame(VIEW_MAP[view_name], champion_classes=champion_classes)
    game.run()


if __name__ == "__main__":
    main()
