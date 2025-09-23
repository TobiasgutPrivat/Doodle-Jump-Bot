from Game import Game
from gymnasium import spaces, Env
import numpy as np
import math

class GameEnv(Env): # or VecEnv possible
    lastHight = 0

    def __init__(self):
        super().__init__()
        
        self.max_platforms = 3

        self.observation_space = spaces.Box(
            low=np.array([
                -1,     # player vy
                *([-1, -1] * self.max_platforms)
            ], dtype=np.float32),
            high=np.array([
                1, # player vy
                *([1, 1] * self.max_platforms)
            ], dtype=np.float32),
            dtype=np.float32
        )


        self.action_space = spaces.Discrete(3)

    def getState(self):
        state = [self.game.player.vy / Game.maxSpeed]

        for p in self.game.platforms[:self.max_platforms]:
            state.extend([
                ((p.x - self.game.player.x + 1)/(Game.width/2)) % 2 - 1, # x relative to player in [-200,200] (use closer direction)
                ((p.y - self.game.player.y) / (Game.preGenHeight + Game.maxJump)) - 1
            ])

        return state

    def reset(self, seed=None):
        self.game = Game(seed=seed) # changing Game properties do effect the outcome
        return self.getState(), {}

    def step(self, action):
        reward = self.game.elim_y - self.lastHight # reward for reaching higher platforms ~50-100 per succesfull jump
        # reward += 100 - min([math.sqrt(p.x**2 + p.y**2) for p in self.game.platforms[:self.max_platforms]]) / 20 # reward for beeing close to a platform (maybe remove when decent)
        self.lastHight = self.game.elim_y
        self.game.step(int(action))
        return self.getState(), reward, self.game.done, False, {}