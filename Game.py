import random

class Player:
    x: float # bottom
    y: float # left
    vy: float # vertical speed upwards
    width: int = 20
    height: int = 20

    def __init__(self, x, y, vy=0):
        self.x = x
        self.y = y
        self.vy = vy

class Platform:
    x: float # bottom
    y: float # left
    width: int = 60
    height: int = 10

    def __init__(self, x, y):
        self.x = x
        self.y = y

    # can make tick method as well for moving platforms etc. (abstractions)

class Game:
    done: bool = False
    width: int # screen width
    height: int # screen height
    elim_y: int = 0 # highest point reached
    seed: int # deterministic seed for world generation
    player: Player
    platforms: list[Platform] = [] # maybe: index for y-level
    platformGen: random.Random
    #monsters

    tickrate: int = 20 # theoretical ticks per second
    preGenHeight: int = 1000 # how much to pre-generate platforms above the screen
    g = -120 # gravity px/s
    moveSpeed = 5
    jumpSpeed = 200

    def __init__(self, width=400, height=600, seed=None):
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

    def genPlatforms(self):
        from_y = self.elim_y
        to_y = self.elim_y + self.preGenHeight
        # Remove platforms below from_y
        self.platforms = [p for p in self.platforms if p.y > from_y]

        # Start from last platform or from_y
        if self.platforms:
            last_y = self.platforms[-1].y
        else:
            last_y = from_y
        
        # Generate platforms until reaching to_y
        while last_y < to_y:
            x = self.platformGen.randint(0, self.width - Platform.width)
            y = last_y + self.platformGen.randint(10, 100)
            self.platforms.append(Platform(x, y))
            last_y = y

    def step(self, action):
        """Advance the game by one tick with given action"""
        if self.done:
            return

        # Apply action
        old_x = self.player.x
        if action == "left":
            self.player.x -= self.moveSpeed
        elif action == "right":
            self.player.x += self.moveSpeed

        self.player.x = self.player.x % self.width # wrap around screen

        # Physics
        self.player.vy += self.g / self.tickrate
        old_y = self.player.y
        self.player.y += self.player.vy / self.tickrate

        self.elim_y = max(self.elim_y, self.player.y - self.height * 0.4)

        # Collision with platform
        filter_platforms = [p for p in self.platforms if 
                            old_y >= p.y + p.height/2 and # at least middle height of platform
                            p.y + p.height >= self.player.y and # jump of top if at top of platform
                            p.x < self.player.x + self.player.width and 
                            self.player.x < p.x + p.width and 
                            self.player.vy <= 0]
        
        if any(filter_platforms):
            self.player.vy = self.jumpSpeed

        # Game over condition
        if self.player.y > self.elim_y + self.height:
            self.done = True

        self.genPlatforms()