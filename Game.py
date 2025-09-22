import pygame
import random
# import enum


class Player:
    x: float
    y: float
    vy: float # vertical speed

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
    platforms: list[Platform] = []
    platformGen: random.Random
    #monsters

    def __init__(self, width=400, height=600, tickrate=20, seed=0):
        self.width = width
        self.height = height
        self.tickrate = tickrate
        self.platformGen = random.Random(seed)

    def genPlatforms(self, until_y: int):
        last_y = 0
        if self.platforms:
            last_y = self.platforms[-1].y
        
        while last_y < until_y:
            x = self.platformGen.randint(0, self.width - 60)
            y = last_y + self.platformGen.randint(50, 150)
            self.platforms.append(Platform(x, y))
            last_y = y

    def step(self, action, dt=1/20):
        """Advance the game by one tick with given action"""
        if self.done:
            return self.get_state(), 0, True

        # Apply action
        if action == "left":
            self.player["x"] -= 5
        elif action == "right":
            self.player["x"] += 5

        # Physics
        self.player["vy"] += 9.81 * dt
        self.player["y"] += self.player["vy"] * dt

        # Collision with platform
        if self.player["y"] > self.height - 50:
            self.player["vy"] = -300 * dt
            self.score += 1

        # Game over condition
        if self.player["y"] > self.height:
            self.done = True

        return self.get_state(), self.score, self.done

    def get_state(self):
        """Return abstract state (for AI)"""
        return {
            "player_x": self.player["x"],
            "player_y": self.player["y"],
            "player_vy": self.player["vy"],
            "platforms": self.platforms,
            "score": self.score,
        }

    def render(self):
        """Render the game (only if render_mode)"""
        if not self.render_mode:
            return
        self.screen.fill((0, 0, 0))
        # Draw player
        pygame.draw.rect(self.screen, (255, 255, 0),
                         (self.player["x"], self.player["y"], 20, 20))
        # Draw platforms
        for px, py in self.platforms:
            pygame.draw.rect(self.screen, (0, 255, 0), (px, py, 60, 10))
        pygame.display.flip()
        self.clock.tick(60)
