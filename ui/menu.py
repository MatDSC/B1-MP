import pygame
import sys
import os
from ui.setup_editor import setup_editor_loop

pygame.font.init()
TITLE_FONT = pygame.font.SysFont("papyrus", 60, bold=True)
MENU_FONT = pygame.font.SysFont("papyrus", 36)

MENU_OPTIONS = [
    ("Multijoueur en ligne", "online"),
    ("Multijoueur en local", "local"),
    ("Quitter", "quit")
]

ONLINE_OPTIONS = [
    ("Heberger une partie", "host"),
    ("Rejoindre une partie", "join"),
    ("Retour", "back")
]

CONFIG_OPTIONS = [
    ("Classique", "Classique"),
    ("Imhotep", "Imhotep"),
    ("Dynasty", "Dynasty"),
    ("Personnalisé", "Custom"),
    ("Retour", "back")
]

def load_background(screen):
    background_path = os.path.join("assets", "images", "menu_bg.png")
    if os.path.exists(background_path):
        raw = pygame.image.load(background_path).convert()
        return pygame.transform.scale(raw, screen.get_size())
    return None

def draw_menu(screen, background, title_text, options, selected_idx):
    screen.fill((0, 0, 0))
    if background:
        screen.blit(background, (0, 0))

    title_surf = TITLE_FONT.render(title_text, True, (255, 215, 0))
    screen.blit(title_surf, (screen.get_width() // 2 - title_surf.get_width() // 2, 60))

    mx, my = pygame.mouse.get_pos()
    hovored_idx = selected_idx

    for i, (label, _) in enumerate(options):
        color = (255, 0, 0) if i == selected_idx else (255, 255, 255)
        text_surf = MENU_FONT.render(label, True, color)
        text_rect = text_surf.get_rect(center=(screen.get_width() // 2, 180 + i * 60))
        if text_rect.collidepoint(mx, my):
            hovored_idx = i
            pygame.draw.rect(screen, (255, 255, 255), text_rect.inflate(20, 10), 2)
        screen.blit(text_surf, text_rect.topleft)

    pygame.display.flip()
    return hovored_idx


def main_menu_loop(screen):
    background = load_background(screen)
    clock = pygame.time.Clock()
    selected = 0

    while True:
        selected = draw_menu(screen, background, "KHET 2.0 - THE LASER GAME", MENU_OPTIONS, selected)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and selected != -1:
                choice = MENU_OPTIONS[selected][1]
                return choice

        clock.tick(60)

def online_menu_loop(screen):
    background = load_background(screen)
    clock = pygame.time.Clock()
    selected = 0

    while True:
        selected = draw_menu(screen, background, "Multijoueur en ligne", ONLINE_OPTIONS, selected)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1 and selected != -1:
                return ONLINE_OPTIONS[selected][1]

        clock.tick(60)

def config_menu_loop(screen):
    background = load_background(screen)
    clock = pygame.time.Clock()
    selected = 0

    while True:
        selected = draw_menu(screen, background, "Choisissez la configuration", CONFIG_OPTIONS, selected)

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                choice = CONFIG_OPTIONS[selected][1]
                if choice == "Custom":
                    setup_editor_loop(screen)
                    break
                else:
                    return choice

        pygame.display.flip()
        clock.tick(60)
