import pygame
from pong.game import Game
from pong.constants import *
from pong.paddle import *

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    game = Game(NeatVsHumanPaddle(PaddleOrientation.LEFT_ORIENTED), HumanPaddle(PaddleOrientation.RIGHT_ORIENTED), screen)
    game.run()