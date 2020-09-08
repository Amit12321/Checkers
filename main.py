import pygame
from board import Board
from assets.constants import WIDTH, HEIGHT, RED, BLACK, WHITE, GREEN, GRAY, SQUARE_SIZE, ROWS, COLS

pygame.font.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers")
FONT = pygame.font.SysFont("comicsansms", 80, 1)

def redraw(window, board, possible_moves, winner):
    window.fill(WHITE)
    board.draw(window)
    for pos in possible_moves:
        pygame.draw.circle(window, GRAY, (pos[1] * SQUARE_SIZE + SQUARE_SIZE // 2, pos[0] * SQUARE_SIZE + SQUARE_SIZE // 2), SQUARE_SIZE // 5)
    if winner != None:
        game_over_label = FONT.render("Game Over!!", 1, BLACK)
        if winner == WHITE:
            winner_label = FONT.render("White Pieces Won.", 1, BLACK)
        else:
            winner_label = FONT.render("Black Pieces Won.", 1, BLACK)
        window.blit(game_over_label, (window.get_width() // 2 - game_over_label.get_width() // 2, window.get_height() // 2 - game_over_label.get_height() // 2))
        window.blit(winner_label, (window.get_width() // 2 - winner_label.get_width() // 2, window.get_height() // 2 - game_over_label.get_height() // 2 + game_over_label.get_height() + 5))
        pygame.time.delay(2000)
    pygame.display.update()

def main():
    run = True
    FPS = 60
    clock = pygame.time.Clock()
    board = Board()
    current = board.turn
    possible_moves = []
    piece = None
    eat = None
    winner = None
    while run:
        clock.tick(FPS)
        current = board.turn
        board.check_for_possible_moves(current)
        redraw(window, board, possible_moves, winner)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                clicked = board.click(pos[0], pos[1])
                if clicked and board.game_over == False:
                    if clicked in possible_moves:
                        board.make_move(piece, clicked[0], clicked[1], eat)
                        board.change_turn() 
                        board.cancel_select()
                        possible_moves = []
                        eat = None
                    else:
                        piece = board.board[clicked[0]][clicked[1]]
                        if piece != "0" and piece.color == current:
                            possible_moves, eat = board.get_moves(clicked[0], clicked[1], piece)
                            board.select(clicked[0], clicked[1])
                        else:
                            possible_moves = []
                            board.cancel_select()
        if board.game_over:
            winner = board.winner
        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            board.init_board()
            current = board.turn
            possible_moves = []
            piece = None
            eat = None
            winner = None
            redraw(window, board, possible_moves, winner)
            reset_label = FONT.render("Reseting Game...", 1, BLACK)
            window.blit(reset_label, (window.get_width() // 2 - reset_label.get_width() // 2, window.get_height() // 2 - reset_label.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(1000)
            


main()
pygame.quit()
