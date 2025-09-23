from RenderGame import drawGameState
import pygame
import os
import pickle as pkl
from Game import Game

class Replay:
    tickrate: int
    seed: int
    actions: list[str] # 1 action per tick

    def __init__(self, tps, seed):
        self.tickrate = tps
        self.seed = seed
        self.actions = []

    def play(self, xSpeed: int):
            game = Game(seed=self.seed, tickrate=self.tickrate)
            pygame.init()
            screen = pygame.display.set_mode((game.width, game.height))

            # Set the title of the window
            pygame.display.set_caption("Doodle Jump")

            running = True
            clock = pygame.time.Clock()

            while running:
                clock.tick(self.tickrate*xSpeed)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        running = False
                game.step(self.actions.pop(0))
                drawGameState(game, screen)

def watchReplay(path, xSpeed: int):
    if path.endswith(".pkl"):
        with open(path, "rb") as f:
            replay = pkl.load(f)
        replay.play(xSpeed)
    elif os.path.isdir(path):
        files = [f for f in os.listdir(path) if f.endswith(".pkl")]
        replays = []
        for file in files:
            with open(os.path.join(path, file), "rb") as f:
                replays.append(pkl.load(f))
        for replay in replays:
            replay.play(xSpeed) #TODO play multiple replays at once
    else:
        raise ValueError("Invalid path. Expect pkl file or folder with pkl files.")

if __name__ == "__main__":
    watchReplay("Bots/Andrew/replay/Run 1/0.pkl", 2)
    # watchReplay("Bots/Andrew/train/Session 2/487.pkl", 2)