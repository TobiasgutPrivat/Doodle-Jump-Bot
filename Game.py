import random
import math
from bisect import bisect_left

class Player:
    name: str
    x: float # bottom
    y: float # left
    vy: float = 0 # vertical speed upwards
    vx: float = 0 # horizontal speed
    width: int = 30 # hitbox width
    height: int = 60 # image height

    def __init__(self, x, y, name=""):
        self.name = name
        self.x = x
        self.y = y

class Platform:
    x: float # bottom
    y: float # left
    width: int = 60 # hitbox/image width
    height: int = 17 # image height

    def __init__(self, x, y):
        self.x = x
        self.y = y

    # can make tick method as well for moving platforms etc. (abstractions)

class Game:
    done: bool = False
    width: int = 400 # screen width
    height: int = 600 # screen height
    elim_y: int = 0 # highest point reached
    max_y: int = 0
    seed: int # deterministic seed for world generation
    player: Player
    platforms: list[Platform] = [] # maybe: index for y-level
    platformGen: random.Random
    #monsters
    
    steps: int

    # default game parameters
    tickrate: int # theoretical ticks per second (in theory should only effect input sensitivity not physics)
    preGenHeight: int # how much to pre-generate platforms above the screen
    g: int = -600 # gravity px/s^2
    moveAcceleration: int = 400 # px/s
    slowdown: float = 0.6 # per second
    maxSpeed: int = 450 # px/s
    elimBelPlatform: int
    maxJump: int = 130

    def __init__(self, seed=None, preGenHeight=1000, elimBelPlatform=100, tickrate=60, name=""):
        if seed is None:
            seed = random.randint(0, 2**32 - 1)
        self.seed = seed
        self.preGenHeight = preGenHeight
        self.elimBelPlatform = elimBelPlatform
        self.tickrate = tickrate

        # init positions
        middle_x = self.width // 2

        # init objects
        self.player = Player(middle_x-Player.width/2, self.height/5,name)
        self.platforms = [Platform(x=middle_x-Platform.width/2, y=self.height/10)] # starting platform
        self.platformGen = random.Random(self.seed)
        self.genPlatforms()

        self.steps = 0

    def genPlatforms(self, height=None):
        to_y = self.elim_y + (height or self.preGenHeight)
        # Remove platforms below elim_y
        index = bisect_left([p.y for p in self.platforms], self.elim_y)
        self.platforms = self.platforms[index:]

        # Start from last platform or elim_y
        if self.platforms:
            last_y = self.platforms[-1].y
        else:
            last_y = self.elim_y
        
        # Generate platforms until reaching to_y
        while last_y < to_y:
            x = self.platformGen.randint(0, self.width - Platform.width)
            y = last_y + self.platformGen.randint(30, self.maxJump)
            self.platforms.append(Platform(x, y))
            last_y = y

    def step(self, action: int): #TODO improve physics for low tickrate
        """Advance the game by one tick with given action"""
        if self.done:
            return

        time = 1 / self.tickrate # seconds
        old_vx = self.player.vx
        old_x = self.player.x
        old_vy = self.player.vy
        old_y = self.player.y

        # Apply action
        if action == 0:
            pass
        elif action == 1:
            self.player.vx -= self.moveAcceleration * time
        elif action == 2:
            self.player.vx += self.moveAcceleration * time

        # Horizontal movement
        self.player.vx *= 1 - (1 - self.slowdown)/self.tickrate # air-friction
        self.player.x += old_vx * time + self.moveAcceleration * (time**2) / 2
        self.player.x = (self.player.x + self.player.width/2) % self.width - self.player.width/2 # wrap around screen (use middle of player)

        # Vertical movement
        self.player.vy = max(self.player.vy + self.g * time, -self.maxSpeed)
        self.player.y += old_vy * time + self.g * (time**2) / 2

        # Update highest point
        if self.player.y > self.max_y:
            self.max_y = self.player.y

        if self.player.vy <= 0:
            if (collided_y := self.checkCollision(old_y)) is not None:
                timeAfterCol = time - (old_vy + math.sqrt(old_vy**2 + 2 * self.g * (collided_y - old_y)))/self.g
                self.player.vy = self.maxSpeed + self.g * timeAfterCol
                self.player.y = collided_y + self.maxSpeed * timeAfterCol + self.g * (timeAfterCol**2) / 2

        # Game over condition
        if self.player.y < self.elim_y:
            self.done = True

        self.steps += 1

    def checkCollision(self, old_y) -> int | None: # return collided at y level
        # Collision with platform
        platforms_below = [p for p in self.platforms if p.y + p.height/2 < old_y]
        platforms_passed = [p for p in platforms_below if p.y + p.height >= self.player.y]
        collision_platforms  = [p for p in platforms_passed if 
                            p.x < self.player.x + self.player.width and 
                            self.player.x < p.x + p.width]
    
        if any(collision_platforms):
            self.player.vy = self.maxSpeed
            collided_platform = sorted(collision_platforms, key=lambda p: p.y)[0]
            self.elim_y = max(self.elim_y, collided_platform.y - self.elimBelPlatform)
            self.genPlatforms()
            return collided_platform.y

        return None
