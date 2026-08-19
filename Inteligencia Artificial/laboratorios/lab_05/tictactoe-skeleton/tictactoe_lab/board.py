"""Tic-tac-toe as an adversarial search problem.

This is the formalism from the lecture turned into code: a game is defined by its
initial state plus `player`, `actions`, `result`, `is_terminal` and `utility`.
There is no minimax and no pygame here, only the board and its rules.

CROSS is MAX and CIRCLE is MIN, so utility is always measured from the point of
view of CROSS: +1 if CROSS wins, -1 if CIRCLE wins, 0 on a draw.
"""

from dataclasses import dataclass

CROSS = "X"
CIRCLE = "O"
EMPTY = " "

# the eight ways to win, over the squares numbered 0..8
LINES = (
    (0, 1, 2),
    (3, 4, 5),
    (6, 7, 8),
    (0, 3, 6),
    (1, 4, 7),
    (2, 5, 8),
    (0, 4, 8),
    (2, 4, 6),
)


@dataclass(frozen=True)
class State:
    """The nine squares, left to right and top to bottom.

    It is immutable: `result` does not modify the state, it returns a new one.
    That property is what makes the minimax recursion safe, since it walks up and
    down the tree without having to undo moves.
    """

    squares: tuple[str, ...] = (EMPTY,) * 9

    def __str__(self) -> str:
        rows = ["|".join(self.squares[i : i + 3]) for i in range(0, 9, 3)]
        return "\n-+-+-\n".join(rows)


INITIAL_STATE = State()


def player(state: State) -> str:
    """Whose turn it is. CROSS always opens the game."""
    crosses = state.squares.count(CROSS)
    circles = state.squares.count(CIRCLE)
    return CROSS if crosses == circles else CIRCLE


def actions(state: State) -> tuple[int, ...]:
    """The legal moves: the indices of the empty squares."""
    return tuple(i for i, square in enumerate(state.squares) if square == EMPTY)


def result(state: State, action: int) -> State:
    """The state left after the player to move puts a mark on `action`."""
    squares = list(state.squares)
    squares[action] = player(state)
    return State(tuple(squares))


def winning_line(state: State) -> tuple[int, int, int] | None:
    """The line with three equal marks, or None if there is none yet."""
    for line in LINES:
        a, b, c = line
        squares = state.squares
        if squares[a] != EMPTY and squares[a] == squares[b] == squares[c]:
            return line
    return None


def winner(state: State) -> str | None:
    """CROSS, CIRCLE, or None if nobody has won."""
    line = winning_line(state)
    return None if line is None else state.squares[line[0]]


def is_terminal(state: State) -> bool:
    """A state is terminal if somebody won or there are no squares left."""
    return winner(state) is not None or EMPTY not in state.squares


def utility(state: State) -> int:
    """Utility of a terminal state for MAX (CROSS).

    The lecture drew the tree with +-100; here it is +-1. The scale does not
    matter, the order does: CROSS wins > draw > CIRCLE wins.
    """
    who = winner(state)
    if who == CROSS:
        return 1
    if who == CIRCLE:
        return -1
    return 0
