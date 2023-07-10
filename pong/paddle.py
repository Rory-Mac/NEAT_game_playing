import pygame
import random
import neat
import pickle
import os
from enum import Enum, auto
from abc import ABC
from pong.constants import *


class PaddleOrientation(Enum):
    LEFT_ORIENTED = auto()
    RIGHT_ORIENTED = auto()

class Paddle(ABC):
    def __init__(self, orientation):
        self.score = 0
        self.orientation = orientation
        if self.is_left_oriented():
            self.shape = pygame.Rect(PADDLE_PADDING, (SCREEN_HEIGHT - PADDLE_HEIGHT) / 2, PADDLE_WIDTH, PADDLE_HEIGHT)
        else:
            self.shape = pygame.Rect(SCREEN_WIDTH - (PADDLE_PADDING + PADDLE_WIDTH), (SCREEN_HEIGHT - PADDLE_HEIGHT) / 2, PADDLE_WIDTH, PADDLE_HEIGHT)
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
        self.optimal_y = None

    def notify(self, optimal_y):
       self.optimal_y = optimal_y - random.uniform(0, PADDLE_HEIGHT / 2)

    def move(self):
        # do nothing if optimal paddle position not yet evaluated 
        if not self.optimal_y:
            return
        if self.shape.y < (self.optimal_y - PADDLE_SPEED) and self.shape.y < SCREEN_HEIGHT - PADDLE_HEIGHT:
            self.shape.y += PADDLE_SPEED
        elif self.shape.y > (self.optimal_y + PADDLE_SPEED) and self.shape.y > 0:
            self.shape.y -= PADDLE_SPEED

class NeatAgentPaddle(Paddle):
    def __init__(self, orientation):
        super().__init__(orientation)

class NeatVsHumanPaddle(Paddle):
    def __init__(self, orientation):
        super().__init__(orientation)
        config = self.__get_config_file()
        with open("best.pickle", "rb") as f:
            genome = pickle.load(f)
        self.network = neat.nn.FeedForwardNetwork.create(genome, config)
    
    def __get_config_file(self):
        curr_dir = os.getcwd()
        config_file_path = os.path.join(curr_dir, 'config.txt')
        return neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_file_path)

    def move(self, ball):
        output = self.network.activate((self.shape.y, ball.shape.y, abs(self.shape.x - ball.shape.x)))
        decision = output.index(max(output))
        print(decision)
        if decision == 0:
            self.is_moving_up = False
            self.is_moving_down = False
        elif decision == 1:
            self.is_moving_up = True
            self.is_moving_down = False
        else:
            self.is_moving_up = False
            self.is_moving_down = True
        super().move()