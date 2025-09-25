from Replay import Replay, playComparison
from Bot import Bot
from GameEnv import GameEnv
import pickle

def train():
    replays = []
    for i in range(10):
        bot = Bot("Short",GameEnv(250, 0, 2, 10)) # only see current and next platform, 0.2 entropy
        bot.train(10000)
        replay = bot.play(1000,seed=0)
        replay.name = f"{i+1}0k"
        replays.append(replay)
    pickle.dump(replays, open("replays.pkl", "wb"))

def play():
    replays: list[Replay] = pickle.load(open("replays.pkl", "rb"))
    print([r.seed for r in replays])
    playComparison(replays)

if __name__ == "__main__":
    # train()
    play()
        