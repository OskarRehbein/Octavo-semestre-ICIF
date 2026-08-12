import pygame
from maze_lab import search


class Game:
    """
    Capa intermedia entre la lógica pura (search.py, maze.py, agent.py) y
    el dibujo (renderer.py). Se encarga de:
      - Ejecutar BFS/DFS cuando se presiona B o P.
      - Guardar 'expanded' y 'path' para que el renderer los pinte.
      - Animar al robot recorriendo el 'path' cuando se presiona ESPACIO.
    """

    def __init__(self, maze, agent, renderer):
        self.maze = maze
        self.agent = agent
        self.renderer = renderer

        # Resultado de la última búsqueda ejecutada (B o P)
        self.path: list[tuple[int, int]] = []
        self.expanded: list[tuple[int, int]] = []
        self.last_algorithm: str | None = None

        # Estado de la animación de "caminar el camino" (tecla ESPACIO)
        self.walking = False
        self.walk_index = 0
        self.walk_delay_ms = 120  # cuánto espera entre cada paso de la animación
        self.walk_timer = 0

    # --- Búsquedas -------------------------------------------------------

    def run_bfs(self):
        self.path, self.expanded = search.bfs(
            self.maze, self.agent.start_position, self.maze.exit
        )
        self.last_algorithm = "BFS"
        self._reset_walk()
        self._print_stats()

    def run_dfs(self):
        self.path, self.expanded = search.dfs(
            self.maze, self.agent.start_position, self.maze.exit
        )
        self.last_algorithm = "DFS"
        self._reset_walk()
        self._print_stats()

    def _print_stats(self):
        if self.path:
            print(
                f"{self.last_algorithm}: {len(self.expanded)} celdas expandidas, "
                f"camino de {len(self.path) - 1} pasos"
            )
        else:
            print(
                f"{self.last_algorithm}: no se encontró camino ({len(self.expanded)} celdas expandidas)"
            )

    # --- Animación del recorrido ------------------------------------------

    def start_walk(self):
        """Prepara al robot para recorrer, paso a paso, el último camino calculado."""
        if not self.path:
            print("No hay camino calculado todavía. Presiona B o P primero.")
            return

        self.agent.position = self.agent.start_position
        self.agent.steps = 0
        self.walking = True
        self.walk_index = 0
        self.walk_timer = 0

    def _reset_walk(self):
        self.walking = False
        self.walk_index = 0

    def update(self, dt_ms: int):
        """Avanza la animación un paso cuando corresponde. Se llama una vez por frame."""
        if not self.walking:
            return

        self.walk_timer += dt_ms
        if self.walk_timer < self.walk_delay_ms:
            return
        self.walk_timer = 0

        self.walk_index += 1
        if self.walk_index >= len(self.path):
            self.walking = False
            print("El robot llegó a la salida siguiendo el camino encontrado.")
            return

        self.agent.position = self.path[self.walk_index]
        self.agent.steps += 1

    # --- Entrada de teclado ------------------------------------------------

    def handle_key(self, key) -> bool:
        """
        Procesa una tecla relacionada a la búsqueda.
        Retorna True si la tecla fue manejada aquí (para que main.py sepa
        que no debe interpretarla también como movimiento).
        """
        if key == pygame.K_b:
            self.run_bfs()
            return True
        if key == pygame.K_p:
            self.run_dfs()
            return True
        if key == pygame.K_SPACE:
            self.start_walk()
            return True
        return False
