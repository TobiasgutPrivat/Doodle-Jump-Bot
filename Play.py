from Game import Game
from RenderGame import drawGameState
from Replay import Replay
import pygame
import asyncio

async def playGame():
    game = Game(tickrate=60)
    replay = Replay(game.tickrate, game.seed)
    running = True
    steps = 0

    screen = pygame.display.set_mode((game.width, game.height))

    # Set the title of the window
    pygame.display.set_caption("Doodle Jump")

    clock = pygame.time.Clock()
    while running:
        clock.tick(game.tickrate)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        keys = pygame.key.get_pressed()

        # do a game step
        action = 0
        if keys[pygame.K_LEFT]:
            action = 1
        elif keys[pygame.K_RIGHT]:
            action = 2

        game.step(action)
        replay.actions.append(action)
        running = not game.done
        steps += 1

        drawGameState(game, screen)

    # run replay
    # replay.play(2)


if __name__ == "__main__": 
    asyncio.run(playGame())