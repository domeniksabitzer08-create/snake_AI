import pygame
import snakeGame

from snakeGame import Vector2D, Grid, screen_to_grid_pos,grid_to_screen_pos ,DeltaTime, MovementManager


import time

pygame.init()

screen = pygame.display.set_mode((500, 500))
running = True


### DEBUG FUNCTIONS ###
def show_grid():
    for i in range(Grid.cell_count):
        for j in range(Grid.cell_count):
            cell = pygame.Rect((i * Grid.cell_size)+Grid.start_pos.x, (j* Grid.cell_size)+Grid.start_pos.y, Grid.cell_render_width, Grid.cell_render_width)
            pygame.draw.rect(screen, (200,0,0), cell)


def debug_grid_with_mouse():
    mouse_pos = pygame.mouse.get_pos()
    mouse_grid_pos = screen_to_grid_pos(Vector2D(mouse_pos[0], mouse_pos[1]))
    print(f"mouse grid pos: {mouse_grid_pos}")
    print(f"mouse screen pos: {mouse_pos}")


def debug_grid_with_part():
    part = snakeGame.Parts(0, Vector2D(350, 100))
    part.render(screen, color=(255, 255, 255))
    part_grid_pos = screen_to_grid_pos(part.position)
    print(f"screen pos: {part.position}")
    print(f"Grid_pos x: {part_grid_pos.x}, Gris_pos y: {part_grid_pos.y}")

### RENDERING FUNCTIONS ###
def clear_screen():
    screen.fill((0, 0, 0))

def render_parts(part_list: iter):
    for part in part_list:
        part.render(screen, color=(255, 255, 255))

### START ###
start_pos_grid = Vector2D(5, 5)
start_pos_screen = grid_to_screen_pos(start_pos_grid)
print(f"screen pos: {start_pos_screen} | grid pos: {start_pos_grid}")
n_starting_parts = 3
part_list = []

first_part = snakeGame.Parts(0, start_pos_screen)
movement_manager = MovementManager(first_part, 1, DeltaTime.get_delta_time()) # Todo-- delta time is static, use the Delta_time directly in the move-function of Parts class

# Creating the first 4 pieces
for i in range(n_starting_parts):
    part_list.append(snakeGame.Parts(i+1, Vector2D(start_pos_screen.x-(Grid.cell_size*(i+1)) ,start_pos_screen.y)))
    movement_manager.add_part(part_list[i])
    for j in range(i):
        part_list[i].movement_list.append(movement_manager.direction)

speed = 0.01

### Update ###
while running:

    tick = pygame.time.get_ticks()
    clear_screen()
    show_grid()
    movement_manager.handle_input()
    first_part.render(screen, color=(255, 255, 255))
    render_parts(part_list)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if tick % 200 == 0:
        movement_manager.tick()
    pygame.display.update()



