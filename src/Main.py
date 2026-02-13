import pygame
import snakeGame

from snakeGame import Vector2D, Grid, screen_to_grid_pos,grid_to_screen_pos ,DeltaTime, MovementManager, GameManager


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

def render_fruit(food):
    food.render(screen, color=(255, 0,0))


### START ###
start_pos_grid = Vector2D(0, 0)
start_pos_screen = grid_to_screen_pos(start_pos_grid)
print(f"screen pos: {start_pos_screen} | grid pos: {start_pos_grid}")
n_starting_parts = 5
part_list = []

#first_part = snakeGame.Parts(0, start_pos_screen)
movement_manager = MovementManager( 1, DeltaTime.get_delta_time()) # Todo-- delta time is static, use the Delta_time directly in the move-function of Parts class

# Creating the first 4 pieces
#for i in range(n_starting_parts):
#    movement_manager.add_part()

movement_manager.init_parts(n_starting_parts, Vector2D(1, 1))
first_part = movement_manager.first_part

speed = 0.01

game_manager = GameManager(first_part, movement_manager=movement_manager)
# Spawning the first fruit manual
game_manager.spawn_fruit()
print(f"Fruits: {game_manager.fruit.grid_pos}")
### Update ###
while running and not game_manager.is_game_over:

    tick = pygame.time.get_ticks()
    clear_screen()
    show_grid()
    movement_manager.handle_input()
    first_part.render(screen, color=(0, 255, 0))
    # Rendering
    render_parts(movement_manager.part_list)
    render_fruit(game_manager.fruit)

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            running = False
    if tick % 300 == 0:
        movement_manager.tick()
        #game_manager.check_border_collision()
        #game_manager.check_other_part_collision()
        game_manager.check_food_collision()
    pygame.display.update()



