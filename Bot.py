from stable_baselines3 import PPO
from GameEnv import GameEnv
from Replay import Replay
from BotMeta import BotMeta
import os
import pickle

class Bot:
    baseFolder: str = "Bots"
    modelPath: str
    metaPath: str
    model: PPO = None
    meta: BotMeta = None

    def __init__(self, name: str, preGenHeight=1000, elimBelPlatform=100, max_platforms=5, tickrate=10, ent_coef=0.1):
        """
        Initializes the bot with the environment and model path.
        """
        os.makedirs(self.baseFolder, exist_ok=True)
        self.modelPath = os.path.join(self.baseFolder, name + ".zip")
        self.metaPath = os.path.join(self.baseFolder, name + ".pkl")

        if os.path.exists(self.modelPath):
            # load existing (assumes meta exists as well)
            self.meta = pickle.load(open(self.metaPath, "rb"))
            self.meta.preGenHeight = preGenHeight
            self.meta.elimBelPlatform = elimBelPlatform
            self.meta.max_platforms = max_platforms
            self.meta.tickrate = tickrate
            self.meta.ent_coef = ent_coef
            self.model = PPO("MlpPolicy", self.meta.getEnv(), verbose=1, ent_coef=self.meta.ent_coef)
            self.model.set_parameters(self.modelPath)
        else:
            self.meta = BotMeta(preGenHeight, elimBelPlatform, max_platforms, tickrate, ent_coef)
            self.model = PPO("MlpPolicy", self.meta.getEnv(), verbose=1,ent_coef=self.meta.ent_coef)

    def train(self, steps=1000, sessions: int = 1, record: bool = False):
        """
        Trains the bot using the PPO algorithm.
        """
        for _ in range(sessions):
            self.model.learn(steps, log_interval=100, progress_bar=True)
            self.meta.trainedSteps += steps
            if record:
                replay = self.play(steps, seed=0)
                replay.name = f"{self.meta.trainedSteps/1000}k"
                self.meta.replays[self.meta.trainedSteps] = replay
            
        self.save()

    def play(self, max_steps, seed=None) -> Replay:
        """
        Runs the bot in the environment for evaluation.
        """
        env = self.meta.getEnv()
        obs, info = env.reset(seed)
        replay = Replay(env.game.seed,env.preGenHeight, env.elimBelPlatform, env.tickrate)
        for step in range(max_steps):
            action, _ = self.model.predict(obs, deterministic=True)
            replay.actions.append(int(action))
            obs, reward, terminated, truncated, info = env.step(action)
            if terminated or truncated:
                break
        print(f"Finished after {step + 1} steps.")
        print(f"Score: {env.game.elim_y:.0f}")
        return replay

    def save(self):
        """
        Saves the trained model to the specified path.
        """
        if self.model is None:
            raise ValueError("Model not trained. Train the model before saving.")
        self.model.save(self.modelPath)
        pickle.dump(self.meta, open(self.metaPath, "wb"))



# Example usage
if __name__ == "__main__":
    bot = Bot("Short",GameEnv(250, 0, 2, 10)) # only see current and next platform, 0.2 entropy
    bot.train(2000000)
    replay = bot.play(1000)
    replay.play(1)