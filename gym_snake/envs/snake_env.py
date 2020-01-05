import gym
import numpy as np

from gym import error, spaces, utils
from gym.utils import seeding


class SnakeEnv(gym.Env):
    def __init__(self):
        self.position = [[200, 200]]
        self.blockSize = 10
        self.direction = 0

        self.score = 0
        self.done = False

        self.action_space = spaces.Discrete(4)
        self.observation_space = spaces.Box(np.empty(9, ), np.empty(9, ))

        self.foodPosition = None

        self.screenHeight = 400
        self.screenWidth = 400
        self.screenColor = [255, 255, 255]
        self.snakeColor = [0, 255, 0]
        self.foodColor = [255, 0, 0]
        self.new_food()

    def step(self, action):
        if not self.done:
            self.direction = action

            for ind in np.arange(len(self.position) - 1, 0, -1):
                self.position[ind] = self.position[ind - 1].copy()

            if self.direction == 0:
                self.position[0][0] += self.blockSize
            if self.direction == 1:
                self.position[0][1] += self.blockSize
            if self.direction == 2:
                self.position[0][0] -= self.blockSize
            if self.direction == 3:
                self.position[0][1] -= self.blockSize

        state = self.get_state()
        reward = self.get_reward()
        done = self.done
        return state, reward, done, None

    def reset(self):
        self.__init__()
        return self.get_state()

    def render(self, mode='human'):
        screen = np.zeros((self.screenHeight, self.screenWidth, 3), dtype=int)
        screen[:, :] = self.screenColor

        for i in self.position:
            screen[i[0]:i[0] + self.blockSize,
                   i[1]:i[1] + self.blockSize] = self.snakeColor

        screen[self.foodPosition[0]:self.foodPosition[0] + self.blockSize,
               self.foodPosition[1]:self.foodPosition[1] + self.blockSize] = self.foodColor

        return screen

    def new_food(self):
        """Generates new position for food."""
        block_size = self.blockSize
        height = self.screenHeight
        width = self.screenWidth
        self.foodPosition = [block_size * np.random.randint(0, width // block_size),
                             block_size * np.random.randint(0, height // block_size)]

    def check_position(self):
        """Check if game over or food eaten."""
        head_position = self.position[0]
        height = self.screenHeight
        width = self.screenWidth
        if head_position[0] < 0 or head_position[0] > width:
            self.done = True
        if head_position[1] < 0 or head_position[1] > height:
            self.done = True

        if len(np.unique(self.position, axis=0)) != len(self.position):
            self.done = True
        if head_position == self.foodPosition:
            self.score += 1
            self.position.append(self.position[0].copy())
            self.new_food()
            return True

        return False

    def get_state(self):
        x = self.foodPosition
        y = self.position[0]
        z = self.position
        size = self.blockSize
        state = [self.direction,
                 x[0] < y[0],
                 x[1] < y[1],
                 x[0] == y[0],
                 x[1] == y[1],
                 int([y[0] - size, y[1]] in z),
                 int([y[0] + size, y[1]] in z),
                 int([y[0], y[1] - size] in z),
                 int([y[0], y[1] + size] in z)]
        return np.array(state)

    def get_reward(self):
        reward = (1 if self.check_position() else 0)
        return reward

    def close(self):
        pass
