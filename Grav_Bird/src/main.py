import os
import neat
import pickle
import pygame
from constants import *
from play_types.neatAgents import RunNeatAgents
from play_types.defaultAgent import RunDefaultAgent
from play_types.bestAgent import RunBestAgent

def eval_genomes(genomes, config):
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    game = RunNeatAgents(genomes, config, screen)
    game.run()

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
    local_dir = os.getcwd()
    config_path = os.path.join(local_dir, "config.txt")
    return neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)

def load_best_agent():
    config = get_config()
    with open("best.pickle", "rb") as f:
        genome = pickle.load(f)
    return neat.nn.FeedForwardNetwork.create(genome, config)

if __name__ == "__main__":
    # default | neat | best
    game_type = "default"
    pygame.init()
    if game_type == "default":
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        game = RunDefaultAgent(screen)
        game.run()
    if game_type == "neat":
        config = get_config()
        run_neat(config)
    if game_type == "best":
        screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        network = load_best_agent()
        game = RunBestAgent(network, screen)
        game.run()
    pygame.quit()