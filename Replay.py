from RenderGame import drawGameState
import pygame
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
            screen = pygame.display.set_mode((game.width, game.height))

            # Set the title of the window
            pygame.display.set_caption("Doodle Jump")

            clock = pygame.time.Clock()

            for action in self.actions:
                clock.tick(self.tickrate*xSpeed)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        break
                game.step(action)
                drawGameState(game, screen)