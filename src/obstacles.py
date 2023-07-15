from collections import deque
from constants import *
import numpy as np
import pygame

class FallingObstacle:
    def __init__(self, x):
        self.body = pygame.Rect(x, -GRID_CELL_SIZE, GRID_CELL_SIZE, GRID_CELL_SIZE)

    def move(self):
        self.body.y += OBSTACLE_SPEED

    def draw(self, surface):
        pygame.draw.rect(surface, OBSTACLE_COLOR, self.body)

class ObstacleGrid:
    def __init__(self):
        self.grid = np.empty((int(GAME_HEIGHT / GRID_CELL_SIZE) + 1, int(GAME_WIDTH / GRID_CELL_SIZE)), dtype=object)

    def shift_grid_down(self, new_obstacles):
        self.grid = np.vstack((new_obstacles, self.grid[:-1]))

    def __get_player_cell(self, player):
        player_x = int(player.body.x // GRID_CELL_SIZE)
        player_y = int(player.body.y // GRID_CELL_SIZE)
        return player_y, player_x

    def get_grid_as_binary(self):
        binary = []
        for row in self.grid:
            for element in row:
                if element:
                    binary.append(1)
                else:
                    binary.append(0)
        return binary

    def player_path_exists(self, player):
        reachable_end_columns = []
        rows, cols = self.grid.shape
        visited = np.zeros((rows, cols), dtype=bool)
        queue = deque([self.__get_player_cell(player)])
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        while queue:
            row, col = queue.popleft()
            visited[row, col] = True
            if row == 0 and self.grid[row, col] == None:
                reachable_end_columns.append(col)
            for move in moves:
                new_row = row + move[0]
                new_col = col + move[1]
                if 0 <= new_row < rows and 0 <= new_col < cols and not visited[new_row, new_col] \
                    and self.grid[new_row, new_col] == None:
                        queue.append((new_row, new_col))
                        visited[new_row, new_col] = True
        return reachable_end_columns

    def update(self, player, frame_count):
        # update obstacle position for all obstacles in obstacle grid:
        for row in self.grid:
            for obstacle in row:
                if obstacle:
                    obstacle.move()

        # obstacles are added in sync with other obstacles, layer by layer
        if frame_count % (GRID_CELL_SIZE / OBSTACLE_SPEED): return False
        # compute viable indices to place new obstacles
        non_blocking_indices = self.player_path_exists(player)
        # create new obstacles 
        number_new_obstacles = np.random.randint(0, len(non_blocking_indices) - 1)
        new_obstacle_indices = np.random.choice(non_blocking_indices, size=number_new_obstacles, replace=False)
        new_obstacles = np.empty(self.grid.shape[1], dtype=object)
        for index in new_obstacle_indices:
            new_obstacles[index] = FallingObstacle(index * GRID_CELL_SIZE)
        # replace obstacles that have fallen below the screen in previous frame with new non-blocking obstacles
        self.shift_grid_down(new_obstacles)
        # return boolean signal that one layer of obstacles have been passed
        return True

    def collides_with(self, player):
        for row in self.grid:
            for obstacle in row:
                if obstacle and pygame.Rect.colliderect(obstacle.body, player.body):
                    return True
        return False

    def draw(self, surface):
        for row in self.grid:
            for obstacle in row:
                if obstacle:
                    obstacle.draw(surface)