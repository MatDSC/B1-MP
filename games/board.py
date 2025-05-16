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

    def get_piece_at(self, pos):
        x, y = pos
        if 0 <= x < 10 and 0 <= y < 8:
            return self.grid[y][x]
        return None

    def is_valid_move(self, piece, target):
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
        if isinstance(piece, Scarab) and isinstance(target_piece, (Anubis, Pyramid)):
            return True
        return target_piece is None

    def move_piece(self, piece, target):
        x0, y0 = piece.position
        tx, ty = target
        target_piece = self.get_piece_at(target)
        if isinstance(piece, Scarab) and isinstance(target_piece, (Anubis, Pyramid)):
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

        # Applique les effets
        if hit_piece:
            if isinstance(hit_piece, Pharaoh):
                self.winner = self.opponent(hit_piece.owner)
                print(f"Le joueur {self.winner} a gagné !")
            elif isinstance(hit_piece, (Pyramid, Anubis)):
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
            # déplacement
            if self.is_valid_move(self.selected, pos):
                self.move_piece(self.selected, pos)
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
        #Pièce Rouge
        self.add_piece(Sphinx((0,0), 'S', 'RED'))
        self.add_piece(Pharaoh((5, 0), 'S', 'RED'))
        self.add_piece(Scarab((4, 3), 'N', 'RED'))
        self.add_piece(Scarab((5, 3), 'N', 'RED'))
        self.add_piece(Anubis((4, 0), 'S', 'RED'))
        self.add_piece(Anubis((6, 0), 'S', 'RED'))
        self.add_piece(Pyramid((2, 1), 'E', 'RED'))
        self.add_piece(Pyramid((7, 0), 'E', 'RED'))
        self.add_piece(Pyramid((0, 3), 'E', 'RED'))
        self.add_piece(Pyramid((0, 4), 'E', 'RED'))
        self.add_piece(Pyramid((7, 3), 'E', 'RED'))
        self.add_piece(Pyramid((7, 4), 'E', 'RED'))
        self.add_piece(Pyramid((6, 5), 'E', 'RED'))
        #Piece grise
        self.add_piece(Sphinx((9, 7), 'W', 'GRAY'))
        self.add_piece(Pharaoh((4, 7), 'N', 'GRAY'))
        self.add_piece(Scarab((4, 4), 'S', 'GRAY'))
        self.add_piece(Scarab((5, 4), 'S', 'GRAY'))
        self.add_piece(Anubis((3, 7), 'N', 'GRAY'))
        self.add_piece(Anubis((5, 7), 'N', 'GRAY'))
        self.add_piece(Pyramid((3, 2), 'E', 'GRAY'))
        self.add_piece(Pyramid((2, 3), 'E', 'GRAY'))
        self.add_piece(Pyramid((2, 4), 'E', 'GRAY'))
        self.add_piece(Pyramid((9, 3), 'E', 'GRAY'))
        self.add_piece(Pyramid((9, 4), 'E', 'GRAY'))
        self.add_piece(Pyramid((7, 6), 'E', 'GRAY'))
        self.add_piece(Pyramid((2, 7), 'E', 'GRAY'))

    def place_imhotep_setup(self):
        self.clear()
        #Pièce Rouge
        self.add_piece(Sphinx((0,0), 'S', 'RED'))
        self.add_piece(Pharaoh((5, 0), 'S', 'RED'))
        self.add_piece(Scarab((7, 0), 'N', 'RED'))
        self.add_piece(Scarab((5, 3), 'N', 'RED'))
        self.add_piece(Anubis((4, 0), 'S', 'RED'))
        self.add_piece(Anubis((6, 0), 'S', 'RED'))
        self.add_piece(Pyramid((5, 4), 'E', 'RED'))
        self.add_piece(Pyramid((6, 5), 'E', 'RED'))
        self.add_piece(Pyramid((0, 3), 'E', 'RED'))
        self.add_piece(Pyramid((0, 4), 'E', 'RED'))
        self.add_piece(Pyramid((8, 3), 'E', 'RED'))
        self.add_piece(Pyramid((8, 4), 'E', 'RED'))
        self.add_piece(Pyramid((6, 2), 'E', 'RED'))
        #Piece grise
        self.add_piece(Sphinx((9, 7), 'W', 'GRAY'))
        self.add_piece(Pharaoh((4, 7), 'N', 'GRAY'))
        self.add_piece(Scarab((4, 4), 'S', 'GRAY'))
        self.add_piece(Scarab((2, 7), 'S', 'GRAY'))
        self.add_piece(Anubis((3, 7), 'N', 'GRAY'))
        self.add_piece(Anubis((5, 7), 'N', 'GRAY'))
        self.add_piece(Pyramid((3, 2), 'E', 'GRAY'))
        self.add_piece(Pyramid((1, 3), 'E', 'GRAY'))
        self.add_piece(Pyramid((1, 4), 'E', 'GRAY'))
        self.add_piece(Pyramid((9, 3), 'E', 'GRAY'))
        self.add_piece(Pyramid((9, 4), 'E', 'GRAY'))
        self.add_piece(Pyramid((4, 3), 'E', 'GRAY'))
        self.add_piece(Pyramid((3, 5), 'E', 'GRAY'))

    def place_dynasty_setup(self):
        self.clear()
        #Pièce Rouge
        self.add_piece(Sphinx((0,0), 'W', 'RED'))
        self.add_piece(Pharaoh((5, 1), 'S', 'RED'))
        self.add_piece(Scarab((6, 2), 'N', 'RED'))
        self.add_piece(Scarab((5, 5), 'N', 'RED'))
        self.add_piece(Anubis((5, 2), 'S', 'RED'))
        self.add_piece(Anubis((5, 0), 'S', 'RED'))
        self.add_piece(Pyramid((5, 4), 'E', 'RED'))
        self.add_piece(Pyramid((6, 0), 'E', 'RED'))
        self.add_piece(Pyramid((0, 2), 'E', 'RED'))
        self.add_piece(Pyramid((0, 3), 'E', 'RED'))
        self.add_piece(Pyramid((4, 0), 'E', 'RED'))
        self.add_piece(Pyramid((3, 4), 'E', 'RED'))
        self.add_piece(Pyramid((4, 2), 'E', 'RED'))
        #Piece grise
        self.add_piece(Sphinx((9, 7), 'W', 'GRAY'))
        self.add_piece(Pharaoh((4, 6), 'N', 'GRAY'))
        self.add_piece(Scarab((3, 5), 'S', 'GRAY'))
        self.add_piece(Scarab((7, 4), 'S', 'GRAY'))
        self.add_piece(Anubis((4, 7), 'N', 'GRAY'))
        self.add_piece(Anubis((4, 5), 'N', 'GRAY'))
        self.add_piece(Pyramid((4, 3), 'E', 'GRAY'))
        self.add_piece(Pyramid((6, 3), 'E', 'GRAY'))
        self.add_piece(Pyramid((5, 5), 'E', 'GRAY'))
        self.add_piece(Pyramid((9, 4), 'E', 'GRAY'))
        self.add_piece(Pyramid((9, 5), 'E', 'GRAY'))
        self.add_piece(Pyramid((3, 7), 'E', 'GRAY'))
        self.add_piece(Pyramid((5, 7), 'E', 'GRAY'))

    def place_test_pieces(self):
        # Configuration de test
        self.pieces.clear()
        self.add_piece(Sphinx((0, 0), 'E', 'RED'))
        self.add_piece(Sphinx((9, 7), 'W', 'GRAY'))
        self.add_piece(Pharaoh((5, 0), 'S', 'GRAY'))
        self.add_piece(Pharaoh((4, 7), 'N', 'RED'))


