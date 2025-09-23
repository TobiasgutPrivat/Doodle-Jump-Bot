from stable_baselines3 import PPO
from GameEnv import GameEnv
from Replay import Replay
import os

class Bot:
    baseFolder: str = "Bots"
    modelPath: str
    env: GameEnv
    model: PPO = None

    def __init__(self, name: str):
        """
        Initializes the bot with the environment and model path.
        """
        self.env = GameEnv()

        #storage
        os.makedirs(self.baseFolder, exist_ok=True)
        self.modelPath = os.path.join(self.baseFolder, name + ".zip")

    def train(self, total_timesteps=10000):
        """
        Trains the bot using the PPO algorithm.
        """
        if not self.model:
            self.load()

        self.model.learn(total_timesteps, log_interval=5, progress_bar=True)
        self.save()

    def play(self, max_steps) -> Replay:
        """
        Runs the bot in the environment for evaluation.
        """
        if not self.model:
            self.load()

        obs, info = self.env.reset()
        replay = Replay(self.env.game.tickrate, self.env.game.seed)
        for step in range(max_steps):
            action, _ = self.model.predict(obs)
            replay.actions.append(int(action))
            obs, reward, terminated, truncated, info = self.env.step(action)
            if terminated or truncated:
                print(f"Finished after {step + 1} steps.")
                print(f"Score: {reward}")
                return replay

    def save(self):
        """
        Saves the trained model to the specified path.
        """
        if self.model is None:
            raise ValueError("Model not trained. Train the model before saving.")
        self.model.save(self.modelPath)
        print(f"Model saved to {self.modelPath}.")

    def load(self):
        """
        Loads the model from the specified path.
        """
        if os.path.exists(self.modelPath):
            self.model = PPO.load(self.modelPath, env=self.env)
        else:
            self.model = PPO("MultiInputPolicy", self.env, verbose=1)

# Example usage
if __name__ == "__main__":
    bot = Bot("Andrew")

    # bot.train(100000)
    replay = bot.play(1000)
    replay.play(1)