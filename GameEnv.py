from Game import Game
from gymnasium import spaces, Env
import numpy as np

class GameEnv(Env): # or VecEnv possible
    def __init__(self):
        super().__init__()
        
        self.max_platforms = 5   # next 5 platforms

        self.observation_space = spaces.Dict({
            "player_state": spaces.Box(low=-np.inf, high=np.inf, shape=(3,), dtype=np.float32),
            "platforms": spaces.Box(low=-np.inf, high=np.inf, shape=(self.max_platforms, 2), dtype=np.float32)
        })

        self.action_space = spaces.Discrete(3)

    def getState(self):
        return {
            "player_state": np.array([self.game.player.x, self.game.player.y, self.game.player.vy]),
            "platforms": np.array([[p.x, p.y-self.game.player.y] for p in self.game.platforms[:self.max_platforms]])
        }

    def reset(self, seed=None):
        self.game = Game(seed=seed)
        return self.getState(), {}

    def step(self, action):
        self.game.step(int(action))
        return self.getState(), self.game.elim_y, self.game.done, False, {}