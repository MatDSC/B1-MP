import pygame
from board import Board
from uirenderer import Renderer
from uievents import handle_events
from uimenu import show_main_menu

def main():
    pygame.init()
    screen = pygame.display.set_mode((800, 640))
    clock = pygame.time.Clock()

    if not show_main_menu(screen):
        return

    board = Board()
    board.place_test_pieces()
    renderer = Renderer(screen, board)

    running = True
    while running:
        running = handle_events(board)
        renderer.draw()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()