from constants import *
import pygame

class Ball:
    def __init__(self):
        self.shape = pygame.Rect(SCREEN_WIDTH / 2 - BALL_WIDTH, SCREEN_HEIGHT / 2 - BALL_WIDTH, BALL_WIDTH, BALL_WIDTH)
        self.horizontal_direction = 1
        self.vertical_direction = 1
        self.vertical_speed = 2
        self.horizontal_speed = BALL_SPEED

    def update_directionality(self, left_paddle, right_paddle):
        if self.overlaps(right_paddle.shape) or self.overlaps(left_paddle.shape):
            self.horizontal_speed *= -1
        if self.shape.y <= 0 or self.shape.y + BALL_WIDTH >= SCREEN_HEIGHT:
            self.vertical_speed *= -1

    def move(self, left_paddle, right_paddle):
        self.update_directionality(left_paddle, right_paddle)
        self.shape.x += self.horizontal_speed
        self.shape.y += self.vertical_speed

    def draw(self, screen):
        pygame.draw.rect(screen, (255,255,255), self.shape)
    
    def overlaps(self, paddle):
        return self.shape.colliderect(paddle)

    def out_of_bounds(self):
        return self.shape.x < 0 - BALL_WIDTH or self.shape.x > SCREEN_WIDTH + BALL_WIDTH