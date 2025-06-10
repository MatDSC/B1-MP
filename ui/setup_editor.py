import os
import sys
import json
import pygame
from pygame.locals import (
    QUIT, KEYDOWN, K_ESCAPE, K_o, K_n,
    MOUSEBUTTONDOWN, K_BACKSPACE, K_RETURN
)

from games.piece import Pharaon, Sphinx, Scarabee, Pyramide, Anubis
from games.board import Board
from config import TILE_SIZE

pygame.font.init()
FONT    = pygame.font.SysFont('papyrus', 24)
BIGFONT = pygame.font.SysFont('papyrus', 32, bold=True)


def ensure_configs_dir():
    this_dir     = os.path.dirname(__file__)
    project_root = os.path.abspath(os.path.join(this_dir, os.pardir))
    cfg_dir      = os.path.join(project_root, "assets", "configs")
    os.makedirs(cfg_dir, exist_ok=True)
    return cfg_dir

def list_custom_configs():
    cfg_dir = ensure_configs_dir()
    return sorted(fname[:-5] for fname in os.listdir(cfg_dir) if fname.endswith(".json"))

def save_config(board, name):
    cfg_dir = ensure_configs_dir()
    data = []
    for piece in board.pieces:
        data.append({
            "type":        piece.__class__.__name__,
            "owner":       piece.owner,
            "orientation": piece.orientation,
            "position":    piece.position
        })
    path = os.path.join(cfg_dir, f"{name}.json")
    with open(path, "w", encoding="utf8") as f:
        json.dump(data, f, indent=2)

def load_config(board, name):
    cfg_dir = ensure_configs_dir()
    path = os.path.join(cfg_dir, f"{name}.json")
    board.clear()
    if not os.path.exists(path):
        return
    with open(path, "r", encoding="utf8") as f:
        data = json.load(f)
    cls_map = {
        "Pharaon":  Pharaon,
        "Sphinx":   Sphinx,
        "Scarabee":   Scarabee,
        "Pyramide":  Pyramide,
        "Anubis":   Anubis
    }
    for item in data:
        cls   = cls_map[item["type"]]
        piece = cls(tuple(item["position"]), item["orientation"], item["owner"])
        board.add_piece(piece)

def delete_config(name):
    cfg_dir = ensure_configs_dir()
    path = os.path.join(cfg_dir, f"{name}.json")
    if os.path.exists(path):
        os.remove(path)

def rename_config(old_name, new_name):
    cfg_dir  = ensure_configs_dir()
    old_path = os.path.join(cfg_dir, f"{old_name}.json")
    new_path = os.path.join(cfg_dir, f"{new_name}.json")
    if os.path.exists(old_path):
        os.replace(old_path, new_path)


