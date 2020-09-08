import pygame
from piece import Piece
from assets.constants import WHITE, GREEN, RED, BLACK, WIDTH, HEIGHT, ROWS, COLS, SQUARE_SIZE


class Move:
    def __init__(self, piece, row_to, col_to, eat):
        self.piece = piece
        self.row_to = row_to
        self.col_to = col_to
        self.eat = eat

    @staticmethod
    def check_if_possible(possible_moves, pos):
        for move in possible_moves:
            if pos[0] == move.row_to and pos[1] == move.col_to:
                return move
        return None


class Board:
    def __init__(self):
        self.board = [["0" for i in range(ROWS)] for j in range(COLS)]
        self.init_board()

    def print_board(self):
        for i in range(ROWS):
            for j in range(COLS):
                print(self.board[i][j], end=" ")
            print()

    def init_board(self):
        self.board = [["0" for i in range(ROWS)] for j in range(COLS)]
        self.white_pieces = []
        self.black_pieces = []
        self.selected_square = None
        self.turn = BLACK
        self.black_left = 12
        self.white_left = 12
        self.game_over = False
        self.winner = None
        for i in range(ROWS // 2 - 1):
            for j in range(1 - i % 2, COLS, 2):
                self.board[i][j] = Piece(WHITE, i, j)
                self.white_pieces.append(self.board[i][j])

        for i in range(ROWS // 2 + 1, ROWS):
            for j in range(1 - i % 2, COLS, 2):
                self.board[i][j] = Piece(BLACK, i, j)
                self.black_pieces.append(self.board[i][j])

    def draw(self, win):
        win.fill(WHITE)
        for i in range(ROWS):
            for j in range(1 - i % 2, COLS, 2):
                pygame.draw.rect(win, GREEN, (j * SQUARE_SIZE,
                                              i * SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE))

        for i in range(ROWS):
            for j in range(COLS):
                if self.board[i][j] != "0":
                    self.board[i][j].draw(win)

        if self.selected_square != None:
            r, c = self.selected_square
            pygame.draw.rect(win, RED, (c * SQUARE_SIZE, r *
                                        SQUARE_SIZE, SQUARE_SIZE, SQUARE_SIZE), 2)

    def click(self, x, y):
        if x > 0 and x < WIDTH and y > 0 and y < HEIGHT:
            return (y // SQUARE_SIZE, x // SQUARE_SIZE)
        return None

    def cancel_select(self):
        self.selected_square = None

    def select(self, row, col):
        self.selected_square = (row, col)

    def check_for_possible_moves(self, color):
        pieces = []
        if color == BLACK:
            pieces = self.black_pieces
            for p in pieces:
                if self.get_moves(p.row, p.col, p) != []:
                    return True
            self.game_over = True
            self.winner = WHITE
        else:
            pieces = self.white_pieces
            for p in pieces:
                if self.get_moves(p.row, p.col, p) != []:
                    return True
            self.game_over = True
            self.winner = BLACK
        return False

    def get_moves(self, row, col, piece):
        possible_moves = []  # list of rows, cols
        if self.board[row][col] != "0":
            d = piece.direction
            if row + d >= 0 and row + d < ROWS and col + d >= 0 and col + d < COLS:
                if self.board[row + d][col + d] == "0":
                    possible_moves.append(Move(piece, row + d, col + d, None))
                elif self.board[row + d][col + d].color != piece.color:
                    if row + 2*d >= 0 and row + 2*d < ROWS and col + 2*d >= 0 and \
                            col + 2*d < COLS and self.board[row + 2*d][col + 2*d] == "0":
                        possible_moves.append(
                            Move(piece, row + 2*d, col + 2*d, (row + d, col + d)))
            if row + d >= 0 and row + d < ROWS and col - d >= 0 and col - d < COLS:
                if self.board[row + d][col - d] == "0":
                    possible_moves.append(Move(piece, row + d, col - d, None))
                elif self.board[row + d][col - d].color != piece.color:
                    if row + 2*d >= 0 and row + 2*d < ROWS and col - 2*d >= 0 and \
                            col - 2*d < COLS and self.board[row + 2*d][col - 2*d] == "0":
                        possible_moves.append(
                            Move(piece, row + 2*d, col - 2*d, (row + d, col - d)))

            if piece.king and row - d >= 0 and row - d < ROWS and col - d >= 0 and col - d < COLS:
                if self.board[row - d][col - d] == "0":
                    possible_moves.append(Move(piece, row - d, col - d, None))
                elif self.board[row - d][col - d].color != piece.color:
                    if row - 2*d >= 0 and row - 2*d < ROWS and col - 2*d >= 0 and \
                            col - 2*d < COLS and self.board[row - 2*d][col - 2*d] == "0":
                        possible_moves.append(
                            Move(piece, row - 2*d, col - 2*d, (row - d, col - d)))
            if piece.king and row - d >= 0 and row - d < ROWS and col + d >= 0 and col + d < COLS:
                if self.board[row - d][col + d] == "0":
                    possible_moves.append(Move(piece, row - d, col + d, None))
                elif self.board[row - d][col + d].color != piece.color:
                    if row - 2*d >= 0 and row - 2*d < ROWS and col + 2*d >= 0 and \
                            col + 2*d < COLS and self.board[row - 2*d][col + 2*d] == "0":
                        possible_moves.append(
                            Move(piece, row - 2*d, col + 2*d, (row - d, col + d)))

        return possible_moves

    def make_move(self, move):
        row = move.row_to
        col = move.col_to
        piece = move.piece
        eat = move.eat
        self.board[piece.row][piece.col] = "0"
        self.board[row][col] = piece
        piece.update_pos(row, col)
        if eat:
            i, j = eat
            if piece.color == BLACK:
                self.white_pieces.remove(self.board[i][j])
                self.white_left -= 1
            else:
                self.black_pieces.remove(self.board[i][j])
                self.black_left -= 1
            self.board[i][j] = "0"
            self.set_winner()
        if (piece.color == BLACK and row == 0) or (piece.color == WHITE and row == ROWS - 1):
            piece.make_king()

    def change_turn(self):
        if self.turn == BLACK:
            self.turn = WHITE
        else:
            self.turn = BLACK

    def set_winner(self):
        if self.black_left == 0:
            self.game_over = True
            self.winner = WHITE
        elif self.white_left == 0:
            self.game_over = True
            self.winner = BLACK
