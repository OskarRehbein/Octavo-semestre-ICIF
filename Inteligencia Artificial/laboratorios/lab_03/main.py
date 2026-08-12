import pygame
import sys
from maze_lab.generator import MazeGenerator
from maze_lab.maze import Maze
from maze_lab.agent import Agent, MoveResult
from maze_lab.renderer import Renderer


def main():
    # 1. Fase de Generación (Crear el mundo)
    print("Generando el laberinto...")
    gen = MazeGenerator(width=40, height=40)
    gen.generate_dungeon()
    gen.add_obstacles(num_obstacles=20)

    # 2. Fase de Inicialización Lógica (El Modelo)
    mapa = Maze(grid=gen.get_grid(), start=gen.start_pos)
    robot = Agent(start_position=gen.start_pos)

    # 3. Fase de Inicialización Gráfica (La Vista)
    renderer = Renderer(tile_size=15)
    renderer.init_pygame(width_cells=40, height_cells=40)

    # El reloj nos ayuda a controlar que el juego no consuma el 100% del procesador
    clock = pygame.time.Clock()

    print("¡Todo listo! Usa W, A, S, D o las Flechas para moverte.")
    jugando = True

    # 4. El Bucle Principal (El Controlador)
    while jugando:
        # A. Escuchar Eventos
        for evento in pygame.event.get():
            # Si el usuario cierra la ventana
            if evento.type == pygame.QUIT:
                jugando = False

            # Si el usuario presiona una tecla
            elif evento.type == pygame.KEYDOWN:
                direccion = None

                # Mapeo de controles (Soporta WASD y Flechas direccionales)
                if evento.key in (pygame.K_w, pygame.K_UP):
                    direccion = "up"
                elif evento.key in (pygame.K_s, pygame.K_DOWN):
                    direccion = "down"
                elif evento.key in (pygame.K_a, pygame.K_LEFT):
                    direccion = "left"
                elif evento.key in (pygame.K_d, pygame.K_RIGHT):
                    direccion = "right"

                # B. Ejecutar la Lógica
                if direccion:
                    resultado = robot.move(mapa, direccion)

                    if resultado == MoveResult.ESCAPED:
                        print("¡Felicidades! Lograste salir del laberinto.")
                        jugando = False  # Termina el juego al ganar
                        # Aquí en el futuro podrías mostrar una pantalla de victoria

        # C. Actualizar la Pantalla
        renderer.draw(mapa, robot)

        # Limitamos el juego a 30 fotogramas por segundo (FPS)
        clock.tick(30)

    # 5. Salida Limpia
    renderer.quit()
    sys.exit()


if __name__ == "__main__":
    main()
