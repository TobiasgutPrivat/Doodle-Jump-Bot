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
    width: int # screen width
    height: int # screen height
    max_y: int = 0 # highest point reached
    seed: int # deterministic seed for world generation
    player: Player
    platforms: list[Platform] = [] # maybe: index for y-level
    platformGen: random.Random
    #monsters

    tickrate: int # theoretical ticks per second
    preGenHeight: int = 1000 # how much to pre-generate platforms above the screen

    def __init__(self, width=400, height=600, seed=None):
        if seed is None:
            seed = random.randint(0, 2**32 - 1)
        self.width = width
        self.height = height
        middle_x = width // 2
        self.player = Player(middle_x+Player.width/2, height/5)
        self.platforms = [Platform(x=middle_x+Platform.width/2, y=height/5)] # starting platform
        self.platformGen = random.Random(seed)
        self.genPlatforms(0, self.preGenHeight)

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

        self.player.x = self.player.x % self.width # wrap around screen

        # Physics
        self.player.vy += -9.81 / self.tickrate
        old_y = self.player.y
        self.player.y += old_y / self.tickrate

        self.max_y = max(self.max_y, self.player.y)

        # Collision with platform
        filter_platforms = [p for p in self.platforms if 
                            old_y + 20 <= p.y <= self.player.y + 20 and 
                            p.x <= self.player.x + 20 <= p.x + 60 and self.player.vy <= 0]
        if any(filter_platforms):
            self.player.vy = 100

        # Game over condition
        if self.player.y > self.max_y + self.height:
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
