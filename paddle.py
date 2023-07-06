from enum import Enum, auto
from abc import ABC
from constants import *
import pygame

class PaddleOrientation(Enum):
    LEFT_ORIENTED = auto()
    RIGHT_ORIENTED = auto()

class Paddle(ABC):
    def __init__(self, orientation):
        self.orientation = orientation
        if self.is_left_oriented():
            self.shape = pygame.Rect(10, (SCREEN_HEIGHT - PADDLE_HEIGHT) / 2, PADDLE_WIDTH, PADDLE_HEIGHT)
        else:
            self.shape = pygame.Rect(SCREEN_WIDTH - (10 + PADDLE_WIDTH), (SCREEN_HEIGHT - PADDLE_HEIGHT) / 2, PADDLE_WIDTH, PADDLE_HEIGHT)
        self.is_moving_up = False
        self.is_moving_down = False

    def is_left_oriented(self):
        return self.orientation == PaddleOrientation.LEFT_ORIENTED

    def move(self):
        if self.is_moving_up and self.shape.y > 0:
            self.shape.y -= PADDLE_SPEED
        if self.is_moving_down and self.shape.y < SCREEN_HEIGHT - PADDLE_HEIGHT:
            self.shape.y += PADDLE_SPEED

    def draw(self, screen):
        pygame.draw.rect(screen, (255,255,255), self.shape)


class HumanPaddle(Paddle):
    def __init__(self, orientation):
        super().__init__(orientation)

class WallPaddle(Paddle):
    def __init__(self, orientation):
        super().__init__(orientation)
        if self.is_left_oriented():
            self.shape = pygame.Rect(0, 0, 10, SCREEN_HEIGHT)
        else:
            self.shape = pygame.Rect(SCREEN_WIDTH - PADDLE_WIDTH, 0, 10, SCREEN_HEIGHT)

    def move(self):
        pass

class PerfectAgentPaddle(Paddle):
    def __init__(self, orientation):
        super().__init__(orientation)



class NeatAgentPaddle(Paddle):
    def __init__(self, orientation):
        super().__init__(orientation)
