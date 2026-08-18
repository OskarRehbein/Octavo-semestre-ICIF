"""Drawing of the board, the marks and the status panel.

Everything is drawn in code, there are no image files. The panel at the bottom
shows the level of the machine, how many nodes it explored to decide its last
move and how long it took: the visible evidence of what minimax does.
"""

from typing import Sequence

import pygame

from .board import CROSS, EMPTY, State, winning_line

BACKGROUND = (14, 13, 18)
GRID = (58, 54, 70)
CROSS_COLOR = (92, 208, 232)
CIRCLE_COLOR = (226, 158, 74)
WIN_LINE = (120, 214, 150)
HUD_BACKGROUND = (22, 20, 28)
HUD_TEXT = (206, 200, 214)
HUD_DIM = (128, 122, 140)

HUD_PADDING = 10
LINE_GAP = 4
SEPARATOR = "   "
HUD_FONT_SIZE = 16
HUD_SMALL_FONT_SIZE = 13
KEY_HINTS = (
    "click play",
    "1 easy",
    "2 medium",
    "3 hard",
    "R new game",
    "ESC quit",
)
# strings of typical length, to reserve the panel height before the game starts
HUD_SAMPLE = (
    "level hard",
    "nodes 000000",
    "time 0000 ms",
    "you play X",
    "the machine wins",
)


def hud_height(width: int, minimum: int) -> int:
    """Height the panel needs so its text is not cut off in this window."""
    font = _hud_font(HUD_FONT_SIZE)
    lines = _wrap(font, HUD_SAMPLE, width - 2 * HUD_PADDING) + _wrap(
        font, KEY_HINTS, width - 2 * HUD_PADDING
    )
    return max(minimum, len(lines) * (font.get_linesize() + LINE_GAP) + HUD_PADDING)


def _hud_font(size: int) -> pygame.font.Font:
    return pygame.font.SysFont("dejavusansmono,monospace", size)


class Renderer:
    def __init__(self, surface: pygame.Surface, config):
        self.surface = surface
        self.config = config
        self.cell = config.cell_size
        self.font = _hud_font(HUD_FONT_SIZE)
        self.small_font = _hud_font(HUD_SMALL_FONT_SIZE)

    def draw(self, state: State, status: Sequence[str]) -> None:
        self.surface.fill(BACKGROUND)
        self._draw_grid()
        for index, mark in enumerate(state.squares):
            if mark != EMPTY:
                self._draw_mark(index, mark)
        self._draw_winning_line(state)
        self._draw_hud(status)

    def square_rect(self, index: int) -> pygame.Rect:
        """The square of a cell, both to draw it and to read clicks on it."""
        row, column = divmod(index, 3)
        return pygame.Rect(column * self.cell, row * self.cell, self.cell, self.cell)

    def square_at(self, position: tuple[int, int]) -> int | None:
        """Index of the square under the mouse, or None if the click was outside."""
        x, y = position
        if y >= 3 * self.cell:
            return None
        return (y // self.cell) * 3 + x // self.cell

    def _draw_grid(self) -> None:
        length = 3 * self.cell
        for i in (1, 2):
            offset = i * self.cell
            pygame.draw.line(self.surface, GRID, (offset, 0), (offset, length), 3)
            pygame.draw.line(self.surface, GRID, (0, offset), (length, offset), 3)

    def _draw_mark(self, index: int, mark: str) -> None:
        rect = self.square_rect(index).inflate(-self.cell // 3, -self.cell // 3)
        width = max(4, self.cell // 14)
        if mark == CROSS:
            pygame.draw.line(self.surface, CROSS_COLOR, rect.topleft, rect.bottomright, width)
            pygame.draw.line(self.surface, CROSS_COLOR, rect.bottomleft, rect.topright, width)
        else:
            pygame.draw.circle(
                self.surface, CIRCLE_COLOR, rect.center, rect.width // 2, width
            )

    def _draw_winning_line(self, state: State) -> None:
        line = winning_line(state)
        if line is None:
            return
        start = self.square_rect(line[0]).center
        end = self.square_rect(line[2]).center
        pygame.draw.line(self.surface, WIN_LINE, start, end, max(4, self.cell // 18))

    def _draw_hud(self, status: Sequence[str]) -> None:
        """The text is split into lines that fit the width of the window."""
        top = 3 * self.cell
        rect = pygame.Rect(0, top, self.surface.get_width(), self.config.hud_height)
        pygame.draw.rect(self.surface, HUD_BACKGROUND, rect)
        pygame.draw.line(self.surface, GRID, rect.topleft, rect.topright)

        available = rect.width - 2 * HUD_PADDING
        groups = ((HUD_TEXT, status), (HUD_DIM, KEY_HINTS))
        for font in (self.font, self.small_font):
            lines = [
                (color, line)
                for color, parts in groups
                for line in _wrap(font, parts, available)
            ]
            step = font.get_linesize() + LINE_GAP
            if len(lines) * step <= rect.height - HUD_PADDING:
                break

        y = top + HUD_PADDING
        for color, line in lines:
            self.surface.blit(font.render(line, True, color), (HUD_PADDING, y))
            y += step


def _wrap(font: pygame.font.Font, parts: Sequence[str], max_width: int) -> list[str]:
    """Packs the texts into lines, breaking before going over the width."""
    lines: list[str] = []
    current = ""
    for part in parts:
        candidate = f"{current}{SEPARATOR}{part}" if current else part
        if current and font.size(candidate)[0] > max_width:
            lines.append(current)
            current = part
        else:
            current = candidate
    if current:
        lines.append(current)
    return lines
