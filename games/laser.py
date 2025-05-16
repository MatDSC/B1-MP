from games.piece import Sphinx, Pyramid, Scarab, Anubis, Pharaoh

def trace_laser(board, start_pos, direction):
    path = []
    hit_piece = None

    dir_map = {'N': (0, -1), 'E': (1, 0), 'S': (0, 1), 'W': (-1, 0)}
    reflect_map = {
        ('N', 'W'): 'E', ('E', 'S'): 'N',
        ('S', 'E'): 'W', ('W', 'N'): 'S',
        ('E', 'W'): 'S', ('N', 'S'): 'E',
        ('S', 'N'): 'W', ('W', 'E'): 'N',

    }

    x, y = start_pos
    dx, dy = dir_map[direction]

    x += dx
    y += dy

    while 0 <= x < 10 and 0 <= y < 8:
        path.append((x, y))
        piece = board.get_piece_at((x, y))

        if piece:
            if isinstance(piece, Sphinx):
                break

            elif isinstance(piece, Scarab):
                direction = {'N': 'E', 'E': 'S', 'S': 'W', 'W': 'N'}[direction]
                dx, dy = dir_map[direction]
                x += dx
                y += dy
                continue

            elif isinstance(piece, Pyramid):
                new_dir = reflect_map.get((direction, piece.orientation))
                if new_dir:
                    direction = new_dir
                    dx, dy = dir_map[direction]
                    x += dx
                    y += dy
                    continue
                else:
                    hit_piece = piece
                    break

            elif isinstance(piece, Anubis):
                if direction == piece.orientation:
                    break
                else:
                    hit_piece = piece
                    break

            elif isinstance(piece, Pharaoh):
                hit_piece = piece
                break

            else:
                break

        else:
            x += dx
            y += dy



    return path, hit_piece

