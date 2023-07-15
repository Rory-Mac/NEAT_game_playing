import pygame
import pickle
from obstacles import ObstacleGrid
from constants import *
from player import Player
import neat

#----------------------------------------------------------------------
# Store game information
#----------------------------------------------------------------------
game_data_file_path = "obstacle_data.pkl"

def store_data(data):
    with open(game_data_file_path, "wb") as file:
        pickle.dump(data, file)

def print_data():
    with open(game_data_file_path, "rb") as file:
        data = pickle.load(file)
        print(data)

def wipe_data():
    with open(game_data_file_path, 'wb') as file:
        pickle.dump([], file)

#----------------------------------------------------------------------
# Main game loop to manage sequence of screen events and player actions
#----------------------------------------------------------------------
class Game:
    def __init__(self, screen, game_surface):
        self.clock = pygame.time.Clock()
        self.screen = screen
        self.game_surface = game_surface
        self.player = Player()
        self.obstacle_grid = ObstacleGrid()
    
    def game_exit(self):
        while True:
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    pygame.quit()
                    exit(0)

    def draw_initial_display(self):
        self.game_surface.fill((0,0,0))
        self.player.draw(self.game_surface)
        self.screen.blit(self.game_surface, (500, 50))
        pygame.display.flip()

    def run(self):
        # initial screen
        self.draw_initial_display()
        intial_running = True
        while intial_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)
                if event.type == pygame.KEYDOWN:
                    intial_running = False
        # start main game loop
        frame_count = 0
        running = True
        while running and (not PROFILE_MODE or frame_count < PROFILE_ITERATIONS):
            # process game events
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    running = False
                self.player.update_player_movement(event)
            # move player and check for collisions
            self.player.move()
            if self.obstacle_grid.collides_with(self.player): 
                self.game_exit()
            # update obstacles
            self.obstacle_grid.update(self.player, frame_count)
            # update frame buffer
            self.game_surface.fill((0,0,0))
            self.player.draw(self.game_surface)
            self.obstacle_grid.draw(self.game_surface)
            # blit surfaces to screen and flip to next frame
            self.screen.blit(self.game_surface, (500, 50))
            self.clock.tick(MAX_FRAME_RATE)
            pygame.display.flip()
            frame_count += 1

    def make_decision(self, network):
        binary_grid = self.obstacle_grid.get_grid_as_binary()
        player_row = (self.player.body.y // GRID_CELL_SIZE) * GRID_CELL_SIZE
        player_col = (self.player.body.x // GRID_CELL_SIZE) * GRID_CELL_SIZE
        obstacle_information = self.player.get_obstacle_distances(self.obstacle_grid)
        return network.activate([*binary_grid, *obstacle_information, self.player.body.x, self.player.body.y, player_row, player_col])

    def update_movement(self, player, network):
        output = self.make_decision(network)
        # up movement decision
        if output[0] > 0.5:
            player.is_moving_up = True
        else:
            player.is_moving_up = False
        # down movement decision
        if output[1] > 0.5:
            player.is_moving_down = True
        else:
            player.is_moving_down = False
        # left movement decision
        if output[2] > 0.5:
            player.is_moving_left = True
        else:
            player.is_moving_left = False
        # right movement decision
        if output[3] > 0.5:
            player.is_moving_right = True
        else:
            player.is_moving_right = False

    def run_NEAT_training(self, genome_tuples, config):
        networks = []
        players = []
        genomes = []
        for _, genome in genome_tuples:
            networks.append(neat.nn.FeedForwardNetwork.create(genome, config))
            players.append(Player())
            genome.fitness = 0
            genomes.append(genome)
        # game loop
        frame_count = 0
        while True:
            # compute NEAT AGENT decisions
            for i, player in enumerate(players):
                self.update_movement(player, networks[i])
                # increment fitness of all players that haven't died
                genomes[i].fitness += 0.1
            # move game entities
            for i, player in enumerate(players):
                player.move()
                # if player collides with obstacle grid, remove player
                if self.obstacle_grid.collides_with(player): 
                    genomes[i].fitness -= 1
                    networks.pop(i)
                    players.pop(i)
                    genomes.pop(i)
            # if no players left, end game
            if not players: break
            # if obstacle grid is updated (layer has been passed), increment fitness 
            if self.obstacle_grid.update(self.player, frame_count):
                for genome in genomes:
                    genome.fitness += 5
            # terminate training if fitness threshold reached (representing no. layers passed)
            if frame_count > (GRID_CELL_SIZE // OBSTACLE_SPEED) * FITNESS_THRESHOLD: break
            # update display
            if VISUALISE:
                self.game_surface.fill((0,0,0))
                for player in players:
                    player.draw(self.game_surface)
                self.obstacle_grid.draw(self.game_surface)
                self.screen.blit(self.game_surface, (500, 50))
                pygame.display.flip()
                # advance frame buffer
                self.clock.tick(MAX_FRAME_RATE)
            frame_count += 1

    def run_best_agent(self, network):
        # initial screen
        self.draw_initial_display()
        intial_running = True
        while intial_running:
            for event in pygame.event.get():
                if event.type == pygame.QUIT:
                    pygame.quit()
                    exit(0)
                if event.type == pygame.KEYDOWN:
                    intial_running = False
        # Game loop
        frame_count = 0
        running = True
        while running:
            # process game events
            for event in pygame.event.get():
                if event.type == pygame.QUIT: 
                    running = False
                self.player.update_player_movement(event)
            # compute agent decision
            self.update_movement(self.player, network)
            # move player and check for collisions
            self.player.move()
            if self.obstacle_grid.collides_with(self.player): 
                self.game_exit()
            # update obstacles
            self.obstacle_grid.update(self.player, frame_count)
            # update frame buffer
            self.game_surface.fill((0,0,0))
            self.player.draw(self.game_surface)
            self.obstacle_grid.draw(self.game_surface)
            # blit surfaces to screen and flip to next frame
            self.screen.blit(self.game_surface, (500, 50))
            self.clock.tick(MAX_FRAME_RATE)
            pygame.display.flip()
            frame_count += 1

# seperate for profiling
if __name__ == "__main__":
    pygame.init()
    display = pygame.display.set_mode((500 + GAME_WIDTH + 50, 50 + GAME_HEIGHT + 50))
    pygame.draw.rect(display, (255,255,255), (490, 40, GAME_WIDTH + 20, GAME_HEIGHT + 20))
    game_surface = pygame.Surface((GAME_WIDTH, GAME_HEIGHT))
    game_instance = Game(display, game_surface)
    game_instance.run()
    pygame.quit()