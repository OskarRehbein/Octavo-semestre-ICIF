"""Minimax over tic-tac-toe. YOUR WORK GOES HERE: the only file you edit.

Two functions to complete:

- `minimax`     the recursive definition from the lecture.
- `choose_move` the move the machine picks.

Everything you need from the board is already in `board.py`:

    player(state)          -> CROSS or CIRCLE, whose turn it is
    actions(state)         -> indices of the empty squares: the legal moves
    result(state, action)  -> the new state, leaving the old one untouched
    is_terminal(state)     -> True if somebody won or no squares are left
    utility(state)         -> +1 CROSS wins, -1 CIRCLE wins, 0 draw

CROSS is MAX and CIRCLE is MIN: utility is always measured from CROSS.

Until you implement them the game still runs, but the machine plays the first
empty square: beating it is easy.
"""

import time
from dataclasses import dataclass

from .board import CROSS, State, actions, is_terminal, player, result, utility, CIRCLE


@dataclass
class Stats:
    """What it cost to decide the last move. The game panel displays it."""

    nodes: int = 0
    seconds: float = 0.0


def minimax(state: State, stats: Stats) -> int:
    """Minimax value of the state: +1 CROSS wins, -1 CIRCLE wins, 0 draw.

    TODO 1: implement the recursive definition from the lecture.

        MINIMAX(s):
          if TERMINAL(s):     return UTILITY(s)
          if PLAYER(s) = MAX: v <- -inf; v <- max(v, MINIMAX(RESULT(s, a))) for each a
          if PLAYER(s) = MIN: v <- +inf; v <- min(v, MINIMAX(RESULT(s, a))) for each a

    Add 1 to `stats.nodes` on every call: that counter is what the panel shows
    and what goes into the report.
    """
    if is_terminal: 
        return utility(state)

    if player(state) == max:
        v = -1000000
        for i in actions(state):
            v = max(v, minimax(result(state, i)))
        Stats.nodes =+ 1
        return v

    if player(state) == min:
        v = 1000000
        for e in actions(state):
            v = min(v, minimax(result(state, e)))
        Stats.nodes =+ 1
        return v


    return v


def choose_move(state: State, level: str = "hard") -> tuple[int, Stats]:
    """The move the machine picks for the player to move, and what it cost.

    TODO 2: try every legal action and keep the best one.

    - The value of an action `a` is `minimax(result(state, a), stats)`.
    - CROSS (MAX) keeps the highest value, CIRCLE (MIN) the lowest one.
    - Return `(move, stats)`; the elapsed time is already measured below.

    `level` is only used by the optional extension in the README. While you
    ignore it, the three levels play exactly the same.
    """
    stats = Stats()
    started = time.perf_counter()

    """if player(state) == max:
        best_move = minimax(result(state), stats)
        return best_move

    if player(state) == min:
        best_move = minimax(result(state), stats)
        return best_move"""
    """for i in actions(state):
        if CROSS:
            best_move = minimax(result(state), stats)
        if CIRCLE:
            best_move = minimax(result(state), stats)"""
    
    
    best_move = actions(state)[0]  # placeholder: the first empty square
    
    stats.seconds = time.perf_counter() - started
    return best_move, stats
