import pygame as pyg
import random
from settings import *

vec = pyg.math.Vector2


class Enemy:
    def __init__(self, app, pos, number):
        # pos is obtained from make_enemies() in app_class.py
        self.app = app
        self.grid_pos = pos
        self.starting_pos = [pos.x, pos.y]
        self.pix_pos = self.get_pix_pos()
        self.radius = self.app.cell_width // 2.3  # radius for enemy circle in draw()

        # Enemy colours
        self.number = number
        self.colour = self.set_colour()

        self.direction = vec(0, 0)  # enemy movement
        self.personality = self.set_personality()

        self.speed = self.set_speed()

        self.target = None

    # pixel positions of enemies
    def get_pix_pos(self):
        return vec(
            (self.grid_pos.x * self.app.cell_width)
            + TOP_BOTTOM_BUFFER // 2
            + self.app.cell_width // 2,
            (self.grid_pos.y * self.app.cell_height)
            + TOP_BOTTOM_BUFFER // 2
            + self.app.cell_height // 2,
        )

    def draw(self):
        pyg.draw.circle(
            self.app.screen,
            self.colour,
            (int(self.pix_pos.x), int(self.pix_pos.y)),
            self.radius,
        )

    def set_colour(self):
        if self.number == 0:
            return (43, 77, 222)
        if self.number == 1:
            return (111, 222, 22)
        if self.number == 2:
            return (111, 22, 22)
        if self.number == 3:
            return (222, 111, 33)

    def set_personality(self):
        if self.number == 0:
            return "speedy"
        elif self.number == 1:
            return "slow"
        elif self.number == 2:
            return "random"
        else:
            return "scared"

    def set_speed(self):
        if self.personality in ["speedy", "scared"]:
            speed = 1.01
        else:
            speed = 1
        return speed

    def set_target(self):
        if self.personality == "speedy" or self.personality == "slow":
            # Vector of PLAYER position in the grid
            return self.app.player.grid_pos
        else:
            if (
                self.app.player.grid_pos[0] > COLUMNS // 2
                and self.app.player.grid_pos[1] > ROWS // 2
            ):
                return vec(1, 1)
            if (
                self.app.player.grid_pos[0] > COLUMNS // 2
                and self.app.player.grid_pos[1] < ROWS // 2
            ):
                return vec(1, ROWS - 2)
            if (
                self.app.player.grid_pos[0] < COLUMNS // 2
                and self.app.player.grid_pos[1] > ROWS // 2
            ):
                return vec(COLUMNS - 2, 1)
            else:
                return vec(COLUMNS - 2, ROWS - 2)

    # Direction for RANDOM enemy
    def get_random_direction(self):
        while True:
            number = random.randint(-2, 2)
            if number == -2:
                x_dir, y_dir = 1, 0
            elif number == -1:
                x_dir, y_dir = 0, 1
            elif number == 0:
                x_dir, y_dir = -1, 0
            else:
                x_dir, y_dir = 0, -1
            next_pos = vec(self.grid_pos.x + x_dir, self.grid_pos.y + y_dir)
            if next_pos not in self.app.walls:
                break
        return vec(x_dir, y_dir)

    # BFS Algorithm
    def BFS(self, start, target):
        # Grid is 28 cols and 30 rows
        grid = [[0 for x in range(28)] for y in range(30)]
        # checking walls
        for cell in self.app.walls:
            if cell.x < 28 and cell.y < 30:
                # whenever looking in 2D array first take y
                grid[int(cell.y)][int(cell.x)] = 1
        queue = [start]
        path = []
        visited = []
        while queue:
            current = queue[0]
            # BFS is first in first out (FIFO). DFS is LILO
            queue.remove(queue[0])
            visited.append(current)
            if current == target:
                break
            else:
                # Down, right, Up, Left
                neighbours = [[0, -1], [1, 0], [0, 1], [-1, 0]]
                for neighbour in neighbours:
                    if neighbour[0] + current[0] >= 0 and neighbour[0] + current[
                        0
                    ] < len(grid[0]):
                        if neighbour[1] + current[1] >= 0 and neighbour[1] + current[
                            1
                        ] < len(grid):
                            next_cell = [
                                neighbour[0] + current[0],
                                neighbour[1] + current[1],
                            ]
                            if next_cell not in visited:
                                if grid[next_cell[1]][next_cell[0]] != 1:
                                    queue.append(next_cell)
                                    # to be able to traverse back to the starting node in order to find
                                    # the shortest path later
                                    path.append({"Current": current, "Next": next_cell})
        shortest = [target]
        # if we haven't made it back to start yet
        while target != start:
            for step in path:
                # moving back up
                if step["Next"] == target:
                    target = step["Current"]
                    shortest.insert(0, step["Current"])
        return shortest

    def find_next_cell(self, target):
        path = self.BFS(
            [int(self.grid_pos.x), int(self.grid_pos.y)],  # enemy starting pos
            [int(target[0]), int(target[1])],  # target is player
        )
        return path[1]

    def get_path_direction(self, target):
        next_cell = self.find_next_cell(target)
        x_direction = next_cell[0] - self.grid_pos[0]
        y_direction = next_cell[1] - self.grid_pos[1]
        return vec(x_direction, y_direction)

    # moves_in_cell() copied from player_class.py
    # self.direction(0,0) to make sure enemy doesn't ignore spawn box
    def moves_in_cells(self):
        if int(self.pix_pos.x + TOP_BOTTOM_BUFFER // 2) % self.app.cell_width == 0:
            if (
                self.direction == vec(1, 0)
                or self.direction == vec(-1, 0)
                or self.direction == vec(0, 0)
            ):
                return True
        if int(self.pix_pos.y + TOP_BOTTOM_BUFFER // 2) % self.app.cell_height == 0:
            if (
                self.direction == vec(0, 1)
                or self.direction == vec(0, -1)
                or self.direction == vec(0, 0)
            ):
                return True
        return False

    def move(self):
        if self.personality == "random":
            self.direction = self.get_random_direction()
        if self.personality == "slow":
            self.direction = self.get_path_direction(self.target)
        if self.personality == "speedy":
            self.direction = self.get_path_direction(self.target)
        if self.personality == "scared":
            self.direction = self.get_path_direction(self.target)

    def update(self):
        self.target = self.set_target()
        if self.target != self.grid_pos:
            self.pix_pos += self.direction * self.speed
            if self.moves_in_cells():
                self.move()

        # Copied from update() from player_class.py
        self.grid_pos[0] = (
            self.pix_pos[0] - TOP_BOTTOM_BUFFER + self.app.cell_width // 2
        ) // self.app.cell_width + 1
        self.grid_pos[1] = (
            self.pix_pos[1] - TOP_BOTTOM_BUFFER + self.app.cell_height // 2
        ) // self.app.cell_height + 1
