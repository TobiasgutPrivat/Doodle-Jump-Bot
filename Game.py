import pygame
import random
# import enum


class Player:
    x: float
    y: float
    vy: float # vertical speed upwards

# class PlatformType(enum.Enum):
#     NORMAL = 0
#     MOVING = 1
#     BREAKABLE = 2

class Platform:
    x: float
    y: float
    # type: PlatformType

class DoodleJump:
    tickrate: int # ticks per second
    width: int
    height: int
    seed: int # deterministic seed for world generation
    player: Player
    platforms: list[Platform] = [] # maybe: index for y-level
    platformGen: random.Random
    #monsters

    def __init__(self, width=400, height=600, tickrate=20, seed=0):
        self.width = width
        self.height = height
        self.tickrate = tickrate
        self.platformGen = random.Random(seed)

    def genPlatforms(self, from_y: int, to_y: int):
        last_y = from_y
        # Remove platforms below from_y
        self.platforms = [p for p in self.platforms if p.y > from_y]

        # Start from last platform or from_y
        if self.platforms:
            last_y = self.platforms[-1].y
        
        # Generate platforms until reaching to_y
        while last_y < to_y:
            x = self.platformGen.randint(0, self.width - 60)
            y = last_y + self.platformGen.randint(50, 150)
            self.platforms.append(Platform(x, y))
            last_y = y

    def step(self, action):
        """Advance the game by one tick with given action"""
        if self.done:
            return self.get_state(), 0, True

        # Apply action
        old_x = self.player.x
        if action == "left":
            self.player.x -= 5
        elif action == "right":
            self.player.x += 5

        # Physics
        self.player.vy += -9.81 / self.tickrate
        old_y = self.player.y
        self.player.y += self.player.vy / self.tickrate

        # Collision with platform
        filter_platforms = [p for p in self.platforms if 
                            old_y + 20 <= p.y <= self.player.y + 20 and 
                            p.x <= self.player.x + 20 <= p.x + 60 and self.player.vy <= 0]
        if any(filter_platforms):
            self.player.vy = 100

        # Game over condition
        if self.player.y > self.height:
            self.done = True

        return self.get_state(), self.player.y, self.done

    def get_state(self):
        """Return abstract state (for AI)"""
        return {
            "player_x": self.player.x,
            "player_y": self.player.y,
            "player_vy": self.player.vy,
            "platforms": self.platforms,
        }
