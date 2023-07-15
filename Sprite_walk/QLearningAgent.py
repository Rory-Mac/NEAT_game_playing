import random
import numpy as np
import pygame
from pygame.locals import *


START_STATE = 0
GOAL_STATE = 21
NUM_ACTIONS = 4
TRAINING_EPISODES = 1000
LEARNING_RATE = 0.1
DISCOUNT_FACTOR = 0.9
EPSILON = 0.1
IMAGE_SCALE_FACTOR = 80

class QLearningAgent:
    def __init__(self, map, display):
        self.display = display
        self.map = map
        self.num_rows, self.num_cols = map.shape
        self.current_state = START_STATE
        self.q_table = np.zeros((self.num_rows * self.num_cols, NUM_ACTIONS))

    def is_lost(self):
        return self.current_state != GOAL_STATE

    def train(self):
        for _ in range(TRAINING_EPISODES):
            self.current_state = START_STATE
            while self.is_lost():
                action = self.get_action()
                self.move(action)

    def follow_optimal_policy(self):
        self.current_state = START_STATE
        path = []
        while self.is_lost():
            path.append(self.current_state)
            action = self.get_greedy_action()
            self.move(action)
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

        if action == 0 and row > 0 and self.map[row - 1, col] != 1:
            next_state = self.current_state - self.num_cols  # Move up
        elif action == 1 and row < self.num_rows - 1 and self.map[row + 1, col] != 1:
            next_state = self.current_state + self.num_cols  # Move down
        elif action == 2 and col > 0 and self.map[row, col - 1] != 1:
            next_state = self.current_state - 1  # Move left
        elif action == 3 and col < self.num_cols - 1 and self.map[row, col + 1] != 1:
            next_state = self.current_state + 1  # Move right
        else:
            next_state = self.current_state # Invalid move

        # Calculate the reward
        reward = -1 if next_state != self.current_state else -10
        self.update_q_table(action, reward, next_state)
        self.draw(display, next_state)
        self.current_state = next_state

    def update_q_table(self, action, reward, next_state):
        current_q = self.q_table[self.current_state, action]
        max_next_q = np.max(self.q_table[next_state])
        new_q = (1 - LEARNING_RATE) * current_q + LEARNING_RATE * (reward + DISCOUNT_FACTOR * max_next_q)
        self.q_table[self.current_state, action] = new_q

    def draw(self, display, next_state):
        
        pass

class Game:
    

if __name__ == "__main__":
    map = np.array([
        [0, 0, 0, 0, 0],
        [1, 1, 0, 1, 0],
        [0, 0, 0, 0, 0],
        [1, 0, 1, 0, 1],
        [0, 0, 0, 0, 0]])

    pygame.init()
    display = pygame.display.set_mode((map.shape[0] * IMAGE_SCALE_FACTOR, map.shape[1] * IMAGE_SCALE_FACTOR))
    floor_image = pygame.image.load("floor.png")
    wall_image = pygame.image.load("wall.png")
    floor_image = pygame.transform.scale(floor_image, (IMAGE_SCALE_FACTOR, IMAGE_SCALE_FACTOR))
    wall_image = pygame.transform.scale(wall_image, (IMAGE_SCALE_FACTOR, IMAGE_SCALE_FACTOR))
    for i, row in enumerate(map):
        for j, element in enumerate(row):
            if element:
                display.blit(wall_image, (j * IMAGE_SCALE_FACTOR, i * IMAGE_SCALE_FACTOR))
            else:
                display.blit(floor_image, (j * IMAGE_SCALE_FACTOR, i * IMAGE_SCALE_FACTOR))
    pygame.display.flip()
    running = True
    while running:
        # Event handling
        for event in pygame.event.get():
            if event.type == QUIT:
                running = False

    agent = QLearningAgent(map, display)
    agent.train()
    agent.follow_optimal_policy()