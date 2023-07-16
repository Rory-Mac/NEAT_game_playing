import pygame
from constants import *
from bird import Bird
from pipe import Pipe
import random
import neat
import pickle
import os

class Game:
    def __init__(self, screen):
        # game features
        self.screen = screen
        self.clock = pygame.time.Clock()
        self.score = 0
        self.bird = Bird()
        self.pipes = [
            Pipe(SCREEN_WIDTH, random.randint(100, 400), self),
            Pipe((1.5 * SCREEN_WIDTH + 40), random.randint(100, 400), self)
        ]
        # image loading
        self.bg_img = pygame.transform.scale(pygame.image.load(os.path.join("imgs","bg.png")).convert_alpha(), (SCREEN_WIDTH, SCREEN_HEIGHT))
        self.bird_img = pygame.transform.scale(pygame.image.load(os.path.join("imgs","bird.png")).convert_alpha(), (BIRD_SIZE, BIRD_SIZE))
        self.floor_img = pygame.transform.scale2x(pygame.image.load(os.path.join("imgs","floor.png")).convert_alpha())

    def get_nearest_pipe(self):
        if self.pipes[0].x < self.pipes[1].x:
            return self.pipes[0]
        return self.pipes[1]

    def process_game_events(self):
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return True
            if event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    self.bird.flap()
        return False

    def draw_game(self, birds):
        self.screen.blit(self.bg_img, (0,0))
        for bird in birds:
            self.screen.blit(self.bird_img, (bird.x,bird.y))
        for pipe in self.pipes:
            pipe.draw(self.screen)
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
        running = True
        while running:
            # if quit signal returned, end game 
            if self.process_game_events(): break
            # move game entities
            self.bird.move_bird()
            for pipe in self.pipes:
                pipe.move()
            # if collision occurred, end game
            for pipe in self.pipes:
                if pipe.check_collisions(self.bird): 
                    running = False
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
                pipe = self.get_nearest_pipe()
                output = network.activate((self.bird.vel, self.bird.y, abs(self.bird.y - pipe.y), abs(self.bird.y - (pipe.y + GAP_SIZE))))
                if output[0] > 0.5:
                    birds[i].flap()
                # increment fitness of all birds that haven't died
                genomes[i].fitness += 0.1
            # move game entities
            for bird in birds:
                bird.move_bird()
            for pipe in self.pipes:
                # if pipe moved off-screen increment fitness
                if pipe.move():
                    for genome in genomes:
                        genome.fitness += 5
            # if collision occurred, remove bird, if no birds left, end game
            for i, bird in enumerate(birds):
                for pipe in self.pipes:
                    if pipe.check_collisions(self.bird): 
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
        running = True
        while running:
            # if quit signal returned, end game 
            if self.process_game_events(): break
            # compute agent decision
            pipe = self.get_nearest_pipe()
            output = network.activate((self.bird.vel, self.bird.y, abs(self.bird.y - pipe.y), abs(self.bird.y - (pipe.y + GAP_SIZE))))
            if output[0] > 0.5:
                self.bird.flap()
            # move game entities
            self.bird.move_bird()
            for pipe in self.pipes:
                pipe.move()
            # if collision occurred, end game
            for pipe in self.pipes:
                if pipe.check_collisions(self.bird):
                    running = False
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
    game_instance.run()
    pygame.quit()