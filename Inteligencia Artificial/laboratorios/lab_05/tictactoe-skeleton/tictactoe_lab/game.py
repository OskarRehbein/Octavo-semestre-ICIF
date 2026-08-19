"""Main loop: turns, mouse and level switching.

The level is just a string handed over to `choose_move`; how much it searches, or
whether it changes anything at all, is decided inside `minimax.py`.
"""

from dataclasses import dataclass, replace

import pygame

from .board import (
    CROSS,
    EMPTY,
    INITIAL_STATE,
    State,
    is_terminal,
    player,
    result,
    winner,
)
from .minimax import Stats, choose_move
from .renderer import Renderer, hud_height

LEVELS = ("easy", "medium", "hard")
LEVEL_KEYS = dict(zip((pygame.K_1, pygame.K_2, pygame.K_3), LEVELS))

MACHINE_DELAY = 350  # ms before the machine answers, so the turn is noticeable


@dataclass(frozen=True)
class GameConfig:
    cell_size: int = 140
    hud_height: int = 64
    fps: int = 60
    level: str = "hard"
    human: str = CROSS  # CROSS opens the game; with CIRCLE the machine opens

    @property
    def window_size(self) -> tuple[int, int]:
        return (3 * self.cell_size, 3 * self.cell_size + self.hud_height)


class Game:
    def __init__(self, config: GameConfig):
        pygame.init()
        pygame.display.set_caption("Tic-tac-toe — minimax")
        # the panel grows if the window is narrow and the text needs more lines
        self.config = replace(
            config,
            hud_height=hud_height(3 * config.cell_size, config.hud_height),
        )
        self.screen = pygame.display.set_mode(self.config.window_size)
        self.clock = pygame.time.Clock()
        self.renderer = Renderer(self.screen, self.config)
        self.level = config.level
        self.new_game()

    def new_game(self) -> None:
        self.state: State = INITIAL_STATE
        self.stats: Stats | None = None
        self.thinking = False
        self.last_move_at = pygame.time.get_ticks()

    def run(self) -> None:
        running = True
        while running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    running = False
                elif event.type == pygame.KEYDOWN:
                    running = self.on_key(event.key)
                elif event.type == pygame.MOUSEBUTTONDOWN:
                    self.on_click(event.pos)
            self.draw()
            self.advance_machine()
            self.clock.tick(self.config.fps)
        pygame.quit()

    def on_key(self, key: int) -> bool:
        """Returns False when the window has to be closed."""
        if key == pygame.K_ESCAPE:
            return False
        if key == pygame.K_r:
            self.new_game()
        elif key in LEVEL_KEYS:
            self.level = LEVEL_KEYS[key]
            self.new_game()
        return True

    def on_click(self, position: tuple[int, int]) -> None:
        if self.thinking or is_terminal(self.state):
            return
        if player(self.state) != self.config.human:
            return
        square = self.renderer.square_at(position)
        if square is not None and self.state.squares[square] == EMPTY:
            self.play(square)

    def advance_machine(self) -> None:
        """Waits a bit, says it is thinking, and only then searches for a move.

        The search is synchronous and with the full tree it can take close to a
        second, so the work is split across two frames: the first one draws
        "thinking" and the next one calls minimax.
        """
        if is_terminal(self.state) or player(self.state) == self.config.human:
            return
        if self.thinking:
            move, self.stats = choose_move(self.state, self.level)
            self.thinking = False
            self.play(move)
        elif pygame.time.get_ticks() - self.last_move_at >= MACHINE_DELAY:
            self.thinking = True

    def play(self, square: int) -> None:
        self.state = result(self.state, square)
        self.last_move_at = pygame.time.get_ticks()

    @property
    def message(self) -> str:
        if is_terminal(self.state):
            who = winner(self.state)
            if who is None:
                return "draw: R for another game"
            if who == self.config.human:
                return "you win: R for another game"
            return "the machine wins: R for another game"
        if self.thinking:
            return "thinking..."
        if player(self.state) == self.config.human:
            return "your turn"
        return "the machine's turn"

    def draw(self) -> None:
        nodes = "-" if self.stats is None else f"{self.stats.nodes}"
        elapsed = "-" if self.stats is None else f"{self.stats.seconds * 1000:.1f} ms"
        status = [
            f"level {self.level}",
            f"you play {self.config.human}",
            f"nodes {nodes}",
            f"time {elapsed}",
            self.message,
        ]
        self.renderer.draw(self.state, status)
        pygame.display.flip()
