from piece import *

class Board:
    def __init__(self):
        self.grid = [[None for _ in range(10)] for _ in range(8)]
        self.pieces = []
        self.selected = None
        self.current_player = 'RED'

    def place_test_pieces(self):
        s1 = Sphinx((0, 0), 'E', 'RED')
        s2 = Sphinx((9, 7), 'W', 'GRAY')
        self.add_piece(s1)
        self.add_piece(s2)

    def add_piece(self, piece):
        x, y = piece.position
        self.grid[y][x] = piece
        self.pieces.append(piece)

    def move_piece(self, piece, target):
        x, y = piece.position
        tx, ty = target
        if self.grid[ty][tx] is None:
            self.grid[y][x] = None
            self.grid[ty][tx] = piece
            piece.position = (tx, ty)

    def get_piece_at(self, pos):
        x, y = pos
        return self.grid[y][x]

    def toggle_select(self, pos):
        piece = self.get_piece_at(pos)
        if piece and piece.owner == self.current_player:
            self.selected = piece
        elif self.selected:
            self.move_piece(self.selected, pos)
            self.selected = None

    def apply_laser(self):
        from laser import trace_laser
        sphinx = next(p for p in self.pieces if isinstance(p, Sphinx) and p.owner == self.current_player)
        path = trace_laser(self, sphinx.position, sphinx.orientation)
        return path