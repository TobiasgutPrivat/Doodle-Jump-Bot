import random
from bisect import bisect_left

class Player:
    x: float # bottom
    y: float # left
    vy: float # vertical speed upwards
    width: int = 30 # hitbox width
    height: int = 60 # image height

    def __init__(self, x, y, vy=0):
        self.x = x
        self.y = y
        self.vy = vy

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
    width: int # screen width
    height: int # screen height
    elim_y: int = 0 # highest point reached
    max_y: int = 0
    seed: int # deterministic seed for world generation
    player: Player
    platforms: list[Platform] = [] # maybe: index for y-level
    platformGen: random.Random
    #monsters
    
    steps: int

    tickrate: int # theoretical ticks per second
    preGenHeight: int = 1000 # how much to pre-generate platforms above the screen
    g = -500 # gravity px/s^2
    moveSpeed = 150 # px/s
    jumpSpeed = 450 # px/s

    def __init__(self, width=400, height=600, seed=None, tickrate=5):
        if seed is None:
            seed = random.randint(0, 2**32 - 1)
        self.seed = seed

        # init positions
        self.width = width
        self.height = height
        middle_x = width // 2

        # init objects
        self.player = Player(middle_x-Player.width/2, height/5)
        self.platforms = [Platform(x=middle_x-Platform.width/2, y=height/10)] # starting platform
        self.platformGen = random.Random(self.seed)
        self.genPlatforms()

        self.tickrate = tickrate
        self.steps = 0

    def genPlatforms(self):
        to_y = self.elim_y + self.preGenHeight
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
            y = last_y + self.platformGen.randint(10, 150)
            self.platforms.append(Platform(x, y))
            last_y = y

    def step(self, action: int):
        """Advance the game by one tick with given action"""
        if self.done:
            return

        # Apply action
        if action == 0:
            pass
        elif action == 1:
            self.player.x -= self.moveSpeed / self.tickrate
        elif action == 2:
            self.player.x += self.moveSpeed / self.tickrate

        self.player.x = (self.player.x + self.player.width/2) % self.width - self.player.width/2 # wrap around screen (use middle of player)

        # Physics
        self.player.vy += self.g / self.tickrate
        old_y = self.player.y
        self.player.y += self.player.vy / self.tickrate

        # Update highest point
        if self.player.y > self.max_y:
            self.max_y = self.player.y

        if self.player.vy <= 0:
            self.checkCollision(old_y)

        # Game over condition
        if self.player.y < self.elim_y:
            self.done = True

        self.steps += 1

    def checkCollision(self, old_y):
        # Collision with platform
        platforms_below = [p for p in self.platforms if p.y + p.height/2 < old_y]
        platforms_passed = [p for p in platforms_below if p.y + p.height >= self.player.y]
        collision_platforms  = [p for p in platforms_passed if 
                            p.x < self.player.x + self.player.width and 
                            self.player.x < p.x + p.width]
    
        if any(collision_platforms):
            self.player.vy = self.jumpSpeed
            self.elim_y = max(self.elim_y, self.player.y - self.height * 0.3)
            self.genPlatforms()
