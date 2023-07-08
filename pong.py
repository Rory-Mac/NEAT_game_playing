import pygame
from ball import Ball
from paddle import *
from constants import *

def exit_game():
    # end screen waits for user to quit
    initial_running = True
    while initial_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)

def main():
    # intialise game features
    pygame.init()
    clock = pygame.time.Clock()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    left_paddle = PerfectAgentPaddle(PaddleOrientation.LEFT_ORIENTED)
    right_paddle = HumanPaddle(PaddleOrientation.RIGHT_ORIENTED)
    ball = Ball()
    # initial screen waits for user keypress
    left_paddle.draw(screen)
    right_paddle.draw(screen)
    ball.draw(screen)
    pygame.display.flip()
    initial_running = True
    while initial_running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                exit(0)
            elif event.type == pygame.KEYDOWN:
                initial_running = False
    # main game loop
    running = True
    while running:
        # user event handling
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                print(f"Left paddle score: {left_paddle.score}")
                print(f"Right paddle score: {right_paddle.score}")
                running = False
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    right_paddle.is_moving_up = True
                elif event.key == pygame.K_DOWN:
                    right_paddle.is_moving_down = True
                elif event.key == pygame.K_w:
                    left_paddle.is_moving_up = True
                elif event.key == pygame.K_s:
                    left_paddle.is_moving_down = True
            if event.type == pygame.KEYUP:
                if event.key == pygame.K_UP:
                    right_paddle.is_moving_up = False
                elif event.key == pygame.K_DOWN:
                    right_paddle.is_moving_down = False
                elif event.key == pygame.K_w:
                    left_paddle.is_moving_up = False
                elif event.key == pygame.K_s:
                    left_paddle.is_moving_down = False

        # ball and paddle movement
        left_paddle.move()
        right_paddle.move()
        ball.move()
        ball.check_collisions(left_paddle, right_paddle)

        # check termination condition
        if ball.out_of_bounds(): 
            print(f"Left paddle score: {left_paddle.score}")
            print(f"Right paddle score: {right_paddle.score}")
            exit_game()

        # update frame buffer
        screen.fill((0, 0, 0))
        left_paddle.draw(screen)
        right_paddle.draw(screen)
        ball.draw(screen)

        # update the display
        clock.tick(MAX_FRAME_RATE)
        pygame.display.flip()
    pygame.quit()

if __name__ == "__main__":
    main()