import time
from time import sleep

import pygame
from dataclasses import dataclass

from random import randint




### MANAGEMENT CLASSES ###

@dataclass(frozen=True)
class Vector2D:
        x: float
        y: float
        def __add__(self, other):
            # Vector + Vector
            if isinstance(other, Vector2D):
                return Vector2D(self.x + other.x, self.y + other.y)
        def __sub__(self, other):
            # Vector - Vector
            if isinstance(other, Vector2D):
                return Vector2D(self.x - other.x, self.y - other.y)
        def __mul__(self, other):
            if isinstance(other, (int, float)):
                # Vector * Number
                return Vector2D(self.x * other, self.y * other)
        def __truediv__(self, other):
            # Vector / Number
            if isinstance(other, (int, float)):
                return Vector2D(self.x / other, self.y / other)

# Vector directions
Vector2D.left = Vector2D(-1, 0)
Vector2D.right = Vector2D(1, 0)
Vector2D.up = Vector2D(0, -1)
Vector2D.down = Vector2D(0, 1)

class RefreshRate:
    refresh_rate = 120

class DeltaTime:
    @staticmethod
    def get_delta_time() -> float:
        """Returns the delta_time depending on the refresh_rate"""
        clock = pygame.time.Clock()
        delta_time = clock.tick(RefreshRate.refresh_rate)
        delta_time = max(0.001,min(0.1,delta_time))
        return delta_time

class Grid:
    start_pos = Vector2D(100, 100)
    cell_count = 10
    cell_size = 30
    cell_render_width = 10

class Snake:
    render_size = 20

def screen_to_grid_pos(pos: Vector2D):
    """Converts the screen position to the grid position of the game field"""
    # find the nearest cell position
    nearest_pos_x = int((pos.x - Grid.start_pos.x)/ Grid.cell_size)
    nearest_pos_y = int((pos.y - Grid.start_pos.y) / Grid.cell_size)
    return Vector2D(nearest_pos_x, nearest_pos_y)

def grid_to_screen_pos(pos: Vector2D):
    """Converts the grid position to the screen position"""
    x = (pos.x * Grid.cell_size) + Grid.start_pos.x
    y = (pos.y * Grid.cell_size) + Grid.start_pos.y
    return Vector2D(x, y)

class Food:
    render_size = 20
    def __init__(self, grid_pos: Vector2D):
        self.grid_pos = grid_pos
        self.screen_pos = grid_to_screen_pos(grid_pos)

    def render(self,screen, color=(255,0,0)):
        food = pygame.Rect(self.screen_pos.x, self.screen_pos.y, Food.render_size, Food.render_size )
        pygame.draw.rect(screen, color, food)


class Parts:
    def __init__(self, index: int, start_pos: Vector2D):
        self.index = index
        self.position = start_pos
        self.grid_pos = screen_to_grid_pos(start_pos)
        self.movement_list = []
        self.start_pos = start_pos


    def move(self, direction: Vector2D):
        self.position += direction * Grid.cell_size
        self.grid_pos = screen_to_grid_pos(self.position)

    def render(self, screen, color = (255,0,0)):
        part = pygame.Rect(self.position.x,self.position.y,Snake.render_size,Snake.render_size)
        pygame.draw.rect(screen,color,part)

class GameManager:
    """Manages the game loop"""
    def __init__(self, first_part:Parts, movement_manager:"MovementManager"):
        self.first_part = first_part
        self.score = 0
        self.is_game_over = False
        self.fruit = None
        self.movement_manager = movement_manager
    def game_over(self):
        print("Game Over!")
        self.is_game_over = True



    def check_border_collision(self):
        if self.first_part.grid_pos.x >= Grid.cell_count or self.first_part.grid_pos.x < 0:
            self.game_over()
        if self.first_part.grid_pos.y >= Grid.cell_count or self.first_part.grid_pos.y < 0:
            self.game_over()

    def check_other_part_collision(self):
        for part in self.movement_manager.part_list:
            if self.first_part.grid_pos == part.grid_pos:
                print("Other snake part")
                self.game_over()

    def spawn_fruit(self):
        # Spawn food at random pos, if a part collides with the food try again
        rnd_pos = Vector2D(randint(0, Grid.cell_count - 1), randint(0, Grid.cell_count - 1))
        self.fruit = Food(rnd_pos)
        for part in self.movement_manager.part_list:
            if part.grid_pos == rnd_pos:
                self.spawn_fruit()

    def check_food_collision(self):
        if self.first_part.grid_pos == self.fruit.grid_pos:
            self.movement_manager.add_part()
            self.spawn_fruit()

