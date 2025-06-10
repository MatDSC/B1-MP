import pygame
import sys
import os

pygame.font.init()
FONT = pygame.font.SysFont("papyrus", 36)

def load_background(screen):
    this_dir = os.path.dirname(__file__)
    project_root = os.path.abspath(os.path.join(this_dir, os.pardir))
    bg_path = os.path.join(project_root, "assets", "images", "menu_bg.png")

    if os.path.exists(bg_path):
        raw = pygame.image.load(bg_path).convert()
        return pygame.transform.scale(raw, screen.get_size())
    else:
        print(f"[load_background] Impossible de trouver : {bg_path}")
        return None

def ask_for_ip(screen):
    clock = pygame.time.Clock()
    input_str = ""
    prompt_surf = FONT.render("Entrer l'adresse IP hôte (ou ECHAP pour annuler):", True, (255, 255, 255))
    background = load_background(screen)

    while True:
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.blit(30, 30, 30)

        screen.blit(prompt_surf, (50, 200))
        ip_surf = FONT.render(input_str, True, (255, 255, 20))
        ip_rect = ip_surf.get_rect(topleft=(50, 260))
        padding_x = 10
        padding_y = 5
        bg_rect = pygame.Rect(
            ip_rect.x - padding_x,
            ip_rect.y - padding_y,
            ip_rect.width + padding_x * 2,
            ip_rect.height + padding_y * 2

        )
        pygame.draw.rect(screen, (0, 0, 0), bg_rect)

        screen.blit(ip_surf, ip_rect.topleft)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_RETURN:
                    if len(input_str.strip()) > 0:
                        return input_str.strip()
                elif event.key == pygame.K_BACKSPACE:
                    input_str = input_str[:-1]
                elif event.key == pygame.K_ESCAPE:
                    return "back"
                else:
                    char = event.unicode
                    if (char.isdigit() or char == "." or char == ":"):
                        input_str += char

        clock.tick(30)

def select_game_mode(screen):
    options = ["Héberger une partie", "Rejoindre une partie", "Retour"]
    values  = ["host",     "join",      "back"]
    selected = 0
    clock   = pygame.time.Clock()
    background = load_background(screen)


    while True:
        if background:
            screen.blit(background, (0, 0))
        else:
            screen.blit(30, 30, 30)

        title_surf = FONT.render("Multijoueur en ligne - Choisissez une configuration", True, (255, 215, 0))
        title_rect = title_surf.get_rect(center=(screen.get_width() / 2, 100))
        screen.blit(title_surf, title_rect)

        mx, my = pygame.mouse.get_pos()
        for i, opt in enumerate(options):
            color = (255, 0, 0) if i == selected else (255, 255, 255)
            surf = FONT.render(opt, True, color)
            rect = surf.get_rect(center=(screen.get_width() // 2, 200 + i * 60))
            if rect.collidepoint(mx, my):
                selected = i
                pygame.draw.rect(screen, (255, 255, 255), rect.inflate(20, 10), 2)
            screen.blit(surf, rect)

        pygame.display.flip()

        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                pygame.quit()
                sys.exit()

            elif event.type == pygame.MOUSEBUTTONDOWN and event.button == 1:
                value = values[selected]
                if value == "join":
                    ip = ask_for_ip(screen)
                    if ip == "back":
                        break
                    else:
                        return ip
                else:
                    return value
            elif event.type == pygame.KEYDOWN:
                if event.key == pygame.K_UP:
                    selected = (selected - 1) % len(options)
                elif event.key == pygame.K_DOWN:
                    selected = (selected + 1) % len(options)
                elif event.key == pygame.K_RETURN:
                    value = values[selected]
                    if value == "join":
                        ip = ask_for_ip(screen)
                        if ip == "back":
                            break
                        else:
                            return ip
                    else:
                        return value

        clock.tick(30)
