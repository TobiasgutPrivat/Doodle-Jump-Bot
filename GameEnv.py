import gym
from gym import spaces
import numpy as np
from Game import Game

class GameEnv(gym.Env):
    def __init__(self):
        super(GameEnv, self).__init__()
        
        # Example: state = 4 floats, action = 3 discrete moves
        self.max_items = 5   # next 5 platforms
        item_dim = 2    # (x, y) coordinates

        self.observation_space = spaces.Dict({
            "player_state": spaces.Box(low=-np.inf, high=np.inf, shape=(3,), dtype=np.float32),
            "items": spaces.Box(low=-np.inf, high=np.inf, shape=(self.max_items, item_dim), dtype=np.float32)
        })

        self.action_space = spaces.Discrete(3)

    def getState(self):
        return {
            "player_state": np.array([self.game.player.x, self.game.player.y, self.game.player.vy]),
            "items": np.array([[p.x, p.y-self.game.player.y] for p in self.game.platforms[:self.max_items]])
        }

    def reset(self):
        # Reset game state
        self.game = Game()
        # self.game.preGenHeight = 500
        
        return self.getState()

    def step(self, action):
        # Apply action
        self.game.step(action)

        # Get state
        state = self.getState()
        reward = self.game.player.y  
        done = self.game.done

        return state, reward, done, {}
