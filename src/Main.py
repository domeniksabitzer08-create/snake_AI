import pygame
import snakeGame

from snakeGame import Vector2D, Grid, screen_to_world_pos


import time

pygame.init()

screen = pygame.display.set_mode((500, 500))
running = True

def show_grid():
    for i in range(Grid.cell_count):
        for j in range(Grid.cell_count):
            cell = snakeGame.Parts(0, Vector2D(i*Grid.cell_size , j*Grid.cell_size))
            cell.render(screen)
            time.sleep(0.001)
            pygame.display.update()
def debug_grid_with_mouse():
    mouse_pos = pygame.mouse.get_pos()
    mouse_grid_pos = screen_to_world_pos(Vector2D(mouse_pos[0], mouse_pos[1]))
    mouse_part = snakeGame.Parts(0, Vector2D((mouse_grid_pos.x * Grid.cell_size) - Grid.start_pos.x,
                                             (mouse_grid_pos.y * Grid.cell_size) - Grid.start_pos.x))
    mouse_part.render(screen, color=(0, 255, 0))

def debug_grid_with_part():
    part = snakeGame.Parts(0, Vector2D(80, 52))
    part.render(screen, color=(255, 255, 255))
    part_grid_pos = screen_to_world_pos(part.position)
    print(f"screen pos: {part.position}")
    print(f"Grid_pos x: {part_grid_pos.x}, Gris_pos y: {part_grid_pos.y}")
show_grid()

while running:

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.update()


