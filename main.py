import pygame
from board import Board, Move
from assets.constants import WIDTH, HEIGHT, RED, BLACK, WHITE, GREEN, GRAY, SQUARE_SIZE, ROWS, COLS
from game import Game

pygame.font.init()
window = pygame.display.set_mode((WIDTH, HEIGHT))
pygame.display.set_caption("Checkers")
FONT = pygame.font.SysFont("comicsans", 85)


def click(x, y):
    if x > 0 and x < WIDTH and y > 0 and y < HEIGHT:
        return (y // SQUARE_SIZE, x // SQUARE_SIZE)
    return None


def redraw(window, game):
    window.fill(WHITE)
    game.draw()
    if game.game_over():
        game_over_label = FONT.render("Game Over!!", 1, BLACK)
        play_again_label = FONT.render(
            "Press space to play again...", 1, BLACK)
        if game.winner() == WHITE:
            winner_label = FONT.render(
                "White Pieces Won.", 1, BLACK)
        else:
            winner_label = FONT.render(
                "Black Pieces Won.", 1, BLACK)
        window.blit(game_over_label, (window.get_width() // 2 - game_over_label.get_width() //
                                      2, window.get_height() // 2 - game_over_label.get_height() // 2))
        window.blit(winner_label, (window.get_width() // 2 - winner_label.get_width() // 2,
                                   window.get_height() // 2 - game_over_label.get_height() // 2 + game_over_label.get_height() + 5))
        window.blit(play_again_label, (window.get_width() // 2 - play_again_label.get_width() //
                                       2, window.get_height() - play_again_label.get_height() - 10))
    pygame.display.update()


def main():
    run = True
    FPS = 60
    clock = pygame.time.Clock()
    game = Game(window)

    while run:
        clock.tick(FPS)
        redraw(window, game)
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                run = False
            if event.type == pygame.MOUSEBUTTONDOWN:
                pos = pygame.mouse.get_pos()
                row, col = click(pos[0], pos[1])
                game.select(row, col)
                if game.game_over() == False:
                    game.bo.check_for_possible_moves(game.turn)

        keys = pygame.key.get_pressed()
        if keys[pygame.K_SPACE]:
            game.reset()
            redraw(window, game)
            reset_label = FONT.render("Reseting Game...", 1, BLACK)
            window.blit(reset_label, (window.get_width() // 2 - reset_label.get_width() //
                                      2, window.get_height() // 2 - reset_label.get_height() // 2))
            pygame.display.update()
            pygame.time.delay(1000)


main()
pygame.quit()
