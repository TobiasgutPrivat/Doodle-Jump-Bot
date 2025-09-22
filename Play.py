from Game import Game
from RenderGame import renderGameState
import pygame

def playGame():
    game = Game()
    running = True
    fps = 60
    steps = 0

    pygame.init()
    screen = pygame.display.set_mode((game.width, game.height))

    while running:
        clock = pygame.time.Clock()
        clock.tick(fps)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
        
        keys = pygame.key.get_pressed()

        timeSinceLastStep = pygame.time.get_ticks() - (steps / game.tickrate * 1000)
        if timeSinceLastStep >= 1000 / game.tickrate:
            # do a game step
            action = None
            if keys[pygame.K_LEFT]:
                action = "left"
            elif keys[pygame.K_RIGHT]:
                action = "right"

            game.step(action)
            running = not game.done
            steps += 1

        renderGameState(game, screen)

    pygame.quit()


if __name__ == "__main__": playGame()