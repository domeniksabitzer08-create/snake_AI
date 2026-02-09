import pygame
import snakeGame

from snakeGame import Vector2D
from snakeGame import Grid

import time

pygame.init()

screen = pygame.display.set_mode((500, 500))
running = True

def show_grid():
    for i in range(Grid.cell_count):
        for j in range(Grid.cell_count):
            cell = snakeGame.Parts(0, Vector2D(i*Grid.cell_size , j*Grid.cell_size))
            cell.render(screen)
            time.sleep(0.01)
            pygame.display.update()
show_grid()
while running:
    part = snakeGame.Parts(0,Vector2D(30,30))
    part.render(screen)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    pygame.display.update()


