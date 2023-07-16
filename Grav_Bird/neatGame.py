import pygame
import pickle
import neat
import os
from constants import *
from game import Game

def eval_genomes(genomes, config):
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    game = Game(screen)
    game.run_NEAT_training(genomes, config)

def run_neat(config):
    pygame.init()
    #p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-0')
    p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))
    winner = p.run(eval_genomes, 50)
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)
    pygame.quit()

def get_config():
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    return neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

if __name__ == "__main__":
    config = get_config()
    run_neat(config)