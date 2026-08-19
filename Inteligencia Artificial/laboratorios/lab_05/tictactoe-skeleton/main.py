"""Entry point: tic-tac-toe against a machine that plays with minimax."""

import argparse

from tictactoe_lab import CIRCLE, CROSS, LEVELS, Game, GameConfig


def parse_args() -> GameConfig:
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument(
        "--level", choices=LEVELS, default="hard", help="level of the machine"
    )
    parser.add_argument(
        "--first",
        choices=("human", "machine"),
        default="human",
        help="who plays X and opens the game",
    )
    parser.add_argument("--cell", type=int, default=140, help="pixels per square")
    args = parser.parse_args()
    return GameConfig(
        cell_size=args.cell,
        level=args.level,
        human=CROSS if args.first == "human" else CIRCLE,
    )


if __name__ == "__main__":
    Game(parse_args()).run()
