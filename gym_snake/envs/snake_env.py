import pygame, sys
import numpy as np

import gym
from gym import error, spaces, utils
from gym.utils import seeding

class SnakeEnv(gym.Env):
    def __init__(self):
        pygame.init()

        self.position  = [[200, 200]]
        self.tail      = []
        self.blockSize = 20
        self.direction = 0

        self.score        = 0
        self.n_actions    = 4
        self.done         = False
        
        self.screenHeight = 720
        self.screenWidth  = 1280
        self.snakeColor   = (0, 255, 0)
        self.foodColor    = (255, 0, 0)
        self.newFood()

    def step(self, action):
        self.direction = action

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
        screen = pygame.display.set_mode((self.screenWidth, self.screenHeight))
        screen.fill((255, 255, 255))
        for i in self.position:
            pygame.draw.rect(screen, self.snakeColor, [i[0], i[1], self.blockSize, self.blockSize])

        pygame.draw.rect(screen, self.foodColor, [self.foodPosition[0], self.foodPosition[1], self.blockSize, self.blockSize])
        pygame.display.update()

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
            self.position.append(self.position[0].copy())
            self.newFood()
            return True

        return False

    def getState(self):
        x    = self.foodPosition
        y    = self.position[0]
        z    = self.position
        size = self.blockSize
        return [self.direction,
                x[0] < y[0],
                x[1] < y[1],
                x[0] == y[0],
                x[1] == y[1],
                int([y[0] - size, y[1]] in z),
                int([y[0] + size, y[1]] in z),
                int([y[0], y[1] - size] in z),
                int([y[0], y[1] + size] in z)]

    def getReward(self):
        reward = -1
        if (self.checkPosition()):
            reward = 1
        return reward

    def close(self):
        pygame.display.quit()
        pygame.quit()
        sys.exit()