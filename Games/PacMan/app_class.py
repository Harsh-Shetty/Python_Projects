import pygame as pyg
import sys
import copy
from settings import *
from player_class import *
from enemy_class import *

pyg.init()
vec = pyg.math.Vector2


class App:
    def __init__(self):
        self.screen = pyg.display.set_mode((WIDTH, HEIGHT))
        self.title = pyg.display.set_caption("PacMan")
        # self.clock = pyg.time.Clock()  # records the times the loop runs for FPS
        self.running = True
        self.state = "start"
        self.cell_width = MAZE_WIDTH // COLUMNS
        self.cell_height = MAZE_HEIGHT // ROWS

        self.walls = []  # list for walls in maze
        self.coins = []  # list for coins
        self.enemies = []  # list of enemies

        self.e_pos = []  # Position of enemies
        self.p_pos = None
        # Walls list is appended in load func. So it must be declared
        # before self.load()
        self.load()  # for loading image (Maze)

        self.player = Player(self, vec(self.p_pos))  # Initialise PacMan

        self.make_enemies()

    def run(self):
        while self.running:
            if self.state == "start":
                self.start_events()
                self.start_draw()
            elif self.state == "playing":
                self.playing_events()
                self.playing_update()
                self.playing_draw()
            elif self.state == "Game Over":
                self.over_events()
                self.over_update()
                self.over_draw()
            # else:
            #    self.clock.tick(FPS)
        pyg.quit()
        sys.exit()

    ############################ HELPER FUNCTIONS ##################################################################################

    def draw_text(self, words, screen, pos, size, colour, font_name, centered=False):
        # By default its set to False.
        # pos is position in tuple format
        font = pyg.font.SysFont(font_name, size)
        # font.render(text, antialias, color). altialias set as False
        text = font.render(words, False, colour)
        text_size = text.get_size()  # gets tuple of width and height of text
        # Reference for centering (SCREEN_WIDTH-surf.get_width())/2 https://realpython.com/lessons/using-blit-and-flip/
        if centered:
            # if centered True
            pos[0] = pos[0] - text_size[0] // 2
            pos[1] = pos[1] - text_size[1] // 2
        screen.blit(
            text, pos
        )  # created Surface (here text (string)) to display on the screen.
        # Pos stores position to display the source surface

    def load(self):
        # Loading image of maze
        self.background = pyg.image.load("maze.png")
        self.background = pyg.transform.scale(
            self.background, (MAZE_WIDTH, MAZE_HEIGHT)
        )

        # Opening "walls" file & creating walls, coins &  enemies
        # list with coords of walls, coins & enemies
        with open("walls.txt", "r") as file:
            for y_index, line in enumerate(file):
                for x_index, char in enumerate(line):
                    if char == "1":
                        self.walls.append(vec(x_index, y_index))
                    elif char == "C":
                        self.coins.append(vec(x_index, y_index))
                    # Player Position
                    elif char == "P":
                        self.p_pos = [x_index, y_index]
                    elif char in ["2", "3", "4", "5"]:
                        # print(y_index, x_index)
                        # Result 15 12
                        #        15 13
                        #        15 14
                        #        15 15
                        # cr8ing Vec pos of enemies from wall.txt
                        self.e_pos.append([x_index, y_index])
                    # Black rect for opening for enemies to come out.
                    # Maze is an img. The img will keep on existing even if char "1"
                    # is removed from "Wall.txt". So we make a black rect on that
                    # portion of the image.
                    elif char == "B":
                        pyg.draw.rect(
                            self.background,
                            BLACK,
                            (
                                x_index * self.cell_width,
                                y_index * self.cell_height,
                                self.cell_width,
                                self.cell_height,
                            ),
                        )

        # print(self.walls) result [<Vector2(0, 0)>, <Vector2(1, 0)>,....,<Vector2(27, 29)>]

    # For visualization purposes only. Comment it off in playing_draw (last func)

    def draw_coins(self):
        for coin in self.coins:
            pyg.draw.circle(
                self.screen,
                (122, 122, 9),
                (
                    int(coin.x * self.cell_width)
                    + self.cell_width // 2
                    + TOP_BOTTOM_BUFFER // 2,
                    int(coin.y * self.cell_height)
                    + self.cell_width // 2
                    + TOP_BOTTOM_BUFFER // 2,
                ),
                5,
            )

    # Using Vec pos obtained from load() to populate pos
    # in Enemy class> def __init__ in enemy_class.py
    def make_enemies(self):
        for idx, pos in enumerate(self.e_pos):
            self.enemies.append(Enemy(self, vec(pos), idx))

    def draw_grid(self):
        # Draws grey cells
        # Vertical lines
        for x in range(WIDTH // self.cell_width):
            pyg.draw.line(
                self.background,
                GREY,
                (x * self.cell_width, 0),  # start position (X,Y))
                (x * self.cell_width, HEIGHT),  # end position (X,Y)
            )
        # Horizontal lines
        for x in range(HEIGHT // self.cell_height):
            pyg.draw.line(
                self.background,
                GREY,
                (0, x * self.cell_height),
                (WIDTH, x * self.cell_height),
            )
        # Maze image is just an image. It's only a background.
        for coin in self.coins:
            pyg.draw.rect(
                self.background,  # Surface
                (167, 177, 33),  # Colour
                (  # Rectangular dimensions
                    coin.x * self.cell_width,  # x position
                    coin.y * self.cell_height,  # y position
                    self.cell_width,  # width
                    self.cell_height,  # height
                ),
            )

    # game reset
    def set(self):
        # Set PacMan's pos to starting pos (p_pos) after life lost &
        # get it moving
        self.player.grid_pos = vec(self.player.starting_pos)

        # Player is pushed into wall when enemy hits it.
        # So reset pix_pos by calling it & mutiply direction by 0 & set it.
        self.player.pix_pos = self.player.get_pix_pos()  # get_pix_pos gets
        # pixel positon based on grid position
        self.player.direction *= 0

        # Reset ENEMIES
        for enemy in self.enemies:
            enemy.grid_pos = vec(enemy.starting_pos)
            enemy.pix_pos = enemy.get_pix_pos()
            enemy.direction *= 0

    def reset(self):
        self.player.lives = 3
        self.player.current_score = 0
        # For some reason there were 2 lives after reset when
        # self.player.lives = 3. So self.set() was added to remove the error
        self.set()
        self.coins = []
        with open("walls.txt", "r") as file:
            for y_index, line in enumerate(file):
                for x_index, char in enumerate(line):
                    if char == "C":
                        self.coins.append(vec(x_index, y_index))
        self.state = "playing"

    ################ START FUNCTIONS ############################################################

    def start_events(self):
        # pyg.event.get keeps records of events since
        # the last time it was called
        for event in pyg.event.get():
            # pyg.QUIT is an event when X window button is pressed
            if event.type == pyg.QUIT:
                self.running = False
            # Start game on pressing Spacebar
            if event.type == pyg.KEYDOWN and event.key == pyg.K_SPACE:
                self.state = "playing"

    # Start Screen
    def start_draw(self):
        self.screen.fill(BLACK)  # Screen background
        self.draw_text(
            "PRESS SAPCE",
            self.screen,
            [WIDTH // 2, HEIGHT // 2 - 50],
            START_TEXT_SIZE,
            (170, 132, 58),
            START_FONT,
            centered=True,
        )
        self.draw_text(
            "1 PLAYER ONLY",
            self.screen,
            [WIDTH // 2, HEIGHT // 2 + 50],
            START_TEXT_SIZE,
            (44, 167, 198),
            START_FONT,
            centered=True,
        )

        pyg.display.update()

    ################ PLAYING FUNCTIONS ############################################################

    def playing_events(self):
        for event in pyg.event.get():
            # pyg.QUIT is an event when X window button is pressed
            if event.type == pyg.QUIT:
                self.running = False
            if event.type == pyg.KEYDOWN:
                if event.key == pyg.K_LEFT:
                    self.player.move(vec(-1, 0))
                if event.key == pyg.K_RIGHT:
                    self.player.move(vec(1, 0))
                if event.key == pyg.K_UP:
                    self.player.move(vec(0, -1))
                if event.key == pyg.K_DOWN:
                    self.player.move(vec(0, 1))

    # Playing Screen
    def playing_draw(self):
        self.screen.fill(BLACK)
        self.screen.blit(
            self.background, (TOP_BOTTOM_BUFFER // 2, TOP_BOTTOM_BUFFER // 2)
        )  # Screen maze background. //2 to centre properly
        self.draw_coins()  # after blit so that coins are drawn on top
        # of screen insted on the screen
        # self.draw_grid() Visualization turned off. Refer line 142
        self.draw_text(
            f"CURRENT SCORE: {self.player.current_score}",
            self.screen,
            (60, 0),
            18,
            WHITE,
            START_FONT,
            centered=False,
        )

        self.draw_text(
            "LIVES:",
            self.screen,
            (40, HEIGHT - 26),
            14,
            WHITE,
            START_FONT,
            centered=False,
        )
        self.player.draw()
        for enemy in self.enemies:
            enemy.draw()
        pyg.display.update()

    def remove_life(self):
        self.player.lives -= 1
        if self.player.lives == 0:
            self.state = "Game Over"
        else:
            self.set()  # Helper function

    def playing_update(self):
        self.player.update()
        for enemy in self.enemies:
            enemy.update()

        # when enemy hits player
        for enemy in self.enemies:
            if enemy.grid_pos == self.player.grid_pos:
                # print("hit")
                self.remove_life()

    ##################### GAME OVER FUNCTIONS #################################################################

    def over_events(self):
        for event in pyg.event.get():
            if event.type == pyg.QUIT:
                self.running = False
            if event.type == pyg.KEYDOWN and event.key == pyg.K_SPACE:
                self.reset()
            if event.type == pyg.KEYDOWN and event.key == pyg.K_ESCAPE:
                self.running = False

    def over_draw(self):
        self.screen.fill(BLACK)
        quit_text = "Press ESCAPE button to Quit"
        play_again_text = "Press SPACE to play again!!"

        # Game over text
        self.draw_text(
            "GAME OVER",
            self.screen,
            [WIDTH // 2, 100],
            36,
            RED,
            "arial",
            centered=True,
        )

        self.draw_text(
            play_again_text,
            self.screen,
            [WIDTH // 2, HEIGHT // 2],  #  centre of the screen
            36,
            WHITE,
            "arial",
            centered=True,
        )
        self.draw_text(
            quit_text,
            self.screen,
            [WIDTH // 2, HEIGHT // 1.5],
            36,
            (128, 128, 128),
            "arial",
            centered=True,
        )
        pyg.display.update()

    def over_update(self):
        pass
