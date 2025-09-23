from Game import Game
from Replay import Replay
import gymnasium as gym
from gymnasium import spaces
import pickle as pkl
import numpy as np
import os
from numpy import ndarray

class GameEnv(gym.Env): # or VecEnv possible
    record: bool
    replays: list[Replay] = []

    def __init__(self, record=False):
        self.record = record

        super(GameEnv, self).__init__()
        
        # Example: state = 4 floats, action = 3 discrete moves
        self.max_platforms = 5   # next 5 platforms
        item_dim = 2    # (x, y) coordinates

        self.observation_space = spaces.Dict({
            "player_state": spaces.Box(low=-np.inf, high=np.inf, shape=(3,), dtype=np.float32),
            "platforms": spaces.Box(low=-np.inf, high=np.inf, shape=(self.max_platforms, item_dim), dtype=np.float32)
        })

        self.action_space = spaces.Discrete(3)

    def getState(self):
        return {
            "player_state": np.array([self.game.player.x, self.game.player.y, self.game.player.vy]),
            "platforms": np.array([[p.x, p.y-self.game.player.y] for p in self.game.platforms[:self.max_platforms]])
        }

    def reset(self, seed=None):
        # Reset game state
        self.game = Game(seed=seed)
        # maybe: self.game.preGenHeight = 500
        if self.record:
            self.replays.append(Replay(self.game.tickrate, self.game.seed))
        
        return self.getState(), {}

    def step(self, action: ndarray):
        # Apply action
        action: int = int(action)
        self.game.step(action)

        if self.record:
            self.replays[-1].actions.append(action)
            
        # Get state
        state = self.getState()
        reward = self.game.elim_y  
        terminated = self.game.done
        truncated = False

        return state, reward, terminated, truncated, {}
    
    def dumpReplays(self, folder):
        for i, replay in enumerate(self.replays):
            with open(os.path.join(folder, f"{i}.pkl"), "wb") as f:
                pkl.dump(replay, f)

        self.replays = []