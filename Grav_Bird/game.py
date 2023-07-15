import pygame
from constants import *
from bird import Bird
import random
import neat
import pickle
import os

class Game:
    def __init__(self, screen):
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.bird = Bird()
        self.pipe_height = random.randint(100, 400)
        self.pipe_x = SCREEN_WIDTH
        self.score = 0

    def move_pipes(self):
        self.pipe_x -= 5
        if self.pipe_x < -PIPE_WIDTH:
            self.pipe_x = SCREEN_WIDTH
            self.pipe_height = random.randint(100, SCREEN_HEIGHT - GAP_SIZE)
            self.score += 1
            return True
        return False


    def check_collisions(self, bird):
        collision_occurred = False
        if bird.y > SCREEN_HEIGHT or bird.y < -BIRD_SIZE:
            collision_occurred = True
        if bird.x + BIRD_SIZE > self.pipe_x and bird.x < self.pipe_x + PIPE_WIDTH:
            if bird.y < self.pipe_height or bird.y + BIRD_SIZE > self.pipe_height + GAP_SIZE:
                collision_occurred = True
        return collision_occurred

    def process_game_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.bird.flap()
        return False

    def draw_game(self, birds):
        self.screen.fill((0, 0, 0))
        for bird in birds:
            pygame.draw.rect(self.screen, (255, 255, 255), (bird.x, bird.y, BIRD_SIZE, BIRD_SIZE))
        pygame.draw.rect(self.screen, (255, 255, 255), (self.pipe_x, 0, PIPE_WIDTH, self.pipe_height))
        pygame.draw.rect(self.screen, (255, 255, 255), (self.pipe_x, self.pipe_height + GAP_SIZE, PIPE_WIDTH, SCREEN_HEIGHT - self.pipe_height - GAP_SIZE))
        pygame.display.update()

    def run(self):
        # initial screen
        if VISUALISE: 
            self.draw_game([self.bird])
        intial_running = True
        while intial_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)
                if event.type == pygame.KEYDOWN:
                    intial_running = False
        # Game loop
        while True:
            # if quit signal returned, end game 
            if self.process_game_events(): break
            # move game entities
            self.bird.move_bird()
            self.move_pipes()
            # if collision occurred, end game
            if self.check_collisions(self.bird): break
            # Update display
            if VISUALISE: self.draw_game([self.bird])
            pygame.display.update()
            self.clock.tick(MAX_FRAME_RATE)
        print(self.score)

    def run_NEAT_training(self, genome_tuples, config):
        networks = []
        birds = []
        genomes = []
        for _, genome in genome_tuples:
            networks.append(neat.nn.FeedForwardNetwork.create(genome, config))
            birds.append(Bird())
            genome.fitness = 0
            genomes.append(genome)
        # game loop
        while True:
            # compute NEAT AGENT decisions
            for i, bird in enumerate(birds):
                output = networks[i].activate((bird.vel, bird.y, abs(bird.y - self.pipe_height), abs(bird.y - (self.pipe_height + GAP_SIZE))))
                if output[0] > 0.5:
                    birds[i].flap()
                # increment fitness of all birds that haven't died
                genomes[i].fitness += 0.1
            # move game entities
            for bird in birds:
                bird.move_bird()
            if self.move_pipes():
                for genome in genomes:
                    genome.fitness += 5
            # if collision occurred, remove bird, if no birds left, end game
            for i, bird in enumerate(birds):
                if self.check_collisions(bird):
                    genomes[i].fitness -= 1
                    networks.pop(i)
                    birds.pop(i)
                    genomes.pop(i)
            if not birds: break
            # terminate training if fitness threshold reached
            if self.score > FITNESS_THRESHOLD: break
            # Update display
            if VISUALISE: self.draw_game(birds)
            pygame.display.update()
            self.clock.tick(MAX_FRAME_RATE)

    def run_best_agent(self, network):
        # initial screen
        if VISUALISE:
            self.draw_game([self.bird])
        intial_running = True
        while intial_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)
                if event.type == pygame.KEYDOWN:
                    intial_running = False
        # Game loop
        while True:
            # if quit signal returned, end game 
            if self.process_game_events(): break
            # compute agent decision
            output = network.activate((self.bird.vel, self.bird.y, abs(self.bird.y - self.pipe_height), abs(self.bird.y - (self.pipe_height + GAP_SIZE))))
            if output[0] > 0.5:
                self.bird.flap()
            # move game entities
            self.bird.move_bird()
            self.move_pipes()
            # if collision occurred, end game
            if self.check_collisions(self.bird): break
            # Update display
            if VISUALISE: self.draw_game([self.bird])
            pygame.display.update()
            self.clock.tick(MAX_FRAME_RATE)
        print(self.score)

def load_network():
    local_dir = os.path.dirname(__file__)
    config_path = os.path.join(local_dir, "config.txt")
    config = neat.Config(neat.DefaultGenome, neat.DefaultReproduction, neat.DefaultSpeciesSet, neat.DefaultStagnation, config_path)
    with open("best.pickle", "rb") as f:
        genome = pickle.load(f)
    return neat.nn.FeedForwardNetwork.create(genome, config)

if __name__ == "__main__":
    pygame.init()
    screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
    game_instance = Game(screen)
    network = load_network()
    game_instance.run_best_agent(network)
    pygame.quit()