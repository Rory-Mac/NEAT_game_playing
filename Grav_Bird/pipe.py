import pygame
from constants import *
import random
import os

class Pipe:
    def __init__(self, x, y, game):
        self.game = game
        self.pipe_img = pygame.transform.scale(pygame.image.load(os.path.join("imgs","pipe.png")).convert_alpha(), (PIPE_WIDTH, PIPE_HEIGHT))
        self.x = x
        self.y = y

    def move(self):
        self.x -= PIPE_SPEED
        if self.x < -PIPE_WIDTH:
            self.x = SCREEN_WIDTH
            self.y = random.randint(100, SCREEN_HEIGHT - GAP_SIZE)
            self.game.score += 1
            return True
        return False

    def check_collisions(self, bird):
        collision_occurred = False
        if bird.y > SCREEN_HEIGHT or bird.y < -BIRD_SIZE:
            collision_occurred = True
        if bird.x + BIRD_SIZE > self.x and bird.x < self.x + PIPE_WIDTH:
            if bird.y < self.y or bird.y + BIRD_SIZE > self.y + GAP_SIZE:
                collision_occurred = True
        return collision_occurred
    
    def draw(self, screen):
        screen.blit(self.pipe_img, (self.x, self.y + GAP_SIZE))
        screen.blit(pygame.transform.flip(self.pipe_img, False, True), (self.x, self.y - PIPE_HEIGHT))