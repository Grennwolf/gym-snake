import pygame, sys, time
import numpy as np

import gym
from gym import error, spaces, utils
from gym.utils import seeding

class SnakeEnv(gym.Env):
    def __init__(self):
        pygame.init()

        self.position  = [[x, y]]
        self.tail      = [[x, y]]
        self.blockSize = blockSize
        self.direction = 0

        self.score        = 0
        self.n_actions    = 4
        self.done         = False
        
        self.screenHeight = 720
        self.screenWidth  = 1280
        self.speed        = speed
        self.screenSize   = (width, height)
        self.snakeColor   = (0, 255, 0)
        self.foodColor    = (255, 0, 0)
        # self.screen       = pygame.display.set_mode(self.screenSize)
        self.newFood()

    def step(self, action):
        self.direction = action

        self.tail = self.position[-1].copy()
        for ind in np.arange(len(self.position) - 1, 0, -1):
            self.position[ind] = self.position[ind - 1].copy()

        if (self.direction == 0):
            self.position[0][0] += self.blockSize
        if (self.direction == 1):
            self.position[0][1] += self.blockSize
        if (self.direction == 2):
            self.position[0][0] -= self.blockSize
        if (self.direction == 3):
            self.position[0][1] -= self.blockSize

        state  = self.getState()
        reward = self.getReward()
        done   = self.done
        return state, reward, done

    def reset(self):
        self.__init__()
        return self.getState()

    def render(self):
        pass

    def newFood(self):
        """Generates new position for food."""
        blockSize = self.blockSize
        height    = self.screenHeight
        width     = self.screenWidth
        self.foodPosition = [blockSize * np.random.randint(0, width / blockSize), blockSize * np.random.randint(0, height / blockSize)]

    def checkPosition(self):
        """Check if game over or food eaten."""
        headPosition = self.position[0]
        height       = self.screenHeight
        width        = self.screenWidth
        if headPosition[0] < 0 or headPosition[0] > width:
            self.done = True
        if headPosition[1] < 0 or headPosition[1] > height:
            self.done = True

        if len(np.unique(self.position, axis = 0)) != len(self.position):
            self.done = True
        if headPosition == self.foodPosition:
            self.score += 1
            self.position.append(self.tail.copy())
            self.newFood()
            return True

        return False

    def getState(self):
        x    = self.foodPosition
        y    = self.position[0]
        z    = self.position
        size = self.blockSize
        return [x[0] <= y[0], x[1] >= y[1], x[0] == y[0], x[1] == y[1], self.direction, int([y[0] - size, y[1]] in z), int([y[0] + size, y[1]] in z), int([y[0], y[1] - size] in z), int([y[0], y[1] + size] in z)]

    def getReward(self):
        reward = -1
        if (self.checkPosition()):
            reward = 0.5
        return reward

    def close(self):
        pass