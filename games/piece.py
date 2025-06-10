class Piece:
    def __init__(self, position, orientation, owner):
        self.position = position
        self.orientation = orientation
        self.owner = owner

    def rotate(self, clockwise=True):
        orientations = ['N', 'E', 'S', 'W']
        idx = orientations.index(self.orientation)
        self.orientation = orientations[(idx + (1 if clockwise else -1)) % 4]

class Pharaon(Piece): pass
class Sphinx(Piece): pass
class Scarabee(Piece): pass
class Pyramide(Piece): pass
class Anubis(Piece): pass
