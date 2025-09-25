from Replay import Replay, playComparison
from GameEnv import GameEnv

class BotMeta:
    replays: dict[int,Replay] # dict[trainedsteps, replay]
    trainedSteps: int
    preGenHeight: int
    elimBelPlatform: int
    max_platforms: int
    tickrate: int
    ent_coef: float

    def __init__(self, preGenHeight=1000, elimBelPlatform=100, max_platforms=5, tickrate=10, ent_coef=0.1):
        self.replays = dict()
        self.trainedSteps = 0
        self.preGenHeight = preGenHeight
        self.elimBelPlatform = elimBelPlatform
        self.max_platforms = max_platforms
        self.tickrate = tickrate
        self.ent_coef = ent_coef
        
    def getEnv(self):
        return GameEnv(self.preGenHeight, self.elimBelPlatform, self.max_platforms, self.tickrate)
    
    def watch(self, fromStep=0, toStep=None):
        replays = [r for s, r in self.replays.items() if fromStep <= s  and (toStep is None or s <= toStep)]
        playComparison(replays)
