import pygame
from pong.ball import Ball
from pong.paddle import *
from pong.constants import *

class Game:
    def __init__(self, left_paddle, right_paddle, screen):
        # intialise game features
        self.clock = pygame.time.Clock()
        self.left_paddle = left_paddle 
        self.right_paddle = right_paddle
        self.screen = screen
        self.ball = Ball()
        # notify perfect agents of initial ball position
        if self.ball.horizontal_velocity < 0 and isinstance(self.left_paddle, PerfectAgentPaddle):
            self.left_paddle.notify(self.ball.ghost_ball(self.left_paddle))
        if self.ball.horizontal_velocity > 0 and isinstance(self.right_paddle, PerfectAgentPaddle):
            self.right_paddle.notify(self.ball.ghost_ball(self.right_paddle)) 

    def print_game_score(self):
        print(f"Left paddle score: {self.left_paddle.score}")
        print(f"Right paddle score: {self.right_paddle.score}")

    def run_initial_screen(self):
        # initial screen waits for user keypress
        self.left_paddle.draw(self.screen)
        self.right_paddle.draw(self.screen)
        self.ball.draw(self.screen)
        pygame.display.flip()
        initial_running = True
        while initial_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)
                elif event.type == pygame.KEYDOWN:
                    initial_running = False

    def process_events(self):
        # user event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.right_paddle.is_moving_up = True
                elif event.key == pygame.K_DOWN:
                    self.right_paddle.is_moving_down = True
                elif event.key == pygame.K_w:
                    self.left_paddle.is_moving_up = True
                elif event.key == pygame.K_s:
                    self.left_paddle.is_moving_down = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    self.right_paddle.is_moving_up = False
                elif event.key == pygame.K_DOWN:
                    self.right_paddle.is_moving_down = False
                elif event.key == pygame.K_w:
                    self.left_paddle.is_moving_up = False
                elif event.key == pygame.K_s:
                    self.left_paddle.is_moving_down = False

    def move_game_entities(self):
        if isinstance(self.left_paddle, NeatVsHumanPaddle) :
            self.left_paddle.move(self.ball)
        else:
            self.left_paddle.move()
        if isinstance(self.right_paddle, NeatVsHumanPaddle) :
            self.right_paddle.move(self.ball)
        else:
            self.right_paddle.move()
        self.ball.move()
        self.ball.check_collisions(self.left_paddle, self.right_paddle)

    def draw_game(self):
        self.screen.fill((0, 0, 0))
        self.left_paddle.draw(self.screen)
        self.right_paddle.draw(self.screen)
        self.ball.draw(self.screen)
        pygame.display.flip()

    def run(self):
        if GAME_VISUALISED: self.run_initial_screen()
        running = True
        while running:
            # if event processing returns quit signal, end game
            if self.process_events(): break
            # move ball and paddles
            self.move_game_entities()
            if self.ball.out_of_bounds(): break
            # display game state
            if GAME_VISUALISED: self.draw_game()
            # move to next time step
            self.clock.tick(MAX_FRAME_RATE)
        self.print_game_score()
        pygame.quit()
        exit(0)

    # if game is instance of NEAT AI testing session, compute AI game decisions
    def run_NEAT_testing(self, net):
        # initiate game loop
        running = True
        while running:
            # compute NEAT AGENT decisions
            output = net.activate((self.left_paddle.y, self.ball.y, abs(self.right_paddle.x - self.ball.x)))
            decision = output.index(max(output))
            if decision == 0:
                self.left_paddle.is_moving_up = False
                self.left_paddle.is_moving_down = False
            elif decision == 1:
                self.left_paddle.is_moving_up = True
                self.left_paddle.is_moving_down = False
            else:
                self.left_paddle.is_moving_up = False
                self.left_paddle.is_moving_down = True
            # move ball and paddles
            self.move_game_entities()
            if self.ball.out_of_bounds():
                break
        return (self.left_paddle.score, self.right_paddle.score)

    # if game is instance of NEAT AI training session, compute AI game decisions
    def run_NEAT_training(self, left_network, right_network):
        run = True
        while run:
            # compute NEAT AGENT decisions
            left_output = left_network.activate((self.left_paddle.shape.y, self.ball.shape.y, abs(self.left_paddle.shape.x - self.ball.shape.x)))
            left_decision = left_output.index(max(left_output))
            if left_decision == 0:
                self.left_paddle.is_moving_up = False
                self.left_paddle.is_moving_down = False
            elif left_decision == 1:
                self.left_paddle.is_moving_up = True
                self.left_paddle.is_moving_down = False
            else:
                self.left_paddle.is_moving_up = False
                self.left_paddle.is_moving_down = True

            right_output = right_network.activate((self.right_paddle.shape.y, self.ball.shape.y, abs(self.right_paddle.shape.x - self.ball.shape.x)))
            right_decision = right_output.index(max(right_output))
            if right_decision == 0:
                self.right_paddle.is_moving_up = False
                self.right_paddle.is_moving_down = False
            elif left_decision == 1:
                self.right_paddle.is_moving_up = True
                self.right_paddle.is_moving_down = False
            else:
                self.right_paddle.is_moving_up = False
                self.right_paddle.is_moving_down = True

            # terminate training if fitness threshold reached
            if self.left_paddle.score > 50 or self.right_paddle.score > 50 or self.ball.out_of_bounds():
                break
            # move ball and paddles
            self.move_game_entities()
            # display game state
            if GAME_VISUALISED: 
                self.screen.fill((0, 0, 0))
                self.left_paddle.draw(self.screen)
                self.right_paddle.draw(self.screen)
                self.ball.draw(self.screen)
                pygame.display.flip()
        return (self.left_paddle.score, self.right_paddle.score)