import pygame
from Game import Game

def renderGameState(game: Game, screen):
    bottom_height = game.elim_y

    # Clear screen
    screen.fill((135, 206, 235))  # Sky blue background

    # Draw player
    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(game.player.x, game.height+bottom_height-game.player.y, game.player.width, game.player.height))

    # Draw platforms
    for platform in game.platforms:
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(platform.x, game.height+bottom_height-platform.y, platform.width, platform.height))
        
    pygame.display.flip()
