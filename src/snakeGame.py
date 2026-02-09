import pygame
from dataclasses import dataclass







@dataclass
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

class Grid:
    start_pos = Vector2D(60, 60)
    cell_count = 13
    cell_size = 30



def screen_to_world_pos(pos: Vector2D):
    """Converts the screen position to the grid position of the game field"""


class Snake:
    def __init__(self, start_pos: Vector2D):
        self.position = start_pos

    def move(self, direction: Vector2D):
        self.position += direction

class Parts:
    def __init__(self, index: int, start_pos: Vector2D):
        self.index = index
        self.position = start_pos
    def move(self, direction: Vector2D):
        self.position += direction
    def render(self, screen):
        part = pygame.Rect(self.position.x,self.position.y,10,10)
        pygame.draw.rect(screen,(255,0,0),part)

