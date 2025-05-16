import os

import pygame

from config import TILE_SIZE


class Renderer:
    def __init__(self, screen, board):
        self.screen = screen
        self.board = board
        self.images = self.load_images()

        # Chargement de l'image de fond
        bg_path = os.path.join("assets", "images", "board_bg.png")
        self.bg_image = pygame.image.load(bg_path).convert()
        self.bg_image = pygame.transform.scale(self.bg_image, (TILE_SIZE * 10, TILE_SIZE * 8))