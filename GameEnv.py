from Game import Game
from gymnasium import spaces, Env
import numpy as np

class GameEnv(Env): # or VecEnv possible
    lastHight = 0
    preGenHeight: int
    elimBelPlatform: int
    max_platforms: int
    tickrate: int

    def __init__(self, preGenHeight=100, elimBelPlatform=100, max_platforms=5, tickrate=10):
        super().__init__()
        
        self.preGenHeight = preGenHeight
        self.elimBelPlatform = elimBelPlatform
        self.max_platforms = max_platforms
        self.tickrate = tickrate

        self.observation_space = spaces.Box(
            low=np.array([
                -1,     # player vy
                -1,
                *([-1, -1] * self.max_platforms)
            ], dtype=np.float32),
            high=np.array([
                1, # player vy
                1,
                *([1, 1] * self.max_platforms)
            ], dtype=np.float32),
            dtype=np.float32
        )


        self.action_space = spaces.Discrete(3)

    def getState(self):
        state = [self.game.player.vy / Game.maxSpeed, self.game.player.vx / Game.maxSpeed]

        for p in self.game.platforms[:self.max_platforms]:
            state.extend([
                ((p.x - self.game.player.x + 1)/(Game.width/2)) % 2 - 1, # x relative to player in [-200,200] (use closer direction)
                ((p.y - self.game.player.y) / (self.preGenHeight + self.elimBelPlatform)) - 1
            ])

        return state

    def reset(self, seed=None):
        self.game = Game(seed, self.preGenHeight, self.elimBelPlatform, self.tickrate) # changing Game properties do effect the outcome
        
        self.lastHight = 0
        return self.getState(), {}

    def step(self, action):
        reward = self.game.elim_y - self.lastHight # reward for reaching higher platforms ~50-100 per succesfull jump
        self.lastHight = self.game.elim_y
        self.game.step(int(action))
        return self.getState(), reward, self.game.done, False, {}