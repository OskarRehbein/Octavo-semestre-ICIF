from maze_lab.config import WALL, FLOOR, HOLE, EXIT, ROCK


class Maze:
    def __init__(self, grid: list[list[str]], start: tuple[int, int]):
        self.grid = grid
        self.start = start  # Posición inicial del robot (x, y)

        # Un diccionario útil para traducir símbolos a objetos TileInfo
        self.tiles = {
            WALL.symbol: WALL,
            FLOOR.symbol: FLOOR,
            HOLE.symbol: HOLE,
            EXIT.symbol: EXIT,
            ROCK.symbol: ROCK,
        }

    def symbol_at(self, position: tuple[int, int]) -> str:
        """Retorna el símbolo en una coordenada específica."""
        x, y = position
        # Retorna un muro por defecto si se sale de los límites
        if 0 <= y < len(self.grid) and 0 <= x < len(self.grid[0]):
            return self.grid[y][x]
        return WALL.symbol

    def tile_at(self, position: tuple[int, int]):
        """Retorna el objeto TileInfo correspondiente a la coordenada."""
        symbol = self.symbol_at(position)
        return self.tiles.get(symbol, WALL)

    def is_walkable(self, position: tuple[int, int]) -> bool:
        """Verifica si la celda no está bloqueada (ej: muros, cajas)."""
        return not self.tile_at(position).blocking

    def is_safe(self, position: tuple[int, int]) -> bool:
        """Verifica si se puede caminar y además no es mortal (ej: hoyos)."""
        return self.is_walkable(position) and not self.tile_at(position).deadly
