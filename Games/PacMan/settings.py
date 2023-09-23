from pygame.math import Vector2 as vec

# screen dimensions
WIDTH, HEIGHT = 610, 670
MAZE_WIDTH, MAZE_HEIGHT = 560, 620  # minus 50 pixels (buffer) from above values

# Maze divided into grids
ROWS = 30
COLUMNS = 28

TOP_BOTTOM_BUFFER = 50  # 50 in pixels. Gap between the window and the maze image

# Colours
BLACK = (0, 0, 0)
RED = (208, 22, 22)
GREY = (107, 107, 107)
WHITE = (255, 255, 255)
PLAYER_COLOUR = (190, 190, 15)

# Font Settings
START_TEXT_SIZE = 16
START_FONT = "arial black"

# PLayer settings
# PLAYER_START_POS = vec(0.98, 1)  # PacMan starting grid position
