import pygame
from maze_lab.maze import Maze
from maze_lab.agent import Agent


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
        pygame.display.set_caption("Laberinto IA - Laboratorio 2")

        # Fuente para los textos (Pasos, Caídas)
        self.font = pygame.font.SysFont(None, 24)

    def draw(self, maze: Maze, agent: Agent):
        """Dibuja el mapa y el agente en cada frame."""
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

        # 2. Dibujar al agente
        agent_x, agent_y = agent.position
        agent_rect = pygame.Rect(
            agent_x * self.tile_size,
            agent_y * self.tile_size,
            self.tile_size,
            self.tile_size,
        )
        # Dibujamos al agente de un color llamativo, como amarillo
        pygame.draw.rect(self.screen, (255, 255, 0), agent_rect)

        # 3. Dibujar la interfaz de texto (HUD)
        if self.font:
            hud_text = f"Pasos: {agent.steps} | Caidas: {agent.falls}"
            text_surface = self.font.render(hud_text, True, (255, 255, 255))
            self.screen.blit(text_surface, (10, len(maze.grid) * self.tile_size + 10))

        # 4. Actualizar la pantalla de Pygame
        pygame.display.flip()

    def quit(self):
        """Cierra pygame de forma segura."""
        pygame.quit()


# Codigo para verificar comportamiento
if __name__ == "__main__":
    import sys
    from generator import MazeGenerator
    # Asegúrate de tener los imports de Maze y Agent que ya pusimos arriba

    # 1. Generar los datos lógicos (como hicimos en la consola)
    print("Generando mapa visual...")
    gen = MazeGenerator(width=40, height=40)
    gen.generate_dungeon()
    gen.add_obstacles(num_obstacles=20)

    mapa = Maze(grid=gen.get_grid(), start=gen.start_pos)
    robot = Agent(start_position=gen.start_pos)

    # 2. Iniciar el renderizador
    # Usamos tile_size=15 para que quepa bien en la pantalla (40x15 = 600px)
    renderer = Renderer(tile_size=15)
    renderer.init_pygame(width_cells=40, height_cells=40)

    # 3. Bucle temporal básico para mantener la ventana abierta
    corriendo = True
    while corriendo:
        # Pygame necesita procesar eventos para no congelarse
        for evento in pygame.event.get():
            if evento.type == pygame.QUIT:  # Si le das a la 'X' de la ventana
                corriendo = False

        # Dibujar nuestro mapa estático (el robot no se moverá aquí)
        renderer.draw(mapa, robot)

    # Cerrar todo limpiamente al salir del bucle
    renderer.quit()
    sys.exit()
