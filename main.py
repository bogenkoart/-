import pygame
from random import shuffle


class Board:
    def __init__(self, width, height, lot):
        self.width = width
        self.height = height
        self.kol = [-1] * (self.width * self.height - lot) + [10] * lot
        shuffle(self.kol)

        self.board = [[0] * width for _ in range(height)]
        k = 0
        for i in range(self.height):
            for j in range(self.width):
                self.board[i][j] = self.kol[k]
                k += 1
        self.left = 10
        self.top = 10
        self.cell_size = 30

    def set_view(self, left, top, cell_size):
        self.left = left
        self.top = top
        self.cell_size = cell_size

    def render(self, data):
        font = pygame.font.Font(None, 22)
        x = self.left
        y = self.top
        for i in self.board:
            for j in i:
                pygame.draw.rect(data, pygame.Color('white'),
                                 pygame.Rect(x, y, self.cell_size, self.cell_size), width=1)
                if j == 10:
                    pygame.draw.rect(data, pygame.Color('red'),
                                     pygame.Rect(x + 1, y + 1, self.cell_size - 2, self.cell_size - 2))
                if j != 10 and j != -1:
                    text = font.render(str(j), True, pygame.Color('green'))
                    text_x, text_y = x + 4, y + 4
                    screen.blit(text, (text_x, text_y))
                x += self.cell_size
            x = self.left
            y += self.cell_size

    def get_cell(self, mouse_pos):
        x = mouse_pos[0]
        y = mouse_pos[1]
        if (x not in range(self.left, self.left + self.width * self.cell_size)) or \
                (y not in range(self.top, self.top + self.height * self.cell_size)):
            return None
        else:
            a = int((x - self.left) / self.cell_size)
            b = int((y - self.top) / self.cell_size)
            return a, b

    def on_click(self, pos):
        x = pos[0]
        y = pos[1]
        lot = 0
        if self.board[y][x] != 10:
            for n in range(-1, 2):
                for m in range(-1, 2):
                    if (n != 0 or m != 0) and self.height > y + n >= 0 and self.width > x + m >= 0:
                        if self.board[y + n][x + m] == 10:
                            lot += 1
            self.board[y][x] = lot


class Minesweeper(Board):
    def open_cell(self, mouse_pos):
        cell = self.get_cell(mouse_pos)
        if cell != None:
            self.on_click(cell)


if __name__ == '__main__':
    a, b, k = list(map(int, input().split()))
    minesweeper = Minesweeper(a, b, k)
    pygame.init()
    pygame.display.set_caption('Дедушка сапёра')
    size = width, height = a * 30 + 20, b * 30 + 20
    screen = pygame.display.set_mode(size)
    running = True

    while running:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                running = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                minesweeper.open_cell(event.pos)
        screen.fill((0, 0, 0))
        minesweeper.render(screen)
        pygame.display.flip()
