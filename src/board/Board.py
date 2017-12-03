# Currently there are two board implementations in development branches.  These
# need to be merged. Until then, master should contain an api that will likely
# be implmented in the future. """


class Board():
    """ This will act as the backend for most of the engine. After it is
    completed, it should be very stable and bug-free and well documented. """

    def __init__(self):
        """ TODO Constructor """
        pass

    def __str__(self):
        """ TODO Ascii representation of the board. """
        return ""

    def read_from_fen(self, fen_string):
        """ TODO Process a position from an fen string """
        pass

    def get_all_legal_moves(self):
        """ TODO Return an array of strings representing all legal moves from
        the current board position """
        pass

    def make_move(self, move):
        """ TODO Make a move on the board. Throw an exception if the move is
        not valid. """
        pass

    def get_fen(self):
        """ TODO Return an fen string of the current board position. """
        return "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
