from games.piece import *

class Board:
    def __init__(self):
        # Plateau 8x10
        self.grid = [[None for _ in range(10)] for _ in range(8)]
        self.pieces = []
        self.selected = None
        self.current_player = 'RED'
        self.restricted_zones = {
            'RED': [(0, y) for y in range(8)] + [(8, 0), (8, 7)],
            'GRAY': [(9, y) for y in range(8)] + [(1, 0), (1, 7)]
        }
        self.winner = None
        self.last_laser_path = []
        self.last_laser_hit = None
        self.configurations = [
            ("Classique", lambda b: b.place_classic_setup()),
            ("Imhotep", lambda b: b.place_imhotep_setup()),
            ("Dynasty", lambda b: b.place_dynasty_setup()),
        ]

    def get_piece_at(self, pos):
        x, y = pos
        if 0 <= x < 10 and 0 <= y < 8:
            return self.grid[y][x]
        return None

    def is_valid_move(self, piece, target):
        if isinstance(piece, Sphinx):
            return False
        tx, ty = target
        if not (0 <= tx < 10 and 0 <= ty < 8):
            return False
        restricted = self.restricted_zones.get(self.opponent(piece.owner), [])
        if target in restricted:
            return False
        dx = abs(tx - piece.position[0])
        dy = abs(ty - piece.position[1])
        if dx > 1 or dy > 1:
            return False
        target_piece = self.get_piece_at(target)
        if isinstance(piece, Scarabee) and isinstance(target_piece, (Anubis, Pyramide)):
            return True
        return target_piece is None

    def move_piece(self, piece, target):
        x0, y0 = piece.position
        tx, ty = target
        target_piece = self.get_piece_at(target)
        if isinstance(piece, Scarabee) and isinstance(target_piece, (Anubis, Pyramide)):
            self.grid[y0][x0], self.grid[ty][tx] = target_piece, piece
            piece.position, target_piece.position = (tx, ty), (x0, y0)
        else:
            self.grid[y0][x0] = None
            self.grid[ty][tx] = piece
            piece.position = (tx, ty)

    def apply_laser(self):
        from games.laser import trace_laser
        sphinx = next((p for p in self.pieces if isinstance(p, Sphinx) and p.owner == self.current_player), None)
        if not sphinx:
            self.last_laser_path = []
            self.last_laser_hit = None
            return [], None

        path, hit_piece = trace_laser(self, sphinx.position, sphinx.orientation)
        self.last_laser_path = path
        self.last_laser_hit = hit_piece

        if hit_piece:
            if isinstance(hit_piece, Pharaon):
                self.winner = self.opponent(hit_piece.owner)
                print(f"Le joueur {self.winner} a gagné !")
            elif isinstance(hit_piece, (Pyramide, Anubis)):
                xh, yh = hit_piece.position
                self.grid[yh][xh] = None
                self.pieces.remove(hit_piece)

        return path, hit_piece


    def opponent(self, player):
        return 'GRAY' if player == 'RED' else 'RED'

    def toggle_select(self, pos):
        piece = self.get_piece_at(pos)
        if piece and piece.owner == self.current_player:
            self.selected = piece
        elif self.selected:

            if self.is_valid_move(self.selected, pos):
                self.move_piece(self.selected, pos)
            self.selected = None

    def end_turn(self):
        self.current_player = self.opponent(self.current_player)
        self.selected = None

    def add_piece(self, piece):
        x, y = piece.position
        self.grid[y][x] = piece
        self.pieces.append(piece)

    def clear(self):
        self.grid = [[None for _ in range(10)] for _ in range(8)]
        self.pieces = []

    def place_classic_setup(self):
        self.clear()
        #Red Piece
        self.add_piece(Sphinx((0,0), 'N', 'RED'))
        self.add_piece(Pharaon((5, 0), 'N', 'RED'))
        self.add_piece(Scarabee((4, 3), 'N', 'RED'))
        self.add_piece(Scarabee((5, 3), 'N', 'RED'))
        self.add_piece(Anubis((4, 0), 'N', 'RED'))
        self.add_piece(Anubis((6, 0), 'N', 'RED'))
        self.add_piece(Pyramide((2, 1), 'N', 'RED'))
        self.add_piece(Pyramide((7, 0), 'N', 'RED'))
        self.add_piece(Pyramide((0, 3), 'N', 'RED'))
        self.add_piece(Pyramide((0, 4), 'N', 'RED'))
        self.add_piece(Pyramide((7, 3), 'N', 'RED'))
        self.add_piece(Pyramide((7, 4), 'N', 'RED'))
        self.add_piece(Pyramide((6, 5), 'N', 'RED'))
        #Gray Piece
        self.add_piece(Sphinx((9, 7), 'N', 'GRAY'))
        self.add_piece(Pharaon((4, 7), 'N', 'GRAY'))
        self.add_piece(Scarabee((4, 4), 'N', 'GRAY'))
        self.add_piece(Scarabee((5, 4), 'N', 'GRAY'))
        self.add_piece(Anubis((3, 7), 'N', 'GRAY'))
        self.add_piece(Anubis((5, 7), 'N', 'GRAY'))
        self.add_piece(Pyramide((3, 2), 'N', 'GRAY'))
        self.add_piece(Pyramide((2, 3), 'N', 'GRAY'))
        self.add_piece(Pyramide((2, 4), 'N', 'GRAY'))
        self.add_piece(Pyramide((9, 3), 'N', 'GRAY'))
        self.add_piece(Pyramide((9, 4), 'N', 'GRAY'))
        self.add_piece(Pyramide((7, 6), 'N', 'GRAY'))
        self.add_piece(Pyramide((2, 7), 'N', 'GRAY'))

    def place_imhotep_setup(self):
        self.clear()
        #Red Piece
        self.add_piece(Sphinx((0,0), 'N', 'RED'))
        self.add_piece(Pharaon((5, 0), 'N', 'RED'))
        self.add_piece(Scarabee((7, 0), 'N', 'RED'))
        self.add_piece(Scarabee((5, 3), 'N', 'RED'))
        self.add_piece(Anubis((4, 0), 'N', 'RED'))
        self.add_piece(Anubis((6, 0), 'N', 'RED'))
        self.add_piece(Pyramide((5, 4), 'N', 'RED'))
        self.add_piece(Pyramide((6, 5), 'N', 'RED'))
        self.add_piece(Pyramide((0, 3), 'N', 'RED'))
        self.add_piece(Pyramide((0, 4), 'N', 'RED'))
        self.add_piece(Pyramide((8, 3), 'N', 'RED'))
        self.add_piece(Pyramide((8, 4), 'N', 'RED'))
        self.add_piece(Pyramide((6, 2), 'N', 'RED'))
        #Gray Piece
        self.add_piece(Sphinx((9, 7), 'N', 'GRAY'))
        self.add_piece(Pharaon((4, 7), 'N', 'GRAY'))
        self.add_piece(Scarabee((4, 4), 'N', 'GRAY'))
        self.add_piece(Scarabee((2, 7), 'N', 'GRAY'))
        self.add_piece(Anubis((3, 7), 'N', 'GRAY'))
        self.add_piece(Anubis((5, 7), 'N', 'GRAY'))
        self.add_piece(Pyramide((3, 2), 'N', 'GRAY'))
        self.add_piece(Pyramide((1, 3), 'N', 'GRAY'))
        self.add_piece(Pyramide((1, 4), 'N', 'GRAY'))
        self.add_piece(Pyramide((9, 3), 'N', 'GRAY'))
        self.add_piece(Pyramide((9, 4), 'N', 'GRAY'))
        self.add_piece(Pyramide((4, 3), 'N', 'GRAY'))
        self.add_piece(Pyramide((3, 5), 'N', 'GRAY'))

    def place_dynasty_setup(self):
        self.clear()
        #Red Piece
        self.add_piece(Sphinx((0,0), 'N', 'RED'))
        self.add_piece(Pharaon((5, 1), 'N', 'RED'))
        self.add_piece(Scarabee((6, 2), 'N', 'RED'))
        self.add_piece(Scarabee((5, 5), 'N', 'RED'))
        self.add_piece(Anubis((5, 2), 'N', 'RED'))
        self.add_piece(Anubis((5, 0), 'N', 'RED'))
        self.add_piece(Pyramide((5, 4), 'N', 'RED'))
        self.add_piece(Pyramide((6, 0), 'N', 'RED'))
        self.add_piece(Pyramide((0, 2), 'N', 'RED'))
        self.add_piece(Pyramide((0, 3), 'N', 'RED'))
        self.add_piece(Pyramide((4, 0), 'N', 'RED'))
        self.add_piece(Pyramide((3, 4), 'N', 'RED'))
        self.add_piece(Pyramide((4, 2), 'N', 'RED'))
        #Gray Piece
        self.add_piece(Sphinx((9, 7), 'N', 'GRAY'))
        self.add_piece(Pharaon((4, 6), 'N', 'GRAY'))
        self.add_piece(Scarabee((3, 5), 'N', 'GRAY'))
        self.add_piece(Scarabee((7, 4), 'N', 'GRAY'))
        self.add_piece(Anubis((4, 7), 'N', 'GRAY'))
        self.add_piece(Anubis((4, 5), 'N', 'GRAY'))
        self.add_piece(Pyramide((4, 3), 'N', 'GRAY'))
        self.add_piece(Pyramide((6, 3), 'N', 'GRAY'))
        self.add_piece(Pyramide((5, 5), 'N', 'GRAY'))
        self.add_piece(Pyramide((9, 4), 'N', 'GRAY'))
        self.add_piece(Pyramide((9, 5), 'N', 'GRAY'))
        self.add_piece(Pyramide((3, 7), 'N', 'GRAY'))
        self.add_piece(Pyramide((5, 7), 'N', 'GRAY'))




