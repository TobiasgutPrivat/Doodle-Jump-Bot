from RenderGame import drawGame, drawWorld, set_size, drawPlayer, drawScores
import pygame
from Game import Game

class Replay:
    name: str
    tickrate: int
    seed: int
    preGenHeight: int
    elimBelPlatform: int
    actions: list[str] # 1 action per tick

    def __init__(self, seed=None, preGenHeight=100, elimBelPlatform=100, tickrate=60):
        self.preGenHeight = preGenHeight
        self.elimBelPlatform = elimBelPlatform
        self.tickrate = tickrate
        self.seed = seed
        self.actions = []

    def play(self, xSpeed: int):
            game = Game(self.seed, self.preGenHeight, self.elimBelPlatform, self.tickrate)

            # Set window
            pygame.display.set_caption("Doodle Jump")
            set_size((game.width, game.height))
            clock = pygame.time.Clock()

            for action in self.actions:
                clock.tick(self.tickrate*xSpeed)
                for event in pygame.event.get():
                    if event.type == pygame.QUIT:
                        break
                game.step(action)
                drawGame(game)

def playComparison(replays: list[Replay], xSpeed: int = 1):
    """
    assumes same game parameters
    """
    games: list[tuple[Replay,Game]] = [(replay,Game(replay.seed, replay.preGenHeight, replay.elimBelPlatform, replay.tickrate, replay.name)) for replay in replays]
    display_game = Game(replays[0].seed, 1000) # used to draw base
    max_y = display_game.max_y

    # Set window
    pygame.display.set_caption("Doodle Jump")
    set_size(display_game.width, display_game.height)

    clock = pygame.time.Clock()

    step = 0

    while games:
        clock.tick(replays[0].tickrate*xSpeed)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                break

        drawWorld(display_game, max_y)
        for i, g in enumerate(games):
            replay, game = g
            if len(replay.actions) <= step:
                games.pop(i)
            else:
                # first draw
                drawPlayer(game.player)
                #then step
                game.step(replay.actions[step])
                max_y = max(max_y, game.max_y)
                display_game.genPlatforms(max_y + 1000)

        drawScores([game.player for _, game in games])
        pygame.display.flip()

        step += 1