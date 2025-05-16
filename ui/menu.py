import pygame
import os
from config import SCREEN_WIDTH, SCREEN_HEIGHT

def show_main_menu(screen):
    # Charger et afficher le fond centré
    bg_path = os.path.join("assets", "images", "board_bg.png")
    if os.path.exists(bg_path):
        bg_image = pygame.image.load(bg_path).convert()
        bg_image = pygame.transform.scale(bg_image, (SCREEN_WIDTH, SCREEN_HEIGHT))
        screen.blit(bg_image, (0, 0))
    else:
        screen.fill((20, 15, 10))

    font = pygame.font.SysFont(None, 60)
    title = font.render("KHET - L'Égypte Stratégique", True, (230, 200, 100))
    instruction = pygame.font.SysFont(None, 36).render("Cliquez pour commencer", True, (255, 255, 255))

    title_rect = title.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 - 60))
    instr_rect = instruction.get_rect(center=(SCREEN_WIDTH // 2, SCREEN_HEIGHT // 2 + 20))

    screen.blit(title, title_rect)
    screen.blit(instruction, instr_rect)
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return True