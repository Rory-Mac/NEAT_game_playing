import pygame
import random
import pickle
from obstacles import ObstacleGrid, FallingObstacle 
from constants import *

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
# Manage player movement
#----------------------------------------------------------------------
def update_player_movement(event, player_movement):    
    if event.type == pygame.KEYDOWN:
        if event.key == pygame.K_UP:
            player_movement[0] = True
        elif event.key == pygame.K_DOWN:
            player_movement[1] = True
        elif event.key == pygame.K_LEFT:
            player_movement[2] = True
        elif event.key == pygame.K_RIGHT:
            player_movement[3] = True

    if event.type == pygame.KEYUP:
        if event.key == pygame.K_UP:
            player_movement[0] = False
        elif event.key == pygame.K_DOWN:
            player_movement[1] = False
        elif event.key == pygame.K_LEFT:
            player_movement[2] = False
        elif event.key == pygame.K_RIGHT:
            player_movement[3] = False

def move_player(player):
    if player_movement[0] and player.y > 0:
        player.y -= 5
    if player_movement[1] and player.y < SCREEN_HEIGHT - PLAYER_HEIGHT:
        player.y += 5
    if player_movement[2] and player.x > 0:
        player.x -= 5
    if player_movement[3] and player.x < SCREEN_WIDTH - PLAYER_WIDTH:
        player.x += 5

def check_overlaps(player):
    for obstacle in obstacles:
        if obstacle.x + obstacle.width > player.x and obstacle.x < player.x + player.width and \
        obstacle.y + obstacle.height > player.y and obstacle.y < player.y + player.height:
            return True
    return False

#----------------------------------------------------------------------
# Initialise game features
#----------------------------------------------------------------------
class GameFeatures:
    def __init__(self):
        self.screen = pygame.display.set_mode((SCREEN_WIDTH, SCREEN_HEIGHT))
        self.player = pygame.Rect(SCREEN_WIDTH / 2 - (PLAYER_WIDTH / 2), SCREEN_HEIGHT / 2 - (PLAYER_HEIGHT / 2) , PLAYER_WIDTH, PLAYER_HEIGHT) 
        self.obstacle_grid = ObstacleGrid()
        self.obstacles = []

#----------------------------------------------------------------------
# Main game loop miscellaneous functions
#----------------------------------------------------------------------
def generate_obstacles(obstacle_grid, obstacles):
    if not random.randint(0, 60 / OBJECTS_PER_SECOND):
        new_obstacle = FallingObstacle()
        obstacles.append(new_obstacle)
        if not obstacle_grid.player_path_exists(obstacles):
            obstacles.remove(new_obstacle)
        else:
            obstacles = sorted(obstacles, key=lambda obstacle: obstacle.x)

def game_exit():
    for obstacle in obstacles:
        print(f"x: {obstacle.x}, y: {obstacle.y}, width: {obstacle.width}, height: {obstacle.height}")
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT: 
                exit(0)

#----------------------------------------------------------------------
# Main game loop to manage sequence of screen events and player actions
#----------------------------------------------------------------------
if __name__ == "__main__":
    pygame.init()
    clock = pygame.time.Clock()
    game = GameFeatures()
    player_movement = [False, False, False, False] # up, down, left, right
    while True:
        # evaluate exit conditions and update player trajectory   
        if check_overlaps(game.player): 
            game_exit()
        for event in pygame.event.get():
            if event.type == pygame.QUIT: exit(0)
            update_player_movement(event, player_movement)

        # for continuous player movement
        move_player(game.player)

        # update obstacles
        generate_obstacles(game.obstacle_grid, obstacles)
        obstacles = [obstacle for obstacle in obstacles if obstacle.y < SCREEN_HEIGHT]

        # update frame buffer
        game.screen.fill((0, 0, 0))
        pygame.draw.rect(game.screen, PLAYER_COLOR, game.player)
        for obstacle in obstacles:
            obstacle.update()
            pygame.draw.rect(game.screen, OBSTACLE_COLOR, (obstacle.x, obstacle.y, obstacle.width, obstacle.height))

        # advance frame based on maximum frame rate
        clock.tick(MAX_FRAME_RATE)
        pygame.display.flip()