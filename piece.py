from assets.constants import WHITE, GRAY, GREEN, BLACK, WIDTH, HEIGHT, ROWS, COLS, SQUARE_SIZE
import pygame
import os

BLACK_PIECE = pygame.image.load(os.path.join("images", "blackpiece.png"))
WHITE_PIECE = pygame.image.load(os.path.join("images", "whitepiece.png"))
BLACK_KING = pygame.image.load(os.path.join("images", "blackking.png"))
WHITE_KING = pygame.image.load(os.path.join("images", "whiteking.png"))


class Piece:
    OUTLINE = 2

    def __init__(self, color, row, col):
        self.color = color
        self.img = None
        self.king = False
        self.set_img()
        self.row = row
        self.col = col
        self.x = self. y = 0
        self.find_pos()
        self.radius = SQUARE_SIZE // 3

    def set_img(self):
        if self.color == WHITE and self.king:
            self.img = WHITE_KING
        elif self.color == WHITE:
            self.img = WHITE_PIECE
        elif self.color == BLACK and self.king:
            self.img = BLACK_KING
        else:
            self.img = BLACK_PIECE

    def find_pos(self):
        self.x = self.col * SQUARE_SIZE + SQUARE_SIZE // 2
        self.y = self.row * SQUARE_SIZE + SQUARE_SIZE // 2

    def draw(self, win):
        if self.color == WHITE:
            win.blit(self.img, (self.x - SQUARE_SIZE + self.img.get_width() -
                            6, self.y - SQUARE_SIZE + self.img.get_height() - 3))
        else:
            win.blit(self.img, (self.x - SQUARE_SIZE + self.img.get_width() -
                            6, self.y - SQUARE_SIZE + self.img.get_height() - 6))
        

    def update_pos(self, row, col):
        self.row = row
        self.col = col
        self.find_pos()

    def make_king(self):
        self.king = True
        self.set_img()

    def __str__(self):
        if self.color == WHITE:
            return "W"
        else:
            return "B"
