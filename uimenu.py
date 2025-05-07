import pygame
from config import SCREEN_WIDTH, SCREEN_HEIGHT

def show_main_menu(screen):
    font = pygame.font.SysFont(None, 60)
    title = font.render("KHET - L'Égypte Stratégique", True, (230, 200, 100))
    instruction = pygame.font.SysFont(None, 36).render("Cliquez pour commencer", True, (255, 255, 255))

    screen.fill((20, 15, 10))
    screen.blit(title, (SCREEN_WIDTH // 2 - title.get_width() // 2, 200))
    screen.blit(instruction, (SCREEN_WIDTH // 2 - instruction.get_width() // 2, 300))
    pygame.display.flip()

    waiting = True
    while waiting:
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                return False
            elif event.type == pygame.MOUSEBUTTONDOWN:
                return True