class MovementManager:
    def __init__(self,  speed: float, delta_time: float):
        self.direction = Vector2D(1, 0) # the direction of the first_part
        self.first_part = None
        self.speed = speed
        self.delta_time = delta_time
        self.is_dir_changing = False
        self.part_list = []



    def tick(self):
        time.sleep(0.1)
        # add the direction of the first part, move the part and delete the saved movement
        #self.first_part.move(self.direction) # Currently commeted out because first part is now in part list
        for part in self.part_list:
            part.movement_list.append(self.direction)
            part.move(part.movement_list[0])
            part.movement_list.pop(0)
        self.is_dir_changing = False


    def change_direction(self, new_direction: Vector2D):
        if self.check_movement(new_direction) and not self.is_dir_changing:
            self.is_dir_changing = True
            self.direction = new_direction


    def add_part(self):
        new_idx = len(self.part_list)
        try:
            new_part_start_x = self.part_list[new_idx-1].grid_pos.x - self.part_list[new_idx-1].movement_list[0].x
            new_part_start_y = self.part_list[new_idx-1].grid_pos.y - self.part_list[new_idx-1].movement_list[0].y
            print(
                f"No error - Index: {new_idx} | pos: {new_part_start_x}, {new_part_start_y} | Calculation: {self.part_list[new_idx - 1].grid_pos.x} - {self.part_list[new_idx-1].movement_list[0].x}")
        except IndexError:
            new_part_start_x = self.part_list[new_idx-1].grid_pos.x - new_idx
            new_part_start_y = self.part_list[new_idx-1].grid_pos.y
            print(f"Index error - Index: {new_idx} | pos: {new_part_start_x}, {new_part_start_y} | Calculation: {self.part_list[new_idx-1].grid_pos.x} - {new_idx}")

        new_part_start_pos = grid_to_screen_pos(Vector2D(new_part_start_x, new_part_start_y))
        new_part = Parts(index=new_idx, start_pos = new_part_start_pos)
        self.part_list.append(new_part)
        new_part.movement_list.append(self.direction)
        for i in range(new_part.index ):
            new_part.movement_list.append(self.direction)
        self.part_list.append(new_part)

    def init_parts(self, n_parts: int, start_grid_pos: Vector2D):

        start_pos = grid_to_screen_pos(start_grid_pos)
        for i in range(n_parts):
            if i == 0:
                self.first_part = Parts(index=0, start_pos=start_pos)
                self.part_list.append(self.first_part)
            else:
                self.part_list.append(Parts(i, Vector2D(start_pos.x - (Grid.cell_size*i),start_pos.y)))

            print(f"{i}. part pos: {self.part_list[i].start_pos.x}, {self.part_list[i].start_pos.y}")
            for j in range(i):
                self.part_list[i].movement_list.append(self.direction)

    def check_movement(self, new_direction: Vector2D):
        """checks if the movement change can be executed"""
        if (new_direction * -1) == self.direction:
            return False
        else:
            return True
    def handle_input(self):
        if pygame.key.get_pressed()[pygame.K_w]:
            self.change_direction(Vector2D.up)
        elif pygame.key.get_pressed()[pygame.K_s]:
            self.change_direction(Vector2D.down)
        elif pygame.key.get_pressed()[pygame.K_d]:
            self.change_direction(Vector2D.right)
        elif pygame.key.get_pressed()[pygame.K_a]:
            self.change_direction(Vector2D.left)


