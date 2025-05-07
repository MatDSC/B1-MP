from piece import *
def trace_laser(board, start_pos, direction):
    path = []
    dir_map = {'N': (0, -1), 'S': (0, 1), 'E': (1, 0), 'W': (-1, 0)}
    x, y = start_pos
    dx, dy = dir_map[direction]
    while 0 <= x < 10 and 0 <= y < 8:
        path.append((x, y))
        piece = board.get_piece_at((x, y))
        if piece and not isinstance(piece, Sphinx):
            break
        x += dx
        y += dy
    return path