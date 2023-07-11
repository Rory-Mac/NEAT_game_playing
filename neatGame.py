from pong.game import Game
import neat
import os
import pickle
from pong.paddle import *

class NeatTrainingGame:
    def __init__(self, screen):
        self.game = Game(NeatAgentPaddle(PaddleOrientation.LEFT_ORIENTED), NeatAgentPaddle(PaddleOrientation.RIGHT_ORIENTED), screen)

    def train_ai(self, left_genome, right_genome, config):
        left_network = neat.nn.FeedForwardNetwork.create(left_genome, config)
        right_network = neat.nn.FeedForwardNetwork.create(right_genome, config)
        left_score, right_score = self.game.run_NEAT_training(left_network, right_network)
        left_genome.fitness += left_score
        right_genome.fitness += right_score

def eval_genomes(genomes, config):
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    for i, (_, left_genome) in enumerate(genomes):
        if i == len(genomes) - 1:
            break
        left_genome.fitness = 0
        for _, right_genome in genomes[i+1:]:
            right_genome.fitness = 0 if right_genome.fitness == None else right_genome.fitness
            neat_game = NeatTrainingGame(screen)
            neat_game.train_ai(left_genome, right_genome, config)
    pygame.quit()

def run_neat(config):
    p = neat.Checkpointer.restore_checkpoint('neat-checkpoint-7')
    #p = neat.Population(config)
    p.add_reporter(neat.StdOutReporter(True))
    stats = neat.StatisticsReporter()
    p.add_reporter(stats)
    p.add_reporter(neat.Checkpointer(1))

    winner = p.run(eval_genomes, 1)
    with open("best.pickle", "wb") as f:
        pickle.dump(winner, f)

if __name__ == "__main__":
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    run_neat(config)