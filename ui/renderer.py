import pygame
import os
from config import TILE_SIZE, SELECT_COLOR
from games.piece import Piece
import pygame.mixer

class Renderer:
    def __init__(self, screen, board):
        self.screen = screen
        self.board = board
        self.images = self.load_images()

        self.board_width = TILE_SIZE * 10
        self.board_height = TILE_SIZE * 8
        self.offset_x = (screen.get_width() - self.board_width) // 2
        self.offset_y = (screen.get_height() - self.board_height) // 2

        bg_path = os.path.join("assets", "images", "board_bg.png")


        if os.path.exists(bg_path):
            raw = pygame.image.load(bg_path).convert()
            self.bg_image = pygame.transform.scale(raw, (self.board_width, self.board_height))
        else:
            self.bg_image = None

        pygame.mixer.init()
        sound_path = os.path.join("assets", "sounds", "laser_hit.wav")
        self.laser_sound = pygame.mixer.Sound(sound_path) if os.path.exists(sound_path) else None

    def load_images(self):
        folder = "assets/images/pieces"
        def load(name):
            return pygame.image.load(os.path.join(folder, name)).convert_alpha()

        return {
            "Pharaon_RED": load("pharaon_red.png"),
            "Pharaon_GRAY": load("pharaon_gray.png"),
            "Sphinx_RED": load("sphinx_red.png"),
            "Sphinx_GRAY": load("sphinx_gray.png"),
            "Scarabee_RED": load("scarabe_red.png"),
            "Scarabee_GRAY": load("scarabe_gray.png"),
            "Anubis_RED": load("anubis_red.png"),
            "Anubis_GRAY": load("anubis_gray.png"),
            "Pyramide_RED": load("pyramide_red.png"),
            "Pyramide_GRAY": load("pyramide_gray.png"),
        }

    def draw(self):

        self.screen.fill((0, 0, 0))

        if self.bg_image:
            self.screen.blit(self.bg_image, (self.offset_x, self.offset_y))


        for y in range(8):
            for x in range(10):
                rect = pygame.Rect(
                    self.offset_x + x * TILE_SIZE,
                     self.offset_y + y * TILE_SIZE,
                     TILE_SIZE, TILE_SIZE
                )
                pygame.draw.rect(self.screen, (40, 40, 40), rect, 1)

        sel_piece = self.board.selected
        if isinstance(sel_piece, Piece):
            px, py = sel_piece.position

            sel_rect = pygame.Rect(
                self.offset_x + px * TILE_SIZE,
                self.offset_y + py * TILE_SIZE,
                TILE_SIZE, TILE_SIZE
            )
            pygame.draw.rect(self.screen, SELECT_COLOR, sel_rect, 4)

            highlight_color = (200,200, 0, 100)
            s = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
            s.fill(highlight_color)

            for dy in (-1, 0, 1):
                for dx in (-1, 0, 1):
                    if dx == 0 and dy == 0:
                        continue
                    tx, ty = px + dx, py + dy
                    if 0 <= tx < 10 and 0 <= ty < 8:
                        if self.board.is_valid_move(sel_piece, (tx, ty)):
                            self.screen.blit(
                                s,
                                (self.offset_x + tx * TILE_SIZE,
                                 self.offset_y + ty * TILE_SIZE)
                            )

        for y in range(8):
            for x in range(10):
                piece = self.board.get_piece_at((x, y))
                if piece:
                    key = f"{type(piece).__name__}_{piece.owner}"
                    img = pygame.transform.scale(self.images[key], (TILE_SIZE, TILE_SIZE))
                    angle = {"N": 0, "E": -90, "S": -180, "W": -270}[piece.orientation]
                    img_rot = pygame.transform.rotate(img, angle)
                    img_rect = img_rot.get_rect(center=(
                        self.offset_x + x * TILE_SIZE + TILE_SIZE // 2,
                        self.offset_y + y * TILE_SIZE + TILE_SIZE // 2
                    ))
                    self.screen.blit(img_rot, img_rect)

        if isinstance(sel_piece, Piece):
            px, py = sel_piece.position
            select_rect = pygame.Rect(
                self.offset_x + px * TILE_SIZE,
                self.offset_y + py * TILE_SIZE,
                TILE_SIZE, TILE_SIZE
            )
            pygame.draw.rect(self.screen, SELECT_COLOR, select_rect, 2)

        path = self.board.last_laser_path
        hit = self.board.last_laser_hit

        if len(path) > 1:
            for i in range(len(path) - 1):
                x0, y0 = path[i]
                x1, y1 = path[i + 1]
                start = (
                    self.offset_x + x0 * TILE_SIZE + TILE_SIZE // 2,
                    self.offset_y + y0 * TILE_SIZE + TILE_SIZE // 2
                )
                end = (
                    self.offset_x + x1 * TILE_SIZE + TILE_SIZE // 2,
                    self.offset_y + y1 * TILE_SIZE + TILE_SIZE // 2
                )
                pygame.draw.line(self.screen, (255, 0, 0), start, end, 3)

        if hit and self.laser_sound:
            self.laser_sound.play()
            self.board.last_laser_hit = None
