import random
import numpy as np
import pygame
from pygame.locals import *

START_STATE = 0
GOAL_STATE = 119
NUM_ACTIONS = 4
TRAINING_EPISODES = 1000
LEARNING_RATE = 0.1
DISCOUNT_FACTOR = 0.9
EPSILON = 0.1
IMAGE_SCALE_FACTOR = 40
MAX_FRAME_RATE = 60
VISUALISE = False

class QLearningAgent:
    def __init__(self, game):
        self.game = game
        self.num_rows, self.num_cols = map.shape
        self.current_state = START_STATE
        self.q_table = np.zeros((self.num_rows * self.num_cols, NUM_ACTIONS))

    def is_lost(self):
        return self.current_state != GOAL_STATE

    def train(self):
        for episode in range(TRAINING_EPISODES):
            self.current_state = START_STATE
            while self.is_lost():
                action = self.get_action()
                self.move(action)
                if VISUALISE: 
                    self.game.clock.tick(MAX_FRAME_RATE)
                    pygame.display.flip()
            if VISUALISE: self.draw_tile(GOAL_STATE)
            if episode % 100 == 0:
                print(f"Training episode {episode} complete")

    def follow_optimal_policy(self):
        self.current_state = START_STATE
        path = []
        while self.is_lost():
            path.append(self.current_state)
            action = self.get_greedy_action()
            self.move(action)
            if VISUALISE:
                self.game.clock.tick(MAX_FRAME_RATE)
                pygame.display.flip()
        path.append(GOAL_STATE)
        print("Shortest path:", path)

    def get_action(self):
        # determine if agent will explore or exploit
        if random.uniform(0, 1) < EPSILON:
            action = random.randint(0, NUM_ACTIONS - 1)
        else:
            action = np.argmax(self.q_table[self.current_state])
        return action

    def get_greedy_action(self):
        return np.argmax(self.q_table[self.current_state])
    
    def move(self, action):
        # Perform the action and observe the next state and reward
        row = self.current_state // self.num_cols
        col = self.current_state % self.num_cols

        if action == 0 and row > 0 and self.game.map[row - 1, col] != 1:
            next_state = self.current_state - self.num_cols  # Move up
        elif action == 1 and row < self.num_rows - 1 and self.game.map[row + 1, col] != 1:
            next_state = self.current_state + self.num_cols  # Move down
        elif action == 2 and col > 0 and self.game.map[row, col - 1] != 1:
            next_state = self.current_state - 1  # Move left
        elif action == 3 and col < self.num_cols - 1 and self.game.map[row, col + 1] != 1:
            next_state = self.current_state + 1  # Move right
        else:
            next_state = self.current_state # Invalid move

        # Calculate the reward
        reward = -1 if next_state != self.current_state else -10
        self.update_q_table(action, reward, next_state)
        if VISUALISE: self.draw(next_state)
        self.current_state = next_state

    def update_q_table(self, action, reward, next_state):
        current_q = self.q_table[self.current_state, action]
        max_next_q = np.max(self.q_table[next_state])
        new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT_FACTOR * max_next_q)
        self.q_table[self.current_state, action] = new_q

    def draw_tile(self, state):
        row = state // self.num_rows
        col = state % self.num_cols
        if self.game.map[row][col]:
            self.game.display.blit(self.game.wall_image, (col * IMAGE_SCALE_FACTOR, row * IMAGE_SCALE_FACTOR))
        else:
            self.game.display.blit(self.game.floor_image, (col * IMAGE_SCALE_FACTOR, row * IMAGE_SCALE_FACTOR))

    def draw(self, next_state):
        self.draw_tile(self.current_state)
        next_row = next_state // self.num_rows
        next_col = next_state % self.num_cols
        self.game.display.blit(self.game.player_image, (next_col * IMAGE_SCALE_FACTOR, next_row * IMAGE_SCALE_FACTOR))

class Game:
    def __init__(self, map):
        self.map = map
        self.display = pygame.display.set_mode((map.shape[0] * IMAGE_SCALE_FACTOR, map.shape[1] * IMAGE_SCALE_FACTOR))
        self.floor_image = pygame.transform.scale(pygame.image.load("floor.png"), (IMAGE_SCALE_FACTOR, IMAGE_SCALE_FACTOR))
        self.wall_image = pygame.transform.scale(pygame.image.load("wall.png"), (IMAGE_SCALE_FACTOR, IMAGE_SCALE_FACTOR))
        self.player_image = pygame.transform.scale(pygame.image.load("player.png"), (IMAGE_SCALE_FACTOR, IMAGE_SCALE_FACTOR))
        self.clock = pygame.time.Clock()

    def draw(self):
        for i, row in enumerate(self.map):
            for j, element in enumerate(row):
                if element:
                    self.display.blit(self.wall_image, (j * IMAGE_SCALE_FACTOR, i * IMAGE_SCALE_FACTOR))
                else:
                    self.display.blit(self.floor_image, (j * IMAGE_SCALE_FACTOR, i * IMAGE_SCALE_FACTOR))
        pygame.display.flip()

if __name__ == "__main__":
    # initialise game and draw game screen
    pygame.init()
    map = np.array([
        [0, 1, 1, 1, 1, 0, 0, 0, 1, 1, 1],
        [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 0],
        [0, 1, 0, 1, 1, 0, 0, 0, 0, 1, 0],
        [0, 0, 0, 1, 0, 0, 1, 0, 1, 0, 0],
        [1, 1, 1, 1, 0, 1, 1, 1, 1, 0, 1],
        [0, 0, 0, 1, 0, 0, 0, 1, 0, 0, 0],
        [0, 1, 0, 0, 0, 0, 1, 0, 0, 1, 0],
        [0, 1, 1, 1, 1, 1, 1, 0, 1, 0, 1],
        [0, 1, 0, 0, 0, 0, 1, 0, 0, 0, 1],
        [0, 0, 0, 1, 1, 0, 0, 1, 1, 0, 1],
        [1, 1, 0, 0, 0, 1, 0, 0, 1, 0, 1],
    ])
    game = Game(map)
    if VISUALISE: game.draw()
    # run agent training
    agent = QLearningAgent(game)
    agent.train()
    agent.follow_optimal_policy()
    # quit game
    pygame.quit()