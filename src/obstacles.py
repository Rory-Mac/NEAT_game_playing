import random
import numpy as np
from collections import deque
from constants import *

#----------------------------------------------------------------------
# This section is responsible for obstacle creation and movement
#----------------------------------------------------------------------
class FallingObstacle:
    def __init__(self):
        self.width = random.randint(100, 200)
        self.height = random.randint(100, 400)
        self.x = random.randint(0, SCREEN_WIDTH - self.width)
        self.y = -self.height

    def update(self):
        self.y += OBSTACLE_SPEED

class ObstacleGrid:
    def __init__(self):
        self.grid = np.zeros((int(SCREEN_HEIGHT / GRID_CELL_LENGTH) + 1, int(SCREEN_WIDTH / GRID_CELL_LENGTH)))

    def clear_grid(self):
        self.grid = self.grid.fill(0)

    def add_obstacles(self, obstacles):
        for obstacle in obstacles:
            upper_left_overlap = obstacle.x % GRID_CELL_LENGTH
            lower_left_overlap = obstacle.y % GRID_CELL_LENGTH
            upper_right_overlap = obstacle.x + obstacle.width % GRID_CELL_LENGTH
            lower_right_overlap = obstacle.y + obstacle.height % GRID_CELL_LENGTH
            self.grid[upper_left_overlap:lower_left_overlap, upper_right_overlap:lower_right_overlap] += 1

    def player_path_exists(self, player_x, player_y):
        rows, cols = self.grid.shape
        visited = np.zeros((rows, cols), dtype=bool)
        queue = deque([(player_x, player_y)])
        moves = [(-1, 0), (1, 0), (0, -1), (0, 1)]
        while queue:
            row, col = queue.popleft()
            if row == 0 and self.grid[row, col] == 0:
                return True
            visited[row, col] = True
            for move in moves:
                new_row = row + move[0]
                new_col = col + move[1]
                if 0 <= new_row < rows and 0 <= new_col < cols and not visited[new_row, new_col] \
                    and self.grid[new_row, new_col] == 0:
                        queue.append((new_row, new_col))
                        visited[new_row, new_col] = True
        return False

# # modified DFS determines if current obstacle map blocks player 
# def obstacle_blocks(obstacles):
#     # if left gap exists obstacles are non-blocking
#     leftmost_obstacle = obstacles[0]
#     if leftmost_obstacle.x > PLAYER_WIDTH:
#         return False
#     # start depth-first-search
#     stack = [leftmost_obstacle]
#     visited = set()
#     while stack:
#         current_obstacle = stack.pop()
#         visited.add(current_obstacle)
#         # add overlapping objects to stack
#         for obstacle in obstacles:
#             if obstacle not in visited and obstacle.x >= current_obstacle.x \
#                 and obstacle.x <= current_obstacle.x + current_obstacle.width \
#                 and obstacle.x + obstacle.width >= current_obstacle.x + current_obstacle.width:
#                     stack.append(obstacle)
#         # if stack is empty and no new obstacles discovered check for gaps
#         if not stack:
#             for obstacle in obstacles:
#                 # if player-sized gap exists to next object return non-blocking
#                 if obstacle.x > current_obstacle.x + current_obstacle.width + PLAYER_WIDTH:
#                     return False
#                 # if gap exits but is not player-sized continue DFS
#                 if obstacle.x > current_obstacle.x + current_obstacle.width:
#                     stack.append(obstacle)
#     # check if last obstacle leaves suitable gap
#     if current_obstacle.x + current_obstacle.width >= SCREEN_WIDTH - PLAYER_WIDTH:
#         return True
