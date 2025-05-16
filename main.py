import pygame
from games.board import Board
from ui.renderer import Renderer
from ui.events import handle_events
from ui.menu import show_main_menu

def main():
    pygame.init()
    screen = pygame.display.set_mode((1000, 850))
    clock = pygame.time.Clock()

    if not show_main_menu(screen):
        return

    board = Board()
    board.place_dynasty_setup()
    renderer = Renderer(screen, board)

    running = True
    while running:
        running = handle_events(board, renderer)
        #print(board.last_laser_path)
        renderer.draw()
        pygame.display.flip()
        clock.tick(60)

    pygame.quit()

if __name__ == "__main__":
    main()