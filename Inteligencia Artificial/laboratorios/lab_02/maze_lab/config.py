from dataclasses import dataclass


@dataclass(frozen=True)
class TileInfo:
    name: str
    symbol: str
    blocking: bool
    deadly: bool
    color: tuple[int, int, int]


WALL = TileInfo("wall", "#", blocking=True, deadly=False, color=(12, 41, 129))
FLOOR = TileInfo("floor", ".", blocking=False, deadly=False, color=(32, 54, 132))
HOLE = TileInfo("hole", "O", blocking=False, deadly=True, color=(231, 100, 50))
EXIT = TileInfo("exit", "E", blocking=False, deadly=False, color=(0, 255, 0))
ROCK = TileInfo("rock", "*", blocking=True, deadly=False, color=(150, 150, 150))
