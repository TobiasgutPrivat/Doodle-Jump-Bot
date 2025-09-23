import pygame
from Game import Game

pygame.init()

background_image = pygame.image.load("Assets/Background.png")
platform_image = pygame.image.load("Assets/Platforms/Platform.png")
player_image = pygame.image.load("Assets/Player/Left.png")
font = pygame.font.Font("Assets/DoodleJump.ttf", 36)

def drawGameState(game: Game, screen: pygame.Surface):
    screenHeight = screen.get_height()
    display_y = game.max_y - screenHeight * 0.4

    # Clear screen
    screen.blit(background_image, (0, 0))

    # Draw platforms
    for platform in game.platforms:
        screen.blit(platform_image, (platform.x, screenHeight-(platform.y-display_y)-platform.height))

    # Draw player
    screen.blit(player_image, (game.player.x - 15, screenHeight-(game.player.y-display_y)-game.player.height))

    # Draw Score
    score_text = font.render(f"{game.player.y:.0f}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

    pygame.display.flip()
