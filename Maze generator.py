import pygame
from random import choice, randint


RES = WIDTH, HEIGHT = 1202, 902
TILE = 100
cols, rows = WIDTH // TILE, HEIGHT // TILE


pygame.init()
sc = pygame.display.set_mode(RES)
clock = pygame.time.Clock()


class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {"top": True, "bottom": True, "right": True, "left": True}
        self.visited = False
        self.end = False
        self.start = False

    def draw(self):
        x, y = self.x * TILE, self.y * TILE
        if self.visited:
            pygame.draw.rect(sc, pygame.Color("black"), (x, y, TILE, TILE))
        if self.end:
            pygame.draw.rect(sc, pygame.Color("red"), (x+2, y+2, TILE-2, TILE-2))
        if self.start:
            pygame.draw.rect(sc, pygame.Color("green"), (x+2, y+2, TILE-2, TILE-2))
        if self.walls["top"]:
            pygame.draw.line(sc, pygame.Color("darkorange"), (x, y), (x + TILE, y), 2)
        if self.walls["bottom"]:
            pygame.draw.line(sc, pygame.Color("darkorange"), (x, y+TILE), (x + TILE, y + TILE), 2)
        if self.walls["right"]:
            pygame.draw.line(sc, pygame.Color("darkorange"), (x + TILE, y), (x + TILE, y+TILE), 2)
        if self.walls["left"]:
            pygame.draw.line(sc, pygame.Color("darkorange"), (x, y), (x, y+TILE), 2)

    def draw_current_cell(self):
        x, y = self.x * TILE, self.y * TILE
        pygame.draw.rect(sc, pygame.Color("orange"), (x, y, TILE, TILE))

    def check_cell(self, x, y):
        find_index = lambda x, y: x + y * cols
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return grid_cells[find_index(x, y)]

    def check_neighbours(self):
        neighbours = []
        top = self.check_cell(self.x, self.y + 1)
        right = self.check_cell(self.x + 1, self.y)
        bottom = self.check_cell(self.x, self.y - 1)
        left = self.check_cell(self.x - 1, self.y)
        if top and not top.visited:
            neighbours.append(top)
        if right and not right.visited:
            neighbours.append(right)
        if bottom and not bottom.visited:
            neighbours.append(bottom)
        if left and not left.visited:
            neighbours.append(left)
        if neighbours:
            return choice(neighbours)
        else:
            return False


def remove_walls(current, next):
    dx = current.x - next.x
    if dx == 1:
        current.walls["left"] = False
        next.walls["right"] = False
    elif dx == -1:
        current.walls["right"] = False
        next.walls["left"] = False
    dy = current.y - next.y
    if dy == 1:
        current.walls["top"] = False
        next.walls["bottom"] = False
    elif dy == -1:
        current.walls["bottom"] = False
        next.walls["top"] = False


grid_cells = []
for row in range(rows):
    for col in range(cols):
        grid_cells.append(Cell(col, row))
current_cell = grid_cells[0]
stack = []


def choose_start_end(grid_cells):
    start, end = choice(grid_cells), choice(grid_cells)
    while ((end.x - start.x)**2 + (end.y - start.y)**2)**1/2 <= 10:
        start, end = choice(grid_cells), choice(grid_cells)
    end.end = True
    start.start = True
    return start, end


start, end = choose_start_end(grid_cells)


while True:
    sc.fill(pygame.Color("darkslategray"))

    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            exit()
    for cell in grid_cells:
        cell.draw()
    current_cell.visited = True
    current_cell.draw_current_cell()

    next_cell = current_cell.check_neighbours()
    if next_cell:
        next_cell.visited = True
        stack.append(current_cell)
        remove_walls(current_cell, next_cell)
        current_cell = next_cell
    else:
        if len(stack) != 1:
            stack.pop()
            current_cell = stack[-1]

    pygame.display.flip()
    clock.tick(30)
