import pygame
from config import TILE_SIZE

def handle_events(board, renderer):
    for event in pygame.event.get():
        if event.type == pygame.QUIT:
            return False

        if event.type == pygame.MOUSEBUTTONDOWN:
            mx, my = event.pos
            x = (mx - renderer.offset_x) // TILE_SIZE
            y = (my - renderer.offset_y) // TILE_SIZE

            if not (0 <= x < 10 and 0 <= y < 8):
                return True

            clicked_piece = board.get_piece_at((x, y))

            if event.button == 1:
                if board.selected:
                    if (x, y) == board.selected.position:
                        board.selected = None
                    elif board.is_valid_move(board.selected, (x, y)):
                        board.move_piece(board.selected, (x, y))
                        board.selected = None
                        board.apply_laser()
                        board.current_player = board.opponent(board.current_player)
                elif clicked_piece and clicked_piece.owner == board.current_player:
                    board.selected = clicked_piece

            elif event.button == 3:
                if clicked_piece and clicked_piece.owner == board.current_player:
                    clicked_piece.rotate(clockwise=True)
                    board.apply_laser()
                    board.current_player = board.opponent(board.current_player)

    return True
