import pygame
from Game import Game

def drawGameState(game: Game, screen):
    bottom_height = game.elim_y

    # Clear screen
    screen.fill((135, 206, 235))  # Sky blue background

    # Draw platforms
    for platform in game.platforms:
        pygame.draw.rect(screen, (0, 255, 0), pygame.Rect(platform.x, game.height+bottom_height-platform.y-platform.height, platform.width, platform.height))

    # Draw player
    pygame.draw.rect(screen, (255, 0, 0), pygame.Rect(game.player.x, game.height+bottom_height-game.player.y-game.player.height, game.player.width, game.player.height))

    # Draw Score
    font = pygame.font.Font(None, 36)
    score_text = font.render(f"{game.player.y:.0f}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    pygame.display.flip()
