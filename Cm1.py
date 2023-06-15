import pygame
from random import choice
from datetime import datetime

# Cm2560 × 1600
RES = WIDTH, HEIGHT = int(1202*0.8), int(923*0.8)
RES_WINDOW = T_WIDTH, T_HEIGHT = 1800, HEIGHT
TILE = 70
cols, rows = WIDTH // TILE, HEIGHT // TILE


pygame.init()
sc = pygame.display.set_mode(RES_WINDOW)
pygame.display.set_caption("Maze generator")
clock = pygame.time.Clock()


class Cell:
    def __init__(self, x, y, walls=None, visited_from_txt=False, end_from_txt=False, start_from_txt=False, path_from_txt=False):
        self.x, self.y = x, y
        if walls == None:
            self.walls = {"top": True, "bottom": True,
                          "right": True, "left": True}
        else:
            self.walls = walls
        self.visited = visited_from_txt
        self.end = end_from_txt
        self.start = start_from_txt
        self.path = path_from_txt

    def draw(self):
        x, y = self.x * TILE, self.y * TILE
        if self.visited:
            pygame.draw.rect(sc, pygame.Color("black"), (x, y, TILE, TILE))
        if self.path:
            pygame.draw.rect(sc, pygame.Color("blue"), (x, y, TILE, TILE))
        if self.end:
            pygame.draw.rect(sc, pygame.Color("red"),
                             (x+2, y+2, TILE-2, TILE-2))
        if self.start:
            pygame.draw.rect(sc, pygame.Color("green"),
                             (x+2, y+2, TILE-2, TILE-2))
        if self.walls["top"]:
            pygame.draw.line(sc, pygame.Color("darkorange"),
                             (x, y), (x + TILE, y), 2)
        if self.walls["bottom"]:
            pygame.draw.line(sc, pygame.Color("darkorange"),
                             (x, y+TILE), (x + TILE, y + TILE), 2)
        if self.walls["right"]:
            pygame.draw.line(sc, pygame.Color("darkorange"),
                             (x + TILE, y), (x + TILE, y+TILE), 2)
        if self.walls["left"]:
            pygame.draw.line(sc, pygame.Color(
                "darkorange"), (x, y), (x, y+TILE), 2)

    def draw_current_cell(self):
        x, y = self.x * TILE, self.y * TILE
        pygame.draw.rect(sc, pygame.Color("purple"), (x, y, TILE, TILE))

    def check_cell(self, x, y):
        global grid_cells
        def find_index(x, y): return x + y * cols
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
        self.text = text
        self.color = {"normal": (255, 165, 0), "hover": (
            139, 64, 0), "pressed": (0, 255, 0)}

    def draw(self):
        colors = self.color
        text = self.text
        x, y = self.x, self.y
        size = 32
        width, height = self.width, self.height
        if self.hover:
            color = colors["hover"]
        elif self.pressed:
            color = colors["pressed"]
        else:
            color = colors["normal"]
        pygame.draw.rect(sc, pygame.Color(color), (x, y, width, height))
        font = pygame.font.Font('freesansbold.ttf', size)
        text = font.render(text, True, (0, 0, 0), None)
        sc.blit(text, (x+width//2-size, y+height//2-(size//2)))


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
    #global grid_cells
    mazes = loading_maze()
    grid_cells = mazes['giovanni21']
    # interface()
    choose_start_end(grid_cells)
    stack = []
    current_cell = grid_cells[0]
    for cell in grid_cells:
        cell.visited = False
        if cell.start:
            current_cell = cell
    while True:
        pygame.draw.rect(sc, pygame.Color(
            "darkslategray"), (0, 0, WIDTH, HEIGHT))
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


def transform(a):
    if a == "t":
        return True
    if a == "f":
        return False
    if str(a) == 'True':
        return "t"
    if str(a) == 'False':
        return "f"
    else:
        return a


def saving_to_txt():
    collection = open("collection_of_mazes", "a")
    name = input("Name the maze: ")
    collection.write(f"{name}|")
    for cells in grid_cells:
        collection.write(
            f"{cells.x},{cells.y},{transform(cells.walls['top'])},{transform(cells.walls['bottom'])},{transform(cells.walls['right'])},{transform(cells.walls['left'])},{transform(cells.visited)},{transform(cells.start)},{transform(cells.end)},{transform(cells.path)}.")
    collection.write("\n")
    collection.close()


def loading_maze():
    dict_of_mazes = {}
    tiny_dicktionnary = {}
    collection = open("collection_of_mazes", "r")
    Lines = collection.readlines()
    # Lines.remove('\n')
    for i in range(len(Lines)):
        current_cells = []
        name_cells_list = str(Lines[i]).split("|")
        cell_list = str(name_cells_list[1]).split(".")
        cell_list.remove('\n')
        name = str(name_cells_list[0])

        for number_of_cell in range(len(cell_list)):
            cell_elements = cell_list[number_of_cell].split(",")
            for i in range(len(cell_elements)-1):
                cell_elements[i] = transform(str(cell_elements[i]))
                tiny_dicktionnary['top'], tiny_dicktionnary['bottom'], tiny_dicktionnary['right'], tiny_dicktionnary[
                    'left'] = cell_elements[2], cell_elements[3], cell_elements[4], cell_elements[5]
            current_cells.append(Cell(
                int(cell_elements[0]), int(cell_elements[1]), tiny_dicktionnary, cell_elements[6], cell_elements[7], cell_elements[8], cell_elements[9]))
        dict_of_mazes[name] = current_cells
    return dict_of_mazes


def maze_generate():
    global grid_cells, RES, RES_WINDOW
    create_cells_stack()
    current_cell = grid_cells[0]
    while True:
        interface()
        pygame.draw.rect(sc, pygame.Color(
            "darkslategray"), (0, 0, WIDTH, HEIGHT))
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
        clock.tick(100)


def interface():
    global RES, RES_WINDOW
    pygame.draw.rect(sc, pygame.Color("beige"),
                     (WIDTH, 0, T_WIDTH-WIDTH, HEIGHT))
    font = pygame.font.Font('freesansbold.ttf', 64)
    text = font.render("INTERFACE", True, (0, 0, 0), None)
    sc.blit(text, (WIDTH + 125, 20))
    test = Button(1370, 200, 300, 50, "Test")
    test.draw()


def main():
    # maze_generate()
    # saving_to_txt()
    # print(len(grid_cells))

    solving()


if __name__ == '__main__':
    main()
