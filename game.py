import pygame
from board import Board, Move
from assets.constants import GREEN, WHITE, BLACK, SQUARE_SIZE, RED, GRAY

class Game:
    def __init__(self, win):
        self.bo = Board()
        self.win = win
        self.reset()
    
    def reset(self):
        self.bo._init()
        self.selected_square = None
        self.turn = BLACK
        self.bo.game_over = False
        self.bo.winner = None
        self.possible_moves = []
    
    def cancel_select(self):
        self.selected_square = None

    def select(self, row, col):
        if self.selected_square:
            res = self._move(row, col)
            if not res:
                self.selected_square = None
                self.possible_moves = []
                self.select(row, col)
        
        piece = self.bo.board[row][col]
        if piece != "0" and piece.color == self.turn:
            self.selected_square = (row, col)
            self.possible_moves = self.bo.get_moves(row, col)
            return True
        return False

    def _move(self, row, col):
        piece = self.bo.board[row][col]
        move = Move.check_if_possible(self.possible_moves, (row, col))
        if self.selected_square and piece == "0" and move:
            self.bo.make_move(move)
            self.selected_square = None
            self.possible_moves = []
            self.change_turn()
        else:
            return False    
        return True

    def draw(self):
        self.bo.draw(self.win)

        if self.selected_square != None:
            r, c = self.selected_square
            pygame.draw.rect(self.win, RED, (c * SQUARE_SIZE, r *
                                        SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 2)
        
        for move in self.possible_moves:
            pygame.draw.circle(self.win, GRAY, (move.col_to * SQUARE_SIZE + SQUARE_SIZE //
                                          2, move.row_to * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 6)

    
    def change_turn(self):
        if self.turn == BLACK:
            self.turn = WHITE
        else:
            self.turn = BLACK
    
    def game_over(self):
        return self.bo.game_over
    
    def winner(self):
        return self.bo.winner

    
