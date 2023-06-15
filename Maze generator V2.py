import pygame
from random import choice


RES = WIDTH, HEIGHT = 1202, 902
RES_WINDOW = T_WIDTH, T_HEIGHT = 1800, HEIGHT
TILE = 50
cols, rows = WIDTH // TILE, HEIGHT // TILE


pygame.init()
sc = pygame.display.set_mode(RES_WINDOW)
pygame.display.set_caption("Maze generator")
clock = pygame.time.Clock()


class Cell:
    def __init__(self, x, y):
        self.x, self.y = x, y
        self.walls = {"top": True, "bottom": True, "right": True, "left": True}
        self.visited = False
        self.end = False
        self.start = False
        self.path = False

    def draw(self):
        x, y = self.x * TILE, self.y * TILE
        if self.visited:
            pygame.draw.rect(sc, pygame.Color("black"), (x, y, TILE, TILE))
        if self.path:
            pygame.draw.rect(sc, pygame.Color("blue"), (x, y, TILE, TILE))
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
        pygame.draw.rect(sc, pygame.Color("purple"), (x, y, TILE, TILE))

    def check_cell(self, x, y):
        global grid_cells
        find_index = lambda x, y: x + y * cols
        if x < 0 or x > cols - 1 or y < 0 or y > rows - 1:
            return False
        return grid_cells[find_index(x, y)]

    def check_neighbours(self):
        neighbours = []
        top = self.check_cell(self.x, self.y - 1)
        right = self.check_cell(self.x + 1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
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

    def check_walls(self):
        neighbours = []
        top = self.check_cell(self.x, self.y - 1)
        right = self.check_cell(self.x + 1, self.y)
        bottom = self.check_cell(self.x, self.y + 1)
        left = self.check_cell(self.x - 1, self.y)
        if top and not top.walls["bottom"] and not top.visited:
            neighbours.append(top)
        if right and not right.walls["left"] and not right.visited:
            neighbours.append(right)
        if bottom and not bottom.walls["top"] and not bottom.visited:
            neighbours.append(bottom)
        if left and not left.walls["right"] and not left.visited:
            neighbours.append(left)
        if neighbours:
            return choice(neighbours)
        else:
            return False


class Button:
    def __init__(self, x, y, width, height, text):
        self.x, self.y = x, y
        self.width, self.height = width, height
        self.pressed = False
        self.hover = False
        self.invisible = False
        self.text = text
        self.color = {"normal": (255, 165, 0), "hover": (139, 64, 0), "pressed": (0, 255, 0)}

    def draw(self):
        if not self.invisible:
            colors = self.color
            text = self.text
            x, y = self.x, self.y
            width, height = self.width, self.height
            self.check_mouse()
            if self.hover:
                color = colors["hover"]
            elif self.pressed:
                color = colors["pressed"]
            else:
                color = colors["normal"]
            pygame.draw.rect(sc, pygame.Color(color), (x, y, width, height))
            font = pygame.font.Font('freesansbold.ttf', 32)
            text1 = font.render(text, True, (0, 0, 0), None)
            center_x = x + width // 2 - (text1.get_width() // 2)
            center_y = y + height // 2 - (text1.get_height() // 2)
            sc.blit(text1, (center_x, center_y))

    def check_mouse(self):
        x, y = self.x, self.y
        width, height = self.width, self.height
        mouse = pygame.mouse.get_pos()
        mouse_click = pygame.mouse.get_pressed(3)
        if x <= mouse[0] <= x + width and y <= mouse[1] <= y + height:
            if mouse_click[0]:
                self.pressed = True
            else:
                self.hover = True
                self.pressed = False
        else:
            self.hover = False


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
stack = []


def create_cells_stack():
    global grid_cells
    for row in range(rows):
        for col in range(cols):
            grid_cells.append(Cell(col, row))


def choose_start_end(grid_cells):
    start, end = choice(grid_cells), choice(grid_cells)
    wall_count_s = 0
    while wall_count_s < 3:
        wall_count_s = 0
        start = choice(grid_cells)
        for wall_s in start.walls:
            if start.walls[wall_s]:
                wall_count_s += 1
    wall_count_e = 0
    while wall_count_e < 3 or end == start:
        wall_count_e = 0
        end = choice(grid_cells)
        for wall_e in end.walls:
            if end.walls[wall_e]:
                wall_count_e += 1
    end.end = True
    start.start = True


def solving():
    global grid_cells
    interface()
    choose_start_end(grid_cells)
    stack = []
    current_cell = grid_cells[0]
    for cell in grid_cells:
        cell.visited = False
        if cell.start:
            current_cell = cell
    while True:
        pygame.draw.rect(sc, pygame.Color("darkslategray"), (0, 0, WIDTH, HEIGHT))
        next_cell = current_cell.check_walls()
        for way in grid_cells:
            if way in stack:
                way.path = True
            else:
                way.path = False
        for cell in grid_cells:
            cell.draw()
        current_cell.visited = True
        current_cell.draw_current_cell()
        if current_cell.end:
            break
        if next_cell:
            next_cell.visited = True
            stack.append(current_cell)
            current_cell = next_cell
        else:
            if len(stack) != 0:
                current_cell = stack[-1]
                stack.pop()
        pygame.display.flip()
        clock.tick(100)
    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        for cell in grid_cells:
            cell.draw()


def maze_generate():
    global grid_cells, stack
    current_cell = grid_cells[0]
    while True:
        pygame.draw.rect(sc, pygame.Color("darkslategray"), (0, 0, WIDTH, HEIGHT))
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
            stack.pop()
            if len(stack) != 0:
                current_cell = stack[-1]
            else:
                break
        pygame.display.flip()
        clock.tick(50)


def interface():
    global RES, RES_WINDOW
    global grid_cells, RES, RES_WINDOW
    create_cells_stack()
    buttons = []
    while True:
        pygame.draw.rect(sc, pygame.Color("darkslategray"), (0, 0, WIDTH, HEIGHT))
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                exit()
        for cell in grid_cells:
            cell.draw()
        pygame.draw.rect(sc, pygame.Color("beige"), (WIDTH, 0, T_WIDTH-WIDTH, HEIGHT))
        font = pygame.font.Font('freesansbold.ttf', 64)
        text = font.render("INTERFACE", True, (0, 0, 0), None)
        center_x = WIDTH + (T_WIDTH - WIDTH) // 2 - (text.get_width() // 2)
        sc.blit(text, (center_x, 20))
        generate = Button(WIDTH + 150, 200, 300, 50, "GENERATE")
        load = Button(WIDTH + 150, 400, 300, 50, "LOAD")
        quit = Button(WIDTH + 150, 600, 300, 50, "QUIT")
        buttons.extend([generate, load, quit])
        for button in buttons:
            button.draw()
        if generate.pressed:
            for button in buttons:
                button.invisible = True
            maze_generate()
        if quit.pressed:
            exit()
        pygame.display.flip()
        clock.tick(50)


def main():
    interface()
    solving()


if __name__ == '__main__':
    main()
