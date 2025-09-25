import pygame
from Game import Game, Platform, Player

#global because pygame is global as well

pygame.init()

background_image = pygame.image.load("Assets/Background.png")
platform_image = pygame.image.load("Assets/Platforms/Platform.png")
player_image = pygame.image.load("Assets/Player/Left.png")
font = pygame.font.Font("Assets/DoodleJump.ttf", 36)
smallfont = pygame.font.Font("Assets/DoodleJump.ttf", 24)

screen = None
startPos: int # the y position in screen of Game-y = 0

def set_size(width, height):
    global screen
    screen = pygame.display.set_mode((width, height))

def drawGame(game: Game): # for singleplayer
    global startPos
    screenHeight = screen.get_height()
    startPos = game.max_y + int(screenHeight * 0.6)

    # Clear screen
    screen.blit(background_image, (0, 0))

    # Draw platforms
    for platform in game.platforms:
        drawPlatform(platform)

    # Draw player
    drawPlayer(game.player)

    # Draw Score
    score_text = font.render(f"{game.player.y:.0f}", True, (0, 0, 0))
    screen.blit(score_text, (10, 10))

def drawWorld(game: Game, display_y: int):
    global startPos
    screenHeight = screen.get_height()
    startPos = display_y + int(screenHeight * 0.6)

    # Clear screen
    screen.blit(background_image, (0, 0))

    # Draw platforms
    for platform in game.platforms:
        drawPlatform(platform)

def drawScores(players: list[Player]):
    for i, player in enumerate(players):
        score_text = smallfont.render(f"{player.name}: {player.y:.0f}", True, (0, 0, 0))
        screen.blit(score_text, (10, 10 + 30 * i))

def drawPlatform(platform: Platform):
    screen.blit(platform_image, (platform.x, startPos-platform.y-platform.height))

def drawPlayer(player: Player):
    if player.name:
        name_text = smallfont.render(player.name, True, (0, 0, 0))
        screen.blit(name_text, (player.x - 15, startPos-player.y-player.height-30))
    screen.blit(player_image, (player.x - 15, startPos-player.y-player.height))