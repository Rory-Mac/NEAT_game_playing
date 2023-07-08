from constants import *
import pygame
import math
import random
from paddle import PerfectAgentPaddle

class Ball:
    def __init__(self):
        self.shape = pygame.Rect(SCREEN_WIDTH / 2 - BALL_WIDTH, SCREEN_HEIGHT / 2 - BALL_WIDTH, BALL_WIDTH, BALL_WIDTH)
        self.vertical_velocity = random.choice([-BALL_SPEED, BALL_SPEED])
        self.horizontal_velocity = BALL_SPEED * random.choice([-1,1])

    def move(self):
        self.shape.x += self.horizontal_velocity
        self.shape.y += self.vertical_velocity

    def draw(self, screen):
        pygame.draw.rect(screen, (255,255,255), self.shape)

    def out_of_bounds(self):
        return self.shape.x < 0 - BALL_WIDTH or self.shape.x > SCREEN_WIDTH + BALL_WIDTH

    def collide_with(self, paddle):
        # calculate angle of collision
        paddle_centre_point = paddle.y + paddle.height / 2
        ball_centre_point = self.shape.y + self.shape.height / 2
        relative_collision = (ball_centre_point - paddle_centre_point) / (paddle.height / 2)
        bounce_angle = relative_collision * (math.pi / 4)
        # update velocity based on collision
        ball_speed = math.sqrt(self.horizontal_velocity ** 2 + self.vertical_velocity ** 2)
        self.horizontal_velocity = ball_speed * math.cos(bounce_angle)
        self.vertical_velocity = ball_speed * -math.sin(bounce_angle)
        if self.shape.x > SCREEN_WIDTH / 2:
            self.horizontal_velocity *= -1
        self.move()

    def ghost_ball(self, paddle):
        x = self.shape.x
        y = self.shape.y
        vv = self.vertical_velocity
        # move perfect paddle randomly for unique case of no vertical movement 
        if self.vertical_velocity == 0:
            return self.shape.y + random.uniform(0, PADDLE_HEIGHT / 2) * random.choice([1,-1])
        if self.horizontal_velocity > 0:
            while x < paddle.shape.x:
                if y <= 0 or y + BALL_WIDTH >= SCREEN_HEIGHT:
                    vv *= -1
                x += round(self.horizontal_velocity)
                y += round(vv)
        elif self.horizontal_velocity < 0:
            while x > paddle.shape.x + paddle.shape.width:
                if y <= 0 or y + BALL_WIDTH >= SCREEN_HEIGHT:
                    vv *= -1
                x += round(self.horizontal_velocity)
                y += round(vv)
        return y

    def check_collisions(self, left_paddle, right_paddle):
        # check collision with roof or floor
        if self.shape.y <= 0 or self.shape.y + BALL_WIDTH >= SCREEN_HEIGHT:
            self.vertical_velocity *= -1
        # check collision with left paddle
        if self.shape.colliderect(left_paddle.shape):
            self.collide_with(left_paddle.shape)
            left_paddle.score += 1
            if isinstance(right_paddle, PerfectAgentPaddle):
                right_paddle.notify(self.ghost_ball(right_paddle))
        # check collision with right paddle
        elif self.shape.colliderect(right_paddle.shape):
            self.collide_with(right_paddle.shape)
            right_paddle.score += 1
            if isinstance(left_paddle, PerfectAgentPaddle):
                left_paddle.notify(self.ghost_ball(left_paddle))