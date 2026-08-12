import argparse
import random
import sys

import pygame

from maze_lab.generator import MazeGenerator
from maze_lab.maze import Maze
from maze_lab.agent import Agent, MoveResult
from maze_lab.renderer import Renderer
from maze_lab.game import Game


def main():
    # 0. Argumentos de consola (para poder reproducir el mismo laberinto)
    parser = argparse.ArgumentParser()
    parser.add_argument(
        "-seed",
        type=int,
        default=None,
        help="Semilla para reproducir el mismo laberinto",
    )
    args = parser.parse_args()

    if args.seed is not None:
        random.seed(args.seed)
        print(f"Usando semilla: {args.seed}")

    # 1. Fase de Generación (Crear el mundo)
    print("Generando el laberinto...")
    gen = MazeGenerator(width=40, height=40)
    gen.generate_dungeon()
    gen.add_obstacles(num_obstacles=20)

    # 2. Fase de Inicialización Lógica (El Modelo)
    mapa = Maze(grid=gen.get_grid(), start=gen.start_pos, exit=gen.exit_pos)
    robot = Agent(start_position=gen.start_pos)

    # 3. Fase de Inicialización Gráfica (La Vista)
    renderer = Renderer(tile_size=15)
    renderer.init_pygame(width_cells=40, height_cells=40)

    # 3.5 Capa de juego: conecta la búsqueda (search.py) con teclas y animación
    juego = Game(maze=mapa, agent=robot, renderer=renderer)

    # El reloj nos ayuda a controlar que el juego no consuma el 100% del procesador
    clock = pygame.time.Clock()

    print(
        "¡Todo listo! WASD/Flechas para moverte. B = BFS, P = DFS, ESPACIO = recorrer el camino."
    )
    jugando = True

    # 4. El Bucle Principal (El Controlador)
    while jugando:
        # dt: milisegundos desde el frame anterior, lo usa la animación de ESPACIO
        dt = clock.tick(30)

        # A. Escuchar Eventos
        for evento in pygame.event.get():
            # Si el usuario cierra la ventana
            if evento.type == pygame.QUIT:
                jugando = False

            # Si el usuario presiona una tecla
            elif evento.type == pygame.KEYDOWN:
                # Primero probamos si es una tecla de búsqueda (B, P, ESPACIO)
                if juego.handle_key(evento.key):
                    continue

                # Si no, probamos si es una tecla de movimiento manual
                direccion = None
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

        # B.5 Actualizar animaciones (recorrido del camino con ESPACIO)
        juego.update(dt)

        # C. Actualizar la Pantalla
        renderer.draw(mapa, robot, expanded=juego.expanded, path=juego.path)

    # 5. Salida Limpia
    renderer.quit()
    sys.exit()


if __name__ == "__main__":
    main()
