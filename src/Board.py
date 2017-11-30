""" Board representation """


class Board():

    """ TODO Use python logging for debugging out """
    debug = False

    __board_size = 12

    """ Start position

    Capital is white, underscore is empty

    [R, N, B, K, Q, B, N, R,
     P, P, P, P, P, P, P, P,
     _, _, _, _, _, _, _, _,
     _, _, _, _, _, _, _, _,
     _, _, _, _, _, _, _, _,
     _, _, _, _, _, _, _, _,
     p, p, p, p, p, p, p, p,
     r, n, b, k, q, b, n, r]

     bottom left is index 0, bottom right is index 7, top 63

     blank is 0, pawn 1, knight 2, bishop 3, rook 4, queen 5, king 6. On the
     boundary board a 7 is a boundary square to prevent going off the edge.

     black is negative eg -1 black pawn
     """
    # __start_board = [+4, +2, +3, +5, +6, +3, +2, +4,
    #                  +1, +1, +1, +1, +1, +1, +1, +1,
    #                  +0, +0, +0, +0, +0, +0, +0, +0,
    #                  +0, +0, +0, +0, +0, +0, +0, +0,
    #                  +0, +0, +0, +0, +0, +0, +0, +0,
    #                  +0, +0, +0, +0, +0, +0, +0, +0,
    #                  -1, -1, -1, -1, -1, -1, -1, -1,
    #                  -4, -2, -3, -5, -6, -3, -2, -4]

    """ Board used for out of bounds detection. This has the added piece "7",
    which just means out of bounds. """

    """
    [X, X, X, X, X, X, X, X, X, X, X, X,
     X, X, X, X, X, X, X, X, X, X, X, X,
     X, X, R, N, B, K, Q, B, N, R, X, X,
     X, X, P, P, P, P, P, P, P, P, X, X,
     X, X, _, _, _, _, _, _, _, _, X, X,
     X, X, _, _, _, _, _, _, _, _, X, X,
     X, X, _, _, _, _, _, _, _, _, X, X,
     X, X, _, _, _, _, _, _, _, _, X, X,
     X, X, p, p, p, p, p, p, p, p, X, X,
     X, X, r, n, b, k, q, b, n, r, X, X,
     X, X, X, X, X, X, X, X, X, X, X, X,
     X, X, X, X, X, X, X, X, X, X, X, X]
    """

    __start_board = [+7, +7, +7, +7, +7, +7, +7, +7, +7, +7, +7, +7,
                     +7, +7, +7, +7, +7, +7, +7, +7, +7, +7, +7, +7,
                     +7, +7, +4, +2, +3, +5, +6, +3, +2, +4, +7, +7,
                     +7, +7, +1, +1, +1, +1, +1, +1, +1, +1, +7, +7,
                     +7, +7, +0, +0, +0, +0, +0, +0, +0, +0, +7, +7,
                     +7, +7, +0, +0, +0, +0, +0, +0, +0, +0, +7, +7,
                     +7, +7, +0, +0, +0, +0, +0, +0, +0, +0, +7, +7,
                     +7, +7, +0, +0, +0, +0, +0, +0, +0, +0, +7, +7,
                     +7, +7, -1, -1, -1, -1, -1, -1, -1, -1, +7, +7,
                     +7, +7, -4, -2, -3, -5, -6, -3, -2, -4, +7, +7,
                     +7, +7, +7, +7, +7, +7, +7, +7, +7, +7, +7, +7,
                     +7, +7, +7, +7, +7, +7, +7, +7, +7, +7, +7, +7]

    """ Used to convert from board to displayable pieces. Currently the X in the
    middle can be used to display the boundary board. """
    __piece_chars = [".", "P", "N", "B", "R", "Q", "K", "X", "k", "q", "r", "b",
                     "n", "p"]

    def __init__(self):
        """ The array to store the board """
        self.board = Board.__start_board

        """ Determine which  player's turn it is. White is True and Black is
        False. """
        self.cur_player_white = True

    def get_all_moves(self):
        """ Returns a list of all valid moves from the current position in
        algebraic notation """

        """ TODO Get moves """

        """ TODO Start with uci notation since it is easier to parse, then
        translate to algebriac """

        """ Theory of operation:

            I haven't planned this out fully yet, but here is what I have so far

            The plan will be to search for every possible move by looking for
            every piece the current player controls and then using a lookup
            table for non 'ray' pieces to look for all their potention moves.

            Steps

            1. Find the location of every piece the current player controls.

            2. TODO If the piece is a 'ray piece', i.e. Bishop, Rook, Queen

            3. Else if it is any other piece, use a lookup table to find all
            potential moves
        """

        """ Find the location of each piece """

        """ Stores the index of each of the current players pieces """
        cur_pieces_list = []
        for i in range(len(self.board) - 1):
            if self.cur_player_white and self.board[i] in [1, 2, 3, 4, 5, 6]:
                cur_pieces_list.append(i)

            elif not self.cur_player_white:
                if self.board[i] in [-1, -2, -3, -4, -5, -6]:
                    cur_pieces_list.append(i)

        for i in cur_pieces_list:

            candidate_moves = []

            """ Temporarily ignore rooks, bishops and queens """
            """ TODO Write code for "ray" pieces """
            if self.board[i] in [3, 4, 5, -3, -4, -5]:
                pass
            elif self.board[i] == 1:
                """ Currently white pawns are the only implemented piece """

                """ TODO Document offsets """
                pawn_move_offsets = [i + 11, i + 12, i + 13, i + 24]

                for j in range(len(pawn_move_offsets) - 1):

                    location = pawn_move_offsets[j]

                    """ The space is unnocupied """
                    if self.board[location] == 0:
                        candidate_moves.append[location]
                    else:
                        """ TODO Allow captures """
                        pass

                    if Board.debug:
                        print(location)
                        if self.board[location] == 7:
                            print("Pawn off of board. Starting location " + str(i))
                        elif self.board[location] == 0:
                            print("location empty")
                        else:
                            print("location OCCUPIED")

            else:
                pass

    def print_board(self):
        """ Print in reverse order, (black in back) """
        """ TODO use string builder """

        line = ''

        """ Used to split the line after each 8th piece """
        """ TODO Board prints with white in back, which isn't wrong but white
        looks better in front """
        file_count = 0
        for i in self.board:
            file_count += 1

            """ Add piece and space to string """
            line += Board.__piece_chars[i] + " "

            if file_count == (Board.__board_size):
                line += '\n'
                file_count = 0

        print(line)
