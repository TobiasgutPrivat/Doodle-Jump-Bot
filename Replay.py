from RenderGame import drawGameState
import pygame
from Game import Game

class Replay:
    tickrate: int
    seed: int
    actions: list[str] = [] # 1 action per tick

    def __init__(self, tps, seed):
        self.tickrate = tps
        self.seed = seed

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