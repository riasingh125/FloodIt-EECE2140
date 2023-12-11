import pygame
import random

# Constants
CELL_SIZE = 35
BOARD_SIZE = 15
COLORS_AVAILABLE = 8

# Define colors
COLOR_LIST = [
    pygame.Color("RED"),
    pygame.Color("BLUE"),
    pygame.Color("GREEN"),
    pygame.Color("YELLOW"),
    pygame.Color("PURPLE"),
    pygame.Color("ORANGE"),
    pygame.Color("PINK"),
    pygame.Color("GRAY")
]

# Represents a single square of the game area
class Cell:
    def __init__(self, x, y, flooded, colors_avail):
        self.x = x
        self.y = y
        self.flooded = flooded
        self.colors_avail = colors_avail
        self.color = self.set_colors()
        self.top = None
        self.bottom = None
        self.left = None
        self.right = None

    def set_colors(self):
        if self.flooded:
            return random.choice(COLOR_LIST.copy()[:self.colors_avail])
        else:
            return pygame.Color("WHITE")

    def cell_rect(self):
        return pygame.Rect(self.x * CELL_SIZE, self.y * CELL_SIZE, CELL_SIZE, CELL_SIZE)

    def draw(self, screen):
        pygame.draw.rect(screen, self.color, self.cell_rect())

# Represents the game world
class FloodItGame:
    def __init__(self, board_size, colors_avail):
        self.board_size = board_size
        if board_size > 15:
            raise ValueError("Board size must be less than or equal to 15")
        self.colors_avail = colors_avail
        if colors_avail > 8 or colors_avail < 2:
            raise ValueError("Colors available must be between 2 and 8")
        self.board = self.make_cell(board_size)
        self.completely_flooded = False
        self.num_of_clicks = 0
        self.turns_given = (board_size * 2) + int(3.25 * colors_avail)
        self.timer = 0
        self.colorList = [self.board[0][0]]

    def make_cell(self, board_size):
        return [
            [Cell(i, j, True, self.colors_avail) for j in range(board_size)] for i in range(board_size)
        ]

    def update_cells(self, cell, next_cell):
        x, y = cell.x, cell.y

        if (0 <= x-1 < self.board_size) and self.board[x-1][y].color == next_cell.color:
                self.colorList.append(self.board[x-1][y])
        if (0 <= x+1 < self.board_size) and self.board[x+1][y].color == next_cell.color:
                self.colorList.append(self.board[x+1][y])
        if (0 <= y-1 < self.board_size) and self.board[x][y-1].color == next_cell.color:
                self.colorList.append(self.board[x][y-1])
        if (0 <= y+1 < self.board_size) and self.board[x][y+1].color == next_cell.color:
                self.colorList.append(self.board[x][y+1])

    def on_mouse_click(self, pos):
        mouse_x, mouse_y = pos
        j = mouse_x // CELL_SIZE
        i = mouse_y // CELL_SIZE
        self.colorList.append(self.board[j][i]) if self.board[j][i] not in self.colorList or (0 <= i < self.board_size and 0 <= j < self.board_size)  else None
        next_cell = self.board[j][i]

        for cell in self.colorList.copy():
            self.update_cells(cell, next_cell)

        if 0 <= i < self.board_size and 0 <= j < self.board_size:
            for cell in self.colorList:
                cell.color = next_cell.color

            self.num_of_clicks += 1
            self.completely_flooded = self.all_flooded()

    def all_flooded(self):
        return all(all(cell.color == self.board[0][0].color for cell in row) for row in self.board)

    def on_tick(self):
        self.timer += 1

    def on_key_event(self, key):
        if key == pygame.K_r:
            self.__init__(self.board_size, self.colors_avail)

    def draw(self, screen):
        for i in range(self.board_size):
            for j in range(self.board_size):
                self.board[i][j].draw(screen)

        font = pygame.font.SysFont(None, 30)
        text = font.render("Clicks: {} / {}".format(self.num_of_clicks, self.turns_given), True, pygame.Color("BLACK"))
        screen.blit(text, (10, 10))
        time = font.render("Time: {}".format(self.timer/10), True, pygame.Color("BLACK"))
        screen.blit(time, (10, 25))

        if self.completely_flooded:
            text = font.render("You Win!! :)", True, pygame.Color("BLUE"))
            screen.blit(text, (10, 40))
        elif self.num_of_clicks > self.turns_given:
            text = font.render("You Lose:(", True, pygame.Color("BLUE"))
            screen.blit(text, (10, 40))

# Main game loop
def main():
    pygame.init()
    world = FloodItGame(10, 8)

    screen = pygame.display.set_mode((world.board_size * CELL_SIZE, world.board_size * CELL_SIZE))
    pygame.display.set_caption("Flood It Game")

    clock = pygame.time.Clock()
    
    world = FloodItGame(10, 8)

    running = True
    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                world.on_mouse_click(pygame.mouse.get_pos())
            elif event.type == pygame.KEYDOWN:
                world.on_key_event(event.key)

        world.on_tick()

        screen.fill(pygame.Color("WHITE"))
        world.draw(screen)

        pygame.display.flip()
        clock.tick(10)

    pygame.quit()

if __name__ == "__main__":
    main()
