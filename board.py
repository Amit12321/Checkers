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
        self._init()

    def print_board(self):
        for i in range(ROWS):
            for j in range(COLS):
                print(self.board[i][j], end=" ")
            print()

    def _init(self):
        self.white_pieces = []
        self.black_pieces = []
        self.white_left = self.black_left = 12
        self.game_over = False
        self.winner = None
        self.board = [["0" for i in range(ROWS)] for j in range(COLS)]
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

    def check_for_possible_moves(self, color):
        pieces = []
        if color == BLACK:
            pieces = self.black_pieces
            for p in pieces:
                if self.get_moves(p.row, p.col) != []:
                    return True
            self.game_over = True
            self.winner = WHITE
        else:
            pieces = self.white_pieces
            for p in pieces:
                if self.get_moves(p.row, p.col) != []:
                    return True
            self.game_over = True
            self.winner = BLACK
        return False
    
    def search_left(self, r_start, r_stop, d, col, piece, skipped=[]):
        possible_moves = []
        last = []

        for r in range(r_start, r_stop, d):
            if col < 0:
                break
            
            current = self.board[r][col]
            if current == "0": #landed on an empty spot
                if skipped and last == []: #not the first square we have moved to, but last one was empty.
                    break
                if skipped:
                    possible_moves.append(Move(piece, r, col, skipped + last))
                else:
                    possible_moves.append(Move(piece, r, col, last))
                
                if last != []:
                    if d == 1:
                        row = min(ROWS, r + 3)
                    else:
                        row = max(-1, r - 3)
                    possible_moves += self.search_right(r + d, row, d, col + 1, piece, skipped = last)
                    possible_moves += self.search_left(r + d, row, d, col - 1, piece, skipped = last)
                break #If we reached this line, it means that previous square was empty (because otherwise we would have a recursive call in line 101/2) and current square is empty - we should break.
            elif current.color == piece.color:
                break
            else:
                last = skipped + [(r, col)]
                
            col -= 1

        return possible_moves

    def search_right(self, r_start, r_stop, d, col, piece, skipped = []):
        possible_moves = []
        last = []

        for r in range(r_start, r_stop, d):
            if col >= ROWS:
                break
            
            current = self.board[r][col]
            if current == "0": #landed on an empty spot
                if skipped and not last:
                    break
                if skipped:
                    possible_moves.append(Move(piece, r, col, skipped + last))
                else:
                    possible_moves.append(Move(piece, r, col, last))
                
                if last:
                    if d == 1:
                        row = min(ROWS, r + 3)
                    else:
                        row = max(-1, r - 3)
                    possible_moves += self.search_right(r + d, row, d, col + 1, piece, skipped = last)
                    possible_moves += self.search_left(r + d, row, d, col - 1, piece, skipped = last)
                break
            elif current.color == piece.color:
                break
            else:
                last = skipped + [(r, col)]

            col += 1

        return possible_moves

    def get_moves(self, row, col):
        piece = self.board[row][col]
        if piece == "0":
            return []
        possible_moves = []
        piece = self.board[row][col]
        right = col + 1
        left = col - 1
        if piece.color == WHITE or piece.king:
            possible_moves += self.search_left(row + 1, min(ROWS, row + 3), 1, left, piece)
            possible_moves += self.search_right(row + 1, min(ROWS, row + 3), 1, right, piece)
        if piece.color == BLACK or piece.king:
            possible_moves += self.search_left(row - 1, max(-1, row - 3), -1, left, piece)
            possible_moves += self.search_right(row - 1, max(-1, row - 3), -1, right, piece)
        
        return possible_moves

    def make_move(self, move):
        row = move.row_to
        col = move.col_to
        piece = move.piece
        self.board[piece.row][piece.col] = "0"
        self.board[row][col] = piece
        piece.update_pos(row, col)
        if move.eat:
            for eat in move.eat:
                i, j = eat
                if self.board[i][j] == "0":
                    continue
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

    def set_winner(self):
        if self.black_left == 0:
            self.game_over = True
            self.winner = WHITE
        elif self.white_left == 0:
            self.game_over = True
            self.winner = BLACK
    