class SetupEditor:
    PIECE_TYPES = [Pharaon, Sphinx, Scarabee, Pyramide, Anubis]

    def __init__(self, screen):
        self.screen = screen
        self.width, self.height = screen.get_size()
        self.board = Board()

        self.selected_piece_type  = Pharaon
        self.selected_owner       = "RED"
        self.selected_orientation = "N"

        self.configs = list_custom_configs()
        self.selected_config_idx = 0 if self.configs else -1

        self.awaiting_name = False
        self.name_input    = ""
        self.rename_mode   = False

        self._preload_all_piece_images()

        board_w  = TILE_SIZE * 10
        board_h  = TILE_SIZE * 8
        board_x  = (self.width  - board_w)  // 2
        board_y  = (self.height - board_h) // 2
        self.board_rect = pygame.Rect(board_x, board_y, board_w, board_h)

        list_w  = 220
        list_h  = self.height - 300
        list_x  = board_x - list_w - 20
        list_y  = board_y
        self.list_rect = pygame.Rect(list_x, list_y, list_w, list_h)

        btn_w     = 180
        btn_h     = 50
        btn_gap   = 30
        total_w   = btn_w + (btn_w + btn_gap) + (btn_w + btn_gap)
        start_x   = board_x + (board_w - total_w) // 2
        y_buttons = board_y + board_h + 40  # 40 px sous le plateau
        self.save_rect   = pygame.Rect(start_x, y_buttons, btn_w, btn_h)
        self.rename_rect = pygame.Rect(start_x + btn_w + btn_gap, y_buttons, btn_w, btn_h)
        self.delete_rect = pygame.Rect(start_x + (btn_w + btn_gap)*2, y_buttons, btn_w, btn_h)

        self.back_rect = pygame.Rect(self.width - 180 - 20, self.height - btn_h - 20, 180, btn_h)

        self.icon_size  = 40
        self.icon_gap   = 10
        self.icon_rects = {}
        x0 = board_x
        y0 = board_y - self.icon_size - 40
        prefix_map = {
            "Pharaon": "pharaon_red.png",
            "Sphinx":  "sphinx_red.png",
            "Scarabee":  "scarabe_red.png",
            "Pyramide": "pyramide_red.png",
            "Anubis":  "anubis_red.png"
        }
        for i, cls in enumerate(self.PIECE_TYPES):
            rect = pygame.Rect(
                x0 + i * (self.icon_size + self.icon_gap),
                y0,
                self.icon_size,
                self.icon_size
            )
            path = os.path.join("assets", "images", "pieces", prefix_map[cls.__name__])
            if os.path.exists(path):
                surf = pygame.image.load(path).convert_alpha()
                surf = pygame.transform.scale(surf, (self.icon_size, self.icon_size))
            else:
                surf = pygame.Surface((self.icon_size, self.icon_size), pygame.SRCALPHA)
            self.icon_rects[cls] = {"rect": rect, "surf": surf}


    def _preload_all_piece_images(self):

        folder = os.path.join("assets", "images", "pieces")
        self.piece_sprites = {}
        name_map = {
            "Pharaon":  "pharaon_",
            "Sphinx":   "sphinx_",
            "Scarabee":   "scarabe_",
            "Pyramide":  "pyramide_",
            "Anubis":   "anubis_"
        }
        for cls_name, prefix in name_map.items():
            for owner in ("RED", "GRAY"):
                filename = f"{prefix}{owner.lower()}.png"
                path     = os.path.join(folder, filename)
                if os.path.exists(path):
                    surf = pygame.image.load(path).convert_alpha()
                else:
                    surf = pygame.Surface((TILE_SIZE, TILE_SIZE), pygame.SRCALPHA)
                self.piece_sprites[(cls_name, owner)] = surf


    def draw(self):
        screen = self.screen

        screen.fill((0, 0, 0))

        title_surf = BIGFONT.render("Éditeur de configuration", True, (255, 215, 0))
        screen.blit(title_surf, ((self.width - title_surf.get_width()) // 2, 20))

        for cls, info in self.icon_rects.items():
            rect = info["rect"]
            surf = info["surf"]
            if cls is self.selected_piece_type:
                pygame.draw.rect(screen, (255, 215, 0), rect.inflate(4, 4), 2)
            screen.blit(surf, rect.topleft)

        pygame.draw.rect(screen, (50, 50, 50), self.list_rect)
        y0 = self.list_rect.y + 10
        for idx, name in enumerate(self.configs):
            color = (255, 215, 0) if idx == self.selected_config_idx else (255, 255, 255)
            text  = FONT.render(name, True, color)
            screen.blit(text, (self.list_rect.x + 10, y0 + idx * 30))

        pygame.draw.rect(screen, (70, 70, 70), self.save_rect)
        txt = FONT.render("Sauvegarder", True, (255, 255, 255))
        screen.blit(txt, txt.get_rect(center=self.save_rect.center))

        pygame.draw.rect(screen, (70, 70, 70), self.rename_rect)
        txt = FONT.render("Renommer", True, (255, 255, 255))
        screen.blit(txt, txt.get_rect(center=self.rename_rect.center))

        pygame.draw.rect(screen, (70, 70, 70), self.delete_rect)
        txt = FONT.render("Supprimer", True, (255, 255, 255))
        screen.blit(txt, txt.get_rect(center=self.delete_rect.center))

        pygame.draw.rect(screen, (70, 70, 70), self.back_rect)
        txt = FONT.render("Retour", True, (255, 255, 255))
        screen.blit(txt, txt.get_rect(center=self.back_rect.center))

        pygame.draw.rect(screen, (100, 100, 100), self.board_rect)
        for row in range(8):
            for col in range(10):
                cell = pygame.Rect(
                    self.board_rect.x + col * TILE_SIZE,
                    self.board_rect.y + row * TILE_SIZE,
                    TILE_SIZE, TILE_SIZE
                )
                pygame.draw.rect(screen, (150, 150, 150), cell, 1)

        for piece in self.board.pieces:
            px, py = piece.position
            cls_name = piece.__class__.__name__
            owner    = piece.owner
            sprite = self.piece_sprites.get((cls_name, owner))
            if sprite:
                img = pygame.transform.scale(sprite, (TILE_SIZE, TILE_SIZE))
                angle = {"N": 0, "E": -90, "S": -180, "W": -270}[piece.orientation]
                img_rot = pygame.transform.rotate(img, angle)
                center_px = self.board_rect.x + px * TILE_SIZE + TILE_SIZE // 2
                center_py = self.board_rect.y + py * TILE_SIZE + TILE_SIZE // 2
                rect = img_rot.get_rect(center=(center_px, center_py))
                screen.blit(img_rot, rect)

        info = f"Pièce : {self.selected_piece_type.__name__ if self.selected_piece_type else 'None'}  |  "
        info += f"Joueur : {self.selected_owner}  |  Orientation : {self.selected_orientation}"
        info_surf = FONT.render(info, True, (255, 255, 255))
        screen.blit(info_surf, (self.board_rect.x, self.board_rect.y - 40))

        if self.awaiting_name:
            prompt = "Entrer le nom de la config :" if not self.rename_mode else "Renommer en :"
            prompt_surf = FONT.render(prompt, True, (255, 255, 255))
            screen.blit(prompt_surf, (self.board_rect.x, self.board_rect.y + TILE_SIZE * 8 + 10))

            input_rect = pygame.Rect(
                self.board_rect.x + 150,
                self.board_rect.y + TILE_SIZE * 8 + 10,
                250,
                35
            )
            pygame.draw.rect(screen, (0, 0, 0), input_rect)
            pygame.draw.rect(screen, (255, 255, 255), input_rect, 2)
            text_surf = FONT.render(self.name_input, True, (255, 215, 0))
            screen.blit(text_surf, (input_rect.x + 5, input_rect.y + 5))

        pygame.display.flip()


    def run(self):
        clock = pygame.time.Clock()
        while True:
            for event in pygame.event.get():
                if event.type == QUIT:
                    pygame.quit()
                    sys.exit()

                if self.awaiting_name:
                    if event.type == KEYDOWN:
                        if event.key == K_RETURN:
                            name = self.name_input.strip()
                            if name:
                                if self.rename_mode and 0 <= self.selected_config_idx < len(self.configs):
                                    old = self.configs[self.selected_config_idx]
                                    rename_config(old, name)
                                else:
                                    save_config(self.board, name)
                                self.configs = list_custom_configs()
                                self.awaiting_name = False
                                self.name_input    = ""
                                self.rename_mode   = False
                                if name in self.configs:
                                    self.selected_config_idx = self.configs.index(name)
                        elif event.key == K_BACKSPACE:
                            self.name_input = self.name_input[:-1]
                        elif event.key == K_ESCAPE:
                            self.awaiting_name = False
                            self.name_input    = ""
                            self.rename_mode   = False
                        else:
                            char = event.unicode
                            if char.isalnum() or char in (" ", "_", "-"):
                                self.name_input += char
                    continue

                if event.type == KEYDOWN:
                    if event.key == K_ESCAPE:
                        return
                    elif event.key == K_o:
                        self.selected_owner = "GRAY" if self.selected_owner == "RED" else "RED"
                    elif event.key == K_n:
                        orients = ["N", "E", "S", "W"]
                        idx = orients.index(self.selected_orientation)
                        self.selected_orientation = orients[(idx + 1) % 4]

                if event.type == MOUSEBUTTONDOWN:
                    mx, my = pygame.mouse.get_pos()

                    for cls, info in self.icon_rects.items():
                        if info["rect"].collidepoint(mx, my):
                            self.selected_piece_type = cls
                            break

                    if self.board_rect.collidepoint(mx, my):
                        bx = (mx - self.board_rect.x) // TILE_SIZE
                        by = (my - self.board_rect.y) // TILE_SIZE
                        if 0 <= bx < 10 and 0 <= by < 8:
                            existing = self.board.get_piece_at((bx, by))
                            if event.button == 1:
                                if existing:
                                    self.board.grid[by][bx] = None
                                    self.board.pieces.remove(existing)
                                else:
                                    piece = self.selected_piece_type(
                                        (bx, by),
                                        self.selected_orientation,
                                        self.selected_owner
                                    )
                                    self.board.add_piece(piece)
                            elif event.button == 3 and existing:
                                orients = ["N", "E", "S", "W"]
                                idx = orients.index(existing.orientation)
                                existing.orientation = orients[(idx + 1) % 4]
                        continue

                    if self.save_rect.collidepoint(mx, my):
                        self.awaiting_name = True
                        self.rename_mode   = False
                        self.name_input    = ""
                        continue

                    if self.rename_rect.collidepoint(mx, my) and self.selected_config_idx >= 0:
                        self.awaiting_name = True
                        self.rename_mode   = True
                        self.name_input    = self.configs[self.selected_config_idx]
                        continue

                    if self.delete_rect.collidepoint(mx, my) and self.selected_config_idx >= 0:
                        to_del = self.configs[self.selected_config_idx]
                        delete_config(to_del)
                        self.configs = list_custom_configs()
                        self.selected_config_idx = min(self.selected_config_idx, len(self.configs) - 1)
                        self.board.clear()
                        continue

                    if self.back_rect.collidepoint(mx, my):
                        return

                    if self.list_rect.collidepoint(mx, my):
                        rel_y = my - self.list_rect.y
                        idx   = rel_y // 30
                        if 0 <= idx < len(self.configs):
                            self.selected_config_idx = idx
                            load_config(self.board, self.configs[idx])
                        continue

            # ————— 2) APRÈS AVOIR TRAITÉ TOUS LES ÉVÉNEMENTS, ON DESSINE —————
            self.draw()
            clock.tick(30)


def setup_editor_loop(screen):
    editor = SetupEditor(screen)
    editor.run()
