import pygame
import os
from config import TILE_SIZE, SELECT_COLOR
import pygame.mixer

class Renderer:
    def __init__(self, screen, board):
        self.screen = screen
        self.board = board
        # Chargement des sprites
        self.images = self.load_images()

        # Calcul dimensions et offsets pour centrer le plateau
        self.board_width = TILE_SIZE * 10
        self.board_height = TILE_SIZE * 8
        self.offset_x = (screen.get_width() - self.board_width) // 2
        self.offset_y = (screen.get_height() - self.board_height) // 2

        # Chargement de l'image de fond
        bg_path = os.path.join("assets", "images", "board_bg.png")
        if os.path.exists(bg_path):
            bg_img = pygame.image.load(bg_path).convert()
            self.bg_image = pygame.transform.scale(bg_img, (self.board_width, self.board_height))
        else:
            self.bg_image = None

        # Chargement du son laser
        pygame.mixer.init()
        sound_path = os.path.join("assets", "sounds", "laser_hit.wav")
        self.laser_sound = pygame.mixer.Sound(sound_path) if os.path.exists(sound_path) else None

    def load_images(self):
        folder = "assets/images/pieces"
        def load(name):
            return pygame.image.load(os.path.join(folder, name)).convert_alpha()

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
        # Met à jour la trajectoire du laser
        self.board.apply_laser()
        path = getattr(self.board, 'last_laser_path', [])
        hit = getattr(self.board, 'last_laser_hit', None)
        #print("DEBUG draw, laser path:", path)

        # Arrière-plan
        self.screen.fill((30, 30, 30))
        if self.bg_image:
            self.screen.blit(self.bg_image, (self.offset_x, self.offset_y))

        # Grille et pièces
        for y in range(8):
            for x in range(10):
                rect = pygame.Rect(
                    self.offset_x + x * TILE_SIZE,
                    self.offset_y + y * TILE_SIZE,
                    TILE_SIZE, TILE_SIZE
                )
                pygame.draw.rect(self.screen, (40, 40, 40), rect, 1)
                piece = self.board.grid[y][x]
                if piece:
                    key = f"{type(piece).__name__}_{piece.owner}"
                    sprite = pygame.transform.scale(self.images[key], (TILE_SIZE, TILE_SIZE))
                    angle = {"N": 0, "E": -90, "S": -180, "W": -270}[piece.orientation]
                    rotated = pygame.transform.rotate(sprite, angle)
                    img_rect = rotated.get_rect(center=rect.center)
                    self.screen.blit(rotated, img_rect)

        # Sélection
        if self.board.selected:
            sx, sy = self.board.selected.position
            sel_rect = pygame.Rect(
                self.offset_x + sx * TILE_SIZE,
                self.offset_y + sy * TILE_SIZE,
                TILE_SIZE, TILE_SIZE
            )
            pygame.draw.rect(self.screen, SELECT_COLOR, sel_rect, 3)

        pts = [(self.offset_x + x * TILE_SIZE + TILE_SIZE // 2,
                self.offset_y + y * TILE_SIZE + TILE_SIZE // 2)
               for x, y in path]

        try:
            pygame.draw.lines(self.screen, (255,0, 0), False, pts, 3)
        except ValueError:
            pass

        #for cx, cy in pts:
            #pygame.draw.circle(self.screen, (255, 255, 255), (cx, cy), TILE_SIZE // 6)
            # Jouer le son d'impact une seule fois
        if hit and self.laser_sound:
            self.laser_sound.play()
            self.board.last_laser_hit = None
