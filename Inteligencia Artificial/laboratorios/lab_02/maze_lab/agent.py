from enum import Enum


class MoveResult(Enum):
    MOVED = "moved"
    BLOCKED = "blocked"
    FELL = "fell"
    ESCAPED = "escaped"


class Agent:
    # Diccionario estático con pura matemática (x, y)
    DIRECTIONS = {
        "up": (0, -1),
        "down": (0, 1),
        "left": (-1, 0),
        "right": (1, 0),
    }  ## Es mas simple de lo que pensaba, a veces me complico cuando pienso en como programar algo

    def __init__(self, start_position: tuple[int, int]):
        self.start_position = start_position
        self.position = start_position
        self.steps = 0
        self.falls = 0

    def move(self, maze, direction: str) -> MoveResult:
        # Extraemos cuánto sumar a X y a Y
        dx, dy = self.DIRECTIONS[direction]

        # Calculamos la nueva coordenada (x + dx, y + dy)
        target_x = self.position[0] + dx
        target_y = self.position[1] + dy
        target = (target_x, target_y)

        # 1. ¿Está bloqueado? (Muros, cajas)
        if not maze.is_walkable(target):
            return MoveResult.BLOCKED

        # Si no está bloqueado, el agente avanza
        self.position = target
        self.steps += 1

        # 2. ¿Es mortal? (Hoyos)
        if maze.tile_at(target).deadly:
            self.falls += 1
            self.position = self.start_position  # El castigo es volver al inicio
            return MoveResult.FELL

        # 3. ¿Es la salida? (Asumiendo que definiste EXIT en tu config)
        # if maze.symbol_at(target) == "E":
        #     return MoveResult.ESCAPED

        # 4. Movimiento normal
        return MoveResult.MOVED
