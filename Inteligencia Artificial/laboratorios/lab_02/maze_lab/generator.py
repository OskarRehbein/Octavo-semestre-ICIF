import random
from dataclasses import dataclass
from maze_lab.config import WALL, FLOOR, EXIT, HOLE, ROCK


@dataclass
class Room:
    x: int
    y: int
    w: int
    h: int

    @property
    def center(self) -> tuple[int, int]:
        """Calcula el centro matemático de la sala para conectar pasillos."""
        return (self.x + self.w // 2, self.y + self.h // 2)

    def intersects(self, other: "Room") -> bool:
        """
        Verifica si esta sala choca con otra.
        Los '+ 1' y '- 1' expanden la 'caja de colisión' (hitbox) de la sala imaginaria.
        Esto garantiza que siempre quede al menos 1 muro de separación entre salas.
        """
        return (
            self.x - 1 <= other.x + other.w
            and self.x + self.w + 1 >= other.x
            and self.y - 1 <= other.y + other.h
            and self.y + self.h + 1 >= other.y
        )


class MazeGenerator:
    def __init__(self, width: int = 40, height: int = 40):
        self.width = width
        self.height = height
        self.grid = [
            [WALL.symbol for _ in range(self.width)] for _ in range(self.height)
        ]
        self.rooms: list[Room] = []

    def _dig(self, x: int, y: int):
        """Convierte en piso, pero NUNCA toca los bordes absolutos del mapa."""
        if 0 < y < self.height - 1 and 0 < x < self.width - 1:
            self.grid[y][x] = FLOOR.symbol

    def _create_room(self, room: Room):
        """Esculpe el interior de la sala en la matriz."""
        for y in range(room.y, room.y + room.h):
            for x in range(room.x, room.x + room.w):
                self._dig(x, y)

    def _dig_corridor(self, x1: int, y1: int, x2: int, y2: int):
        """Traza un pasillo recto en 'L' entre dos puntos."""
        x, y = x1, y1

        # Excavamos horizontalmente
        while x != x2:
            self._dig(x, y)
            x += 1 if x < x2 else -1

        # Excavamos verticalmente
        while y != y2:
            self._dig(x, y)
            y += 1 if y < y2 else -1

    def _is_corridor_safe(
        self, cx1: int, cy1: int, cx2: int, cy2: int, horizontal_first: bool
    ) -> bool:
        """
        Convierte el pasillo en 'cajas de colisión' temporales y verifica que
        no choquen con ninguna sala antigua, garantizando que no se deformen.
        """
        # Ignoramos la última sala creada (self.rooms[-1]) porque es de donde sale el pasillo.
        # Tampoco verificamos la sala nueva, porque aún no la agregamos a self.rooms.
        rooms_to_check = self.rooms[:-1]

        # Simulamos los dos tramos del pasillo en 'L'
        if horizontal_first:
            seg1 = Room(min(cx1, cx2), cy1, abs(cx1 - cx2) + 1, 1)
            seg2 = Room(cx2, min(cy1, cy2), 1, abs(cy1 - cy2) + 1)
        else:
            seg1 = Room(cx1, min(cy1, cy2), 1, abs(cy1 - cy2) + 1)
            seg2 = Room(min(cx1, cx2), cy2, abs(cx1 - cx2) + 1, 1)

        # Si el pasillo choca con alguna sala vieja, es un mal trayecto
        for old_room in rooms_to_check:
            if seg1.intersects(old_room) or seg2.intersects(old_room):
                return False

        return True

    def generate_dungeon(
        self, max_rooms: int = 15, min_size: int = 4, max_size: int = 8
    ):
        """Genera el laberinto validando salas y pasillos antes de construir."""
        for _ in range(max_rooms):
            # 1. Generamos medidas al azar
            w = random.randint(min_size, max_size)
            h = random.randint(min_size, max_size)
            x = random.randint(1, self.width - w - 1)
            y = random.randint(1, self.height - h - 1)

            new_room = Room(x, y, w, h)

            # 2. Verificamos si la sala choca con otra
            failed = False
            for other_room in self.rooms:
                if new_room.intersects(other_room):
                    failed = True
                    break

            if failed:
                continue  # Sala descartada, intentamos otra

            # Si es la primera sala de todo el mapa, la construimos de inmediato
            if not self.rooms:
                self._create_room(new_room)
                self.rooms.append(new_room)
                continue

            # 3. ¡LA MAGIA! Validamos los pasillos antes de tocar la matriz
            prev_room = self.rooms[-1]
            cx1, cy1 = new_room.center
            cx2, cy2 = prev_room.center

            safe_h = self._is_corridor_safe(cx1, cy1, cx2, cy2, horizontal_first=True)
            safe_v = self._is_corridor_safe(cx1, cy1, cx2, cy2, horizontal_first=False)

            # Decidimos qué pasillo usar basándonos en la seguridad
            if safe_h and safe_v:
                use_h = random.choice(
                    [True, False]
                )  # Si ambos son seguros, elegimos al azar
            elif safe_h:
                use_h = True
            elif safe_v:
                use_h = False
            else:
                # Si AMBOS pasillos chocarían con una sala vieja,
                # rechazamos la generación de la sala completa para evitar desastres.
                continue

            # 4. Construcción oficial (ahora que sabemos que todo es seguro)
            self._create_room(new_room)

            if use_h:
                self._dig_corridor(cx1, cy1, cx2, cy1)
                self._dig_corridor(cx2, cy1, cx2, cy2)
            else:
                self._dig_corridor(cx1, cy1, cx1, cy2)
                self._dig_corridor(cx1, cy2, cx2, cy2)

            self.rooms.append(new_room)

        # Al final de def generate_dungeon(...):
        if self.rooms:
            self.add_obstacles(num_obstacles=25)

    def print_console(self, agent_pos: tuple[int, int] | None = None):
        """Dibuja el laberinto y superpone al agente si se proporciona su posición."""
        for y, row in enumerate(self.grid):
            row_str = ""
            for x, cell in enumerate(row):
                # Si la coordenada actual es la del agente, dibujamos un '@'
                if agent_pos and (x, y) == agent_pos:
                    row_str += "@"
                else:
                    row_str += cell
            print(row_str)

    def _is_reachable(self, start: tuple[int, int], goal: tuple[int, int]) -> bool:
        """
        Relleno por inundación (BFS) para verificar si hay camino desde 'start' hasta 'goal'.
        """
        # Si por alguna razón el inicio o el fin no son piso o salida, retornamos False
        if self.grid[start[1]][start[0]] not in (
            FLOOR.symbol,
            EXIT.symbol,
        ) or self.grid[goal[1]][goal[0]] not in (FLOOR.symbol, EXIT.symbol):
            return False

        visited = set()
        visited.add(start)
        queue = [start]

        # Direcciones: Arriba, Abajo, Izquierda, Derecha
        directions = [(0, -1), (0, 1), (-1, 0), (1, 0)]

        while queue:
            # Sacamos el primer elemento de la cola
            current_x, current_y = queue.pop(0)

            # Si llegamos a la meta, ¡el camino existe!
            if (current_x, current_y) == goal:
                return True

            # Revisamos los 4 vecinos
            for dx, dy in directions:
                nx, ny = current_x + dx, current_y + dy

                # Verificamos que no nos salgamos de la matriz
                if 0 <= ny < self.height and 0 <= nx < self.width:
                    # Solo caminamos por celdas SEGURAS (piso o salida)
                    # Excluimos muros (#), hoyos (O) y rocas (*)
                    symbol = self.grid[ny][nx]
                    if (
                        symbol in (FLOOR.symbol, EXIT.symbol)
                        and (nx, ny) not in visited
                    ):
                        visited.add((nx, ny))
                        queue.append((nx, ny))

        # Si la cola se vacía y no llegamos a la meta, el camino está bloqueado
        return False

    def add_obstacles(self, num_obstacles: int = 20):
        """Esparce obstáculos al azar asegurando que el laberinto tenga solución."""
        # 1. Definimos la entrada (centro de la primera sala) y la salida (centro de la última)
        self.start_pos = self.rooms[0].center
        self.exit_pos = self.rooms[-1].center

        # Colocamos la salida físicamente en el mapa
        self.grid[self.exit_pos[1]][self.exit_pos[0]] = EXIT.symbol

        # 2. Recopilamos EXCLUSIVAMENTE las coordenadas del interior de las salas
        floor_cells = []
        for room in self.rooms:
            # Recorremos solo el ancho y alto de cada sala
            for y in range(room.y, room.y + room.h):
                for x in range(room.x, room.x + room.w):
                    # Verificamos que sea piso y no sea la posición de inicio
                    if self.grid[y][x] == FLOOR.symbol and (x, y) != self.start_pos:
                        floor_cells.append((x, y))

        # Mezclamos las celdas disponibles para que sea aleatorio
        random.shuffle(floor_cells)

        placed = 0

        for x, y in floor_cells:
            if placed >= num_obstacles:
                break

            # Elegimos al azar si poner un hoyo o una roca
            obstacle = HOLE.symbol if random.choice([True, False]) else ROCK.symbol

            # Ponemos el obstáculo temporalmente
            self.grid[y][x] = obstacle

            # Revisamos si la salida sigue siendo alcanzable
            if self._is_reachable(self.start_pos, self.exit_pos):
                placed += 1  # Es seguro, lo dejamos
            else:
                self.grid[y][x] = FLOOR.symbol  # ¡Nos bloqueó! Deshacemos la jugada

    def get_grid(self) -> list[list[str]]:
        """Devuelve la matriz terminada."""
        return self.grid


# Ejecucion por consola para debugging
if __name__ == "__main__":
    from maze import Maze
    from agent import Agent, MoveResult

    # 1. Generar el plano del nivel
    print("Generando laberinto, por favor espera...")
    gen = MazeGenerator(width=40, height=40)
    gen.generate_dungeon()
    gen.add_obstacles(num_obstacles=20)

    # 2. Inicializar los objetos lógicos
    # Pasamos la matriz cruda y la posición de inicio al gestor del mapa
    mapa = Maze(grid=gen.get_grid(), start=gen.start_pos)

    # Creamos al robot en esa misma posición inicial
    robot = Agent(start_position=gen.start_pos)

    # 3. El ciclo principal del juego (El Controlador)
    while True:
        # Imprimir el estado actual
        print("\n" * 2)  # Separador visual en la consola
        gen.print_console(agent_pos=robot.position)
        print(f"Pasos: {robot.steps} | Caídas: {robot.falls}")

        # Escuchar al jugador
        tecla = input("Mover (w/a/s/d) o 'q' para salir: ").lower()

        if tecla == "q":
            print("Saliendo de la simulación...")
            break

        # Traducir la tecla a la dirección que entiende el agente
        direccion = None
        if tecla == "w":
            direccion = "up"
        elif tecla == "s":
            direccion = "down"
        elif tecla == "a":
            direccion = "left"
        elif tecla == "d":
            direccion = "right"

        # Ejecutar el movimiento y evaluar las consecuencias
        if direccion:
            resultado = robot.move(mapa, direccion)

            if resultado == MoveResult.BLOCKED:
                print(">>> Has chocado con un muro. <<<")
            elif resultado == MoveResult.FELL:
                print(">>> Te has caido en un muro <<<")
            elif resultado == MoveResult.ESCAPED:
                print(">>> Lograste llegar a la salida <<<")
                break
