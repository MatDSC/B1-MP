import pygame
import sys

from games.board import Board
from ui.renderer import Renderer
from ui.menu import *
from ui.network_menu import select_game_mode
from config import TILE_SIZE
from network.sync import NetworkSync

pygame.init()
screen = pygame.display.set_mode((1600, 900))
pygame.display.set_caption("KHET 2.0 - The Laser Game")
clock = pygame.time.Clock()

def run_local_game(board, renderer):

    while True:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN and event.key == pygame.K_SPACE:
                board.apply_laser()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos()
                gx = (mx - renderer.offset_x) // TILE_SIZE
                gy = (my - renderer.offset_y) // TILE_SIZE
                if 0 <= gx < 10 and 0 <= gy < 8:
                    prev = board.selected
                    board.toggle_select((gx, gy))
                    if prev and not board.selected:
                        board.apply_laser()
                        board.end_turn()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and board.selected:
                orientations = ['N', 'E', 'S', 'W']
                idx = orientations.index(board.selected.orientation)
                board.selected.orientation = orientations[(idx + 1) % 4]
                #board.apply_laser()
                board.end_turn()

        renderer.draw()
        pygame.display.flip()
        clock.tick(60)

def run_online_game(board, renderer, net):
    while True:
        incoming = net.receive()
        if incoming:
            parts = incoming.split()
            cmd = parts[0]

            if cmd == 'MOVE':
                x, y = int(parts[1]), int(parts[2])
                board.toggle_select((x, y))
                board.toggle_select((x, y))
                board.apply_laser()
                board.end_turn()

            elif cmd == 'ROTATE':
                x, y = int(parts[1]), int(parts[2])
                piece = board.get_piece_at((x, y))
                if piece:
                    orientations = ['N', 'E', 'S', 'W']
                    idx = orientations.index(piece.orientation)
                    piece.orientation = orientations[(idx + 1) % 4]
                    board.apply_laser()
                    board.end_turn()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                net.close()
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                mx, my = pygame.mouse.get_pos()
                gx = (mx - renderer.offset_x) // TILE_SIZE
                gy = (my - renderer.offset_y) // TILE_SIZE
                if 0 <= gx < 10 and 0 <= gy < 8:
                    prev = board.selected
                    board.toggle_select((gx, gy))
                    if prev and not board.selected:
                        net.send(f"MOVE {gx} {gy}")
                        board.apply_laser()
                        board.end_turn()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 3 and board.selected:
                orientations = ['N', 'E', 'S', 'W']
                idx = orientations.index(board.selected.orientation)
                board.selected.orientation = orientations[(idx + 1) % 4]
                pos = board.selected.position
                net.send(f"ROTATE {pos[0]} {pos[1]}")
                board.apply_laser()
                board.end_turn()

        renderer.draw()
        pygame.display.flip()
        clock.tick(60)


def main():

    while True:
        choice = main_menu_loop(screen)

        if choice == "quit":
            pygame.quit()
            sys.exit()

        if choice == "local":
            board = Board()
            config_name = config_menu_loop(screen)
            if config_name == "back":
                continue
            for name, fn in board.configurations:
                if name == config_name:
                    fn(board)
                    break
            renderer = Renderer(screen, board)
            run_local_game(board, renderer)

        if choice == "online":
            mode_ip = select_game_mode(screen)
            if mode_ip == "back":
                continue

            net = NetworkSync(mode_ip)

            board = Board()
            config_name = config_menu_loop(screen)
            if config_name == "back":
                net.close()
                continue

            for name, fn in board.configurations:
                if name == config_name:
                    fn(board)
                    break

            renderer = Renderer(screen, board)
            run_online_game(board, renderer, net)





if __name__ == "__main__":
    main()
