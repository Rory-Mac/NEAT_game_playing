import pygame
from constants import *

#----------------------------------------------------------------------
# Manage player and player movement
#----------------------------------------------------------------------
class Player:
    def __init__(self):
        self.body = pygame.Rect(GAME_WIDTH / 2 - (PLAYER_SIZE / 2), GAME_HEIGHT / 2 - (PLAYER_SIZE / 2) , PLAYER_SIZE, PLAYER_SIZE) 
        self.is_moving_up = False
        self.is_moving_down = False
        self.is_moving_left = False
        self.is_moving_right = False

    def update_player_movement(self, event):
        if event.type == pygame.KEYDOWN:
            if event.key == pygame.K_UP:
                self.is_moving_up = True
            elif event.key == pygame.K_DOWN:
                self.is_moving_down = True
            elif event.key == pygame.K_LEFT:
                self.is_moving_left = True
            elif event.key == pygame.K_RIGHT:
                self.is_moving_right = True

        if event.type == pygame.KEYUP:
            if event.key == pygame.K_UP:
                self.is_moving_up = False
            elif event.key == pygame.K_DOWN:
                self.is_moving_down = False
            elif event.key == pygame.K_LEFT:
                self.is_moving_left = False
            elif event.key == pygame.K_RIGHT:
                self.is_moving_right = False

    def move(self):
        if self.is_moving_up and self.body.y > 0:
            self.body.y -= PLAYER_SPEED
        if self.is_moving_down and self.body.y < GAME_HEIGHT - PLAYER_SIZE:
            self.body.y += PLAYER_SPEED
        if self.is_moving_left and self.body.x > 0:
            self.body.x -= PLAYER_SPEED
        if self.is_moving_right and self.body.x < GAME_WIDTH - PLAYER_SIZE:
            self.body.x += PLAYER_SPEED

    def draw(self, surface):
        pygame.draw.rect(surface, PLAYER_COLOR, self.body)

    def get_obstacle_distances(self, obstacle_grid):
        player_row = self.body.y // GRID_CELL_SIZE
        player_col = self.body.x // GRID_CELL_SIZE
        
        nearest_obstacle_above = None
        nearest_obstacle_below = None
        for obstacle in obstacle_grid.grid[:, player_col]:
            if obstacle and obstacle.body.y + GRID_CELL_SIZE < self.body.y:
                if not nearest_obstacle_above:
                    nearest_obstacle_above = obstacle
                elif obstacle.body.y > nearest_obstacle_above.body.y:
                    nearest_obstacle_above = obstacle
            elif obstacle and self.body.y + PLAYER_SIZE < obstacle.body.y:
                if not nearest_obstacle_below:
                    nearest_obstacle_below = obstacle
                elif obstacle.body.y < nearest_obstacle_below.body.y:
                    nearest_obstacle_below = obstacle
        nearest_obstacle_left = None
        nearest_obstacle_right = None
        for obstacle in obstacle_grid.grid[player_row, :]:
            if obstacle and obstacle.body.x + GRID_CELL_SIZE < self.body.x:
                if not nearest_obstacle_left:
                    nearest_obstacle_left = obstacle
                elif obstacle.body.x > nearest_obstacle_left.body.x:
                    nearest_obstacle_left = obstacle
            elif obstacle and self.body.x + PLAYER_SIZE < obstacle.body.x:
                if not nearest_obstacle_right:
                    nearest_obstacle_right = obstacle
                elif obstacle.body.x < nearest_obstacle_right.body.x:
                    nearest_obstacle_right = obstacle

        # characteristics of obstacle above
        if nearest_obstacle_above == None:
            space_above = self.body.y
            above_y = 0
        else:
            space_above = self.body.y - (nearest_obstacle_above.body.y + GRID_CELL_SIZE)
            above_y = nearest_obstacle_above.body.y + GRID_CELL_SIZE
        # characteristics of obstacle below
        if nearest_obstacle_below == None:
            space_below = GAME_HEIGHT - (self.body.y + PLAYER_SIZE) 
            below_y = GAME_HEIGHT
        else:
            space_below = nearest_obstacle_below.body.y - (self.body.y + PLAYER_SIZE)
            below_y = nearest_obstacle_below.body.y
        # characteristics of obstacle to left
        if nearest_obstacle_left == None:
            space_to_left = self.body.x
            left_x = 0
        else:
            space_to_left = self.body.x - (nearest_obstacle_left.body.x + GRID_CELL_SIZE)
            left_x = nearest_obstacle_left.body.x + GRID_CELL_SIZE
        # characteristics of obstacle to right
        if nearest_obstacle_right == None:
            space_to_right = GAME_WIDTH - (self.body.x + GRID_CELL_SIZE)
            right_x = GAME_WIDTH
        else:
            space_to_right = nearest_obstacle_right.body.x - (self.body.x + PLAYER_SIZE)
            right_x = nearest_obstacle_right.body.x
        
        return space_above, space_below, space_to_left, space_to_right, above_y, below_y, left_x, right_x
        

            
