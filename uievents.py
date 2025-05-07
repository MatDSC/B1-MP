import pygame
from config import TILE_SIZE

def handle_events(board):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False
        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            x, y = mx // TILE_SIZE, my // TILE_SIZE
            board.toggle_select((x, y))
    return True