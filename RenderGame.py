import pygame
from Game import Game

def drawGameState(game: Game, screen):
    bottom_height = game.elim_y

    # Clear screen
    background_image = pygame.image.load("Assets/Background.png")
    screen.blit(background_image, (0, 0))

    # Draw platforms
    for platform in game.platforms:
        platform_image = pygame.image.load("Assets/Platforms/Platform.png")
        screen.blit(platform_image, (platform.x, game.height+bottom_height-platform.y-platform.height))

    # Draw player
    player_image = pygame.image.load("Assets/Player/Left.png")
    screen.blit(player_image, (game.player.x - 15, game.height+bottom_height-game.player.y-game.player.height))

    # Draw Score
    font = pygame.font.Font("Assets/DoodleJump.ttf", 36)
    score_text = font.render(f"{game.player.y:.0f}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))
    pygame.display.flip()
