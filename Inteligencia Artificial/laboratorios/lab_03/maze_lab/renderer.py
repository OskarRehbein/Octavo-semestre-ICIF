import pygame
from maze_lab.maze import Maze
from maze_lab.agent import Agent

# Colores para la visualización de la búsqueda
EXPANDED_COLOR = (80, 80, 200)  # celdas que la búsqueda exploró
PATH_COLOR = (255, 165, 0)  # camino final encontrado


class Renderer:
    def __init__(self, tile_size: int = 15):
        self.tile_size = tile_size
        self.screen = None
        self.font = None

    def init_pygame(self, width_cells: int, height_cells: int):
        """Inicializa la ventana de pygame basada en el tamaño del laberinto."""
        pygame.init()

        # Calculamos el tamaño en píxeles multiplicando celdas por el tamaño del cuadro
        width_px = width_cells * self.tile_size
        height_px = height_cells * self.tile_size

        # Dejamos un margen de 40 píxeles abajo para el texto de la interfaz (HUD)
        self.screen = pygame.display.set_mode((width_px, height_px + 40))
        pygame.display.set_caption("Laberinto IA - Laboratorio 3")

        # Fuente para los textos (Pasos, Caídas)
        self.font = pygame.font.SysFont(None, 24)

    def draw(self, maze: Maze, agent: Agent, expanded=None, path=None):
        """Dibuja el mapa, la búsqueda (si hay) y al agente en cada frame."""
        if not self.screen:
            return

        # Limpiamos la pantalla pintándola de negro
        self.screen.fill((0, 0, 0))

        # 1. Dibujar el laberinto
        for y in range(len(maze.grid)):
            for x in range(len(maze.grid[0])):
                # Le pedimos al mapa el objeto TileInfo para saber su color
                tile = maze.tile_at((x, y))

                rect = pygame.Rect(
                    x * self.tile_size,
                    y * self.tile_size,
                    self.tile_size,
                    self.tile_size,
                )
                pygame.draw.rect(self.screen, tile.color, rect)

        # 2. Dibujar las celdas expandidas por la última búsqueda (debajo del camino)
        if expanded:
            for x, y in expanded:
                rect = pygame.Rect(
                    x * self.tile_size,
                    y * self.tile_size,
                    self.tile_size,
                    self.tile_size,
                )
                pygame.draw.rect(self.screen, EXPANDED_COLOR, rect, width=0)
                pygame.draw.rect(self.screen, (0, 0, 0), rect, width=1)

        # 3. Dibujar el camino encontrado (encima de las expandidas)
        if path:
            for x, y in path:
                rect = pygame.Rect(
                    x * self.tile_size,
                    y * self.tile_size,
                    self.tile_size,
                    self.tile_size,
                )
                pygame.draw.rect(self.screen, PATH_COLOR, rect)

        # 4. Dibujar al agente (siempre encima de todo lo demás)
        agent_x, agent_y = agent.position
        agent_rect = pygame.Rect(
            agent_x * self.tile_size,
            agent_y * self.tile_size,
            self.tile_size,
            self.tile_size,
        )
        pygame.draw.rect(self.screen, (255, 255, 0), agent_rect)

        # 5. Dibujar la interfaz de texto (HUD)
        if self.font:
            hud_text = f"Pasos: {agent.steps} | Caidas: {agent.falls}"
            text_surface = self.font.render(hud_text, True, (255, 255, 255))
            self.screen.blit(text_surface, (10, len(maze.grid) * self.tile_size + 10))

        # 6. Actualizar la pantalla de Pygame
        pygame.display.flip()

    def quit(self):
        """Cierra pygame de forma segura."""
        pygame.quit()
