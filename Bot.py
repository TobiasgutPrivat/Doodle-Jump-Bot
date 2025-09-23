from stable_baselines3 import PPO
from GameEnv import GameEnv
import os

class Bot:
    baseFolder: str = "Bots"
    folder: str
    trainFolder: str
    modelPath: str
    name: str
    env: GameEnv
    model: PPO = None

    def __init__(self, name: str):
        """
        Initializes the bot with the environment and model path.
        """
        self.env = GameEnv(True)
        self.name = name

        #Folderstructure
        os.makedirs(self.baseFolder, exist_ok=True)
        self.folder = os.path.join(self.baseFolder, name)
        os.makedirs(self.folder, exist_ok=True)
        self.trainFolder = os.path.join(self.folder, "train")
        os.makedirs(self.trainFolder, exist_ok=True)
        self.replayFolder = os.path.join(self.folder, "replay")
        os.makedirs(self.replayFolder, exist_ok=True)
        self.modelPath = os.path.join(self.folder, "model.zip")

    def train(self, total_timesteps=1000):
        """
        Trains the bot using the PPO algorithm.
        """
        if not self.model:
            self.model = PPO("MultiInputPolicy", self.env, verbose=1)
        self.model.learn(total_timesteps=total_timesteps)
        session_count = len([1 for name in os.listdir(self.trainFolder) if os.path.isdir(os.path.join(self.trainFolder, name))])
        sessionPath = os.path.join(self.trainFolder, f"Session {session_count+1}")
        os.makedirs(sessionPath, exist_ok=True)
        self.env.dumpReplays(sessionPath)
        print("Training complete.")

    def play(self, max_steps):
        """
        Runs the bot in the environment for evaluation.
        """
        if self.model is None:
            raise ValueError("Model not loaded. Train or load a model first.")

        obs, info = self.env.reset()
        for step in range(max_steps):
            action, _ = self.model.predict(obs)
            obs, reward, terminated, truncated, info = self.env.step(action)
            if terminated or truncated:
                print(f"Finished after {step + 1} steps.")
                print(f"Score: {reward}")
                run_count = len([1 for name in os.listdir(self.trainFolder) if os.path.isdir(os.path.join(self.trainFolder, name))])
                runFolder = os.path.join(self.replayFolder, f"Run {run_count+1}")
                os.makedirs(runFolder, exist_ok=True)
                self.env.dumpReplays(runFolder)
                break

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
        if not os.path.exists(self.modelPath):
            raise FileNotFoundError(f"No model found at {self.modelPath}. Train and save a model first.")
        self.model = PPO.load(self.modelPath, env=self.env)
        print(f"Model loaded from {self.modelPath}.")

# Example usage
if __name__ == "__main__":
    bot = Bot("Andrew")

    # Train the bot
    bot.train(total_timesteps=10000)

    # Save the trained model
    bot.save()

    # Load the model
    bot.load()

    # Let the bot play
    bot.play(1000)