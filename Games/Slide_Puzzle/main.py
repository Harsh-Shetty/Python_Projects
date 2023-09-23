import pygame, sys, os, random


class SlidePuzzle:

    speed = 500  # speed for slide animation
    prev = None  # for making puzzle randomiztion better
    # gs=Grid Size, ts=Tile Silze, ms=Margin Size
    def __init__(self, gs, ts, ms):
        self.gs, self.ts, self.ms = gs, ts, ms

        self.tiles_len = gs[0] * gs[1] - 1
        self.tiles = [(x, y) for y in range(gs[1]) for x in range(gs[0])]

        self.tilepos = [
            (x * (ts + ms) + ms, y * (ts + ms) + ms)
            for y in range(gs[1])
            for x in range(gs[0])
        ]  # actual positon on screen
        self.tilePOS = {
            (x, y): (x * (ts + ms) + ms, y * (ts + ms) + ms)
            for y in range(gs[1])
            for x in range(gs[0])
        }  # The place they slide to

        w, h = (
            gs[0] * (ts + ms) + ms,
            gs[1] * (ts + ms) + ms,
        )  # width & height of board

        pic = pygame.image.load("image.jpg")  # Loading image for puzzle
        pic = pygame.transform.smoothscale(pic, (w, h))  # Fitting image

        self.font = pygame.font.Font(None, 120)

        self.images = []

        # Numbers in the tiles
        for i in range(self.tiles_len):
            x, y = self.tilepos[i]  # x & y coordinate of tiles
            image = pic.subsurface(
                x, y, ts, ts
            )  # fitting image in each tile (x,y,ts(width), ts(height))
            text = self.font.render(str(i + 1), 2, (0, 0, 0))
            w, h = text.get_size()  # for centering the numbers
            image.blit(text, ((ts - w) / 2, (ts - h) / 2))
            self.images += [image]

    # Blank Tile
    def getBlank(self):
        return self.tiles[-1]

    def setBlank(self, pos):
        self.tiles[-1] = pos

    opentile = property(getBlank, setBlank)

    def sliding(self):
        for i in range(self.tiles_len):
            x, y = self.tilepos[i]  # current position
            X, Y = self.tilePOS[self.tiles[i]]  # target position
            if x != X or y != Y:
                return True

    def switch(self, tile):

        if self.sliding():
            return

        self.tiles[self.tiles.index(tile)], self.opentile, self.prev = (
            self.opentile,
            tile,
            self.opentile,
        )

    # FOR MOUSE COLLISIONS
    # check mouse pointer in grid
    def in_grid(self, tile):
        return (
            tile[0] >= 0
            and tile[0] < self.gs[0]
            and tile[1] >= 0
            and tile[1] < self.gs[1]
        )

    # diagonal tiles must not be switched
    def adjacent(self):
        x, y = self.opentile
        return (x - 1, y), (x + 1, y), (x, y - 1), (x, y + 1)

    # randomize puzzle on key press Space. diagonal tiles randomised
    def random(self):
        adj = self.adjacent()
        self.switch(
            random.choice(
                [pos for pos in adj if self.in_grid(pos) and pos != self.prev]
            )
        )

    def update(self, dt):
        mouse = pygame.mouse.get_pressed()
        mpos = pygame.mouse.get_pos()  # getting mouse position

        if mouse[0]:
            # no output for mouse in margin(between tiles)
            x, y = mpos[0] % (self.ts + self.ms), mpos[1] % (self.ts + self.ms)
            if x > self.ms and y > self.ms:
                tile = mpos[0] // self.ts, mpos[1] // self.ts
                if self.in_grid(tile):
                    # if mouse in tile switch places with blank tile
                    # No switch for mouse in adjacent tile
                    if tile in self.adjacent():
                        self.switch(tile)

        # For slide animation
        s = self.speed * dt
        for i in range(self.tiles_len):
            x, y = self.tilepos[i]  # current position
            X, Y = self.tilePOS[self.tiles[i]]  # target position
            dx, dy = X - x, Y - y
            x = x + s if dx > 0 else x - s if dx < 0 else X
            y = y + s if dy > 0 else y - s if dy < 0 else Y
            self.tilepos[i] = x, y

    def draw(self, screen):
        for i in range(self.tiles_len):
            x, y = self.tilepos[i]
            pygame.draw.rect(screen, (0, 255, 0), (x, y, self.ts, self.ts))
            screen.blit(self.images[i], (x, y))

    # Event for KEYBOARD COLLISION
    def events(self, event):
        # move tiles
        if event.type == pygame.KEYDOWN:
            for key, dx, dy in (
                (pygame.K_w, 0, -1),
                (pygame.K_s, 0, 1),
                (pygame.K_a, -1, 0),
                (pygame.K_d, 1, 0),
            ):
                if event.key == key:
                    x, y = self.opentile
                    tile = x + dx, y + dy
                    if self.in_grid(tile):
                        self.switch(tile)
            # for randomising
            if event.key == pygame.K_SPACE:
                for i in range(100):
                    self.random()


def main():
    pygame.init()
    os.environ["SDL_VIDEO_CENTERED"] = "1"
    pygame.display.set_caption("Slide Puzzle")
    screen = pygame.display.set_mode((500, 500))
    fpsclock = pygame.time.Clock()
    program = SlidePuzzle((3, 3), 160, 5)  # (gs=x,y), ts, ms

    gameLoop = True

    while gameLoop:
        dt = fpsclock.tick() / 1000
        screen.fill((0, 0, 0))
        program.draw(screen)
        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                gameLoop = False
            program.events(event)  # Event for KEYBOARD COLLISION

        program.update(dt)


if __name__ == "__main__":
    main()
