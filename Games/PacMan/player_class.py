import pygame as pyg
from settings import *

vec = pyg.math.Vector2


class Player:
    def __init__(self, app, pos):
        self.app = app
        self.starting_pos = vec(pos)
        self.grid_pos = pos  # grid position of PacMan
        self.pix_pos = self.get_pix_pos()
        self.direction = vec(1, 0)  # move  in +ve x-axis by default
        # print(self.grid_pos, self.pix_pos) result [1,1] [55,55]

        # For locking the movement of PacMan in the cells. It can move between
        # them originally.
        self.stored_direction = None

        self.able_to_move = True  # Always able to move by default

        self.current_score = 0

        self.speed = 1

        self.lives = 3

    def get_pix_pos(self):
        return vec(
            (self.grid_pos.x * self.app.cell_width)
            + TOP_BOTTOM_BUFFER // 2
            + self.app.cell_width // 2,
            (self.grid_pos.y * self.app.cell_height)
            + TOP_BOTTOM_BUFFER // 2
            + self.app.cell_height // 2,
        )  # pixel position of PacMan

    def draw(self):
        # Draws Yellow PacMan
        # pyg.draw.circle(surface, color, center, radius). centre should be intergar
        pyg.draw.circle(
            self.app.screen,
            PLAYER_COLOUR,
            (int(self.pix_pos.x), int(self.pix_pos.y)),
            self.app.cell_width // 2 - 2,
        )

        # Drawing Player lives
        for x in range(self.lives):
            pyg.draw.circle(
                self.app.screen, PLAYER_COLOUR, (110 + 20 * x, HEIGHT - 15), 7
            )

        # Rectangle which fits grid cell to keep track of pix_pos of PacMan
        # pyg.draw.rect(surface, color, rect).
        # rect variable in function is position vals, width and height
        # Position vals are aadjusted to fit in grid cells
        # Comment it out.
        # pyg.draw.rect(
        #    self.app.screen,
        #   RED,
        #    (
        #        self.grid_pos[0] * self.app.cell_width + TOP_BOTTOM_BUFFER // 2,
        #        self.grid_pos[1] * self.app.cell_height + TOP_BOTTOM_BUFFER // 2,
        #        self.app.cell_width,
        #        self.app.cell_height,
        #    ),
        #    1,  # makes the rectngle hollow. Only red borders. NO fill.
        # )

    # used in app_class.py in line 183
    def move(self, direction):
        self.stored_direction = direction

    # To lock the movement of PacMan in cells
    def moves_in_cells(self):
        if int(self.pix_pos.x + TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0:
            # print("x is in line")
            # Print as PacMan moves along cells in x-axis
            # self.direction(0,0) so that PacMan starts moving on command on
            # reset (after life lost)
            if (
                self.direction == vec(1, 0)
                or self.direction == vec(-1, 0)
                or self.direction == vec(0, 0)
            ):
                # if PacMan moves left and right
                return True
        if int(self.pix_pos.y + TOP_BOTTOM_BUFFER // 2) % self.app.cell_height == 0:
            if (
                self.direction == vec(0, 1)
                or self.direction == vec(0, -1)
                or self.direction == vec(0, 0)
            ):
                return True

    """
    if moving PacMan (vec) in some grid postion and direction
    equals/hits a wall vec (denoted by <Vector2(0, 29)>) then yield "False."

    For vector of walls refer app_class.py line 67 & visualized in line 98 of draw_grid func in 
    line 76

    This "False" output is assigned to "self.able_to_move" (line 19) in line 118 where PacMan's
    movement is locked in cells. So if PacMan hits wall, can_move becomes False thereby making
    able_to_move False which leads to line 110 becoming False and PacMans direction isn't incremented.
    i.e PacMan stops 
    """

    def can_move(self):
        for wall in self.app.walls:
            if vec(self.grid_pos + self.direction) == wall:
                return False
        return True

    # Delete the coins touched by PacMan
    def on_coin(self):
        # if vector of coin co-incides with PacMan
        if self.grid_pos in self.app.coins:
            # PacMan in cell. Only writing return True led to PacMan eating a bit early.
            if self.moves_in_cells():
                return True
        return False

    def eat_coin(self):
        self.app.coins.remove(self.grid_pos)  # Delete that coin
        self.current_score += 1

    def update(self):
        # self.able_to_move True by default
        if self.able_to_move:
            # PacMan moves & changes direction on command
            self.pix_pos += self.direction * self.speed

        # Locks PacMan in cells.
        if self.moves_in_cells():
            if self.stored_direction != None:
                self.direction = self.stored_direction
            self.able_to_move = self.can_move()

        # Red hollow rectangle follows PacMan.
        # Setting gid position in reference to pixel position
        self.grid_pos[0] = (
            self.pix_pos[0] - TOP_BOTTOM_BUFFER + self.app.cell_width // 2
        ) // self.app.cell_width + 1
        self.grid_pos[1] = (
            self.pix_pos[1] - TOP_BOTTOM_BUFFER + self.app.cell_height // 2
        ) // self.app.cell_height + 1

        # Eat coins
        if self.on_coin():
            self.eat_coin()
