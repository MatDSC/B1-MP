import pygame
import os
from config import TILE_SIZE, SELECT_COLOR

class Renderer:
    def __init__(self, screen, board):
        self.screen = screen
        self.board = board
        self.images = self.load_images()

    def load_images(self):
        folder = "assets/images/pieces"
        def load(name):
            path = os.path.join(folder, name)
            return pygame.image.load(path).convert_alpha()

        return {
            "Pharaoh_RED": load("pharaon_red.png"),
            "Pharaoh_GRAY": load("pharaon_gray.png"),
            "Sphinx_RED": load("sphinx_red.png"),
            "Sphinx_GRAY": load("sphinx_gray.png"),
            "Scarab_RED": load("scarabe_red.png"),
            "Scarab_GRAY": load("scarabe_gray.png"),
            "Anubis_RED": load("anubis_red.png"),
            "Anubis_GRAY": load("anubis_gray.png"),
            "Pyramid_RED": load("pyramide_red.png"),
            "Pyramid_GRAY": load("pyramide_gray.png"),
        }

    def draw(self):
        self.screen.fill((30, 30, 30))
        for y in range(8):
            for x in range(10):
                rect = pygame.Rect(x * TILE_SIZE, y * TILE_SIZE, TILE_SIZE, TILE_SIZE)
                pygame.draw.rect(self.screen, (40, 40, 40), rect)
                pygame.draw.rect(self.screen, (80, 80, 80), rect, 1)
                piece = self.board.grid[y][x]
                if piece:
                    key = f"{type(piece).__name__}_{piece.owner}"
                    image = pygame.transform.scale(self.images[key], (TILE_SIZE, TILE_SIZE))
                    angle = {"N": 0, "E": -90, "S": -180, "W": -270}[piece.orientation]
                    rotated = pygame.transform.rotate(image, angle)
                    img_rect = rotated.get_rect(center=rect.center)
                    self.screen.blit(rotated, img_rect)

        if self.board.selected:
            sx, sy = self.board.selected.position
            pygame.draw.rect(self.screen, SELECT_COLOR, pygame.Rect(sx * TILE_SIZE, sy * TILE_SIZE, TILE_SIZE, TILE_SIZE), 3)

        laser_path = self.board.apply_laser()
        for lx, ly in laser_path:
            pygame.draw.circle(self.screen, (255, 0, 0), (lx * TILE_SIZE + TILE_SIZE // 2, ly * TILE_SIZE + TILE_SIZE // 2), 5)
