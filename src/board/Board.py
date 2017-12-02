# Board representation

import re


class Board():
    """ Uses a 12 by 12 array to store the board """

    # Start position

    # Capital is white, underscore is empty

    # bottom left of board, a1 in algebraic notation, is index 0, bottom right
    # is index 7, top right is 63.

    # empty location is 0, pawn 1, knight 2, bishop 3, rook 4, queen 5, king 6.
    # On the boundary board a 7 is a boundary square to prevent going off the
    # edge.

    # black is negative eg -1 is a black pawn

    # Visualization of the board. This is backwards because of the way the
    # array is arranged.
    #
    # [X, X, X, X, X, X, X, X, X, X, X, X,
    #  X, X, X, X, X, X, X, X, X, X, X, X,
    #  X, X, R, N, B, K, Q, B, N, R, X, X,
    #  X, X, P, P, P, P, P, P, P, P, X, X,
    #  X, X, _, _, _, _, _, _, _, _, X, X,
    #  X, X, _, _, _, _, _, _, _, _, X, X,
    #  X, X, _, _, _, _, _, _, _, _, X, X,
    #  X, X, _, _, _, _, _, _, _, _, X, X,
    #  X, X, p, p, p, p, p, p, p, p, X, X,
    #  X, X, r, n, b, k, q, b, n, r, X, X,
    #  X, X, X, X, X, X, X, X, X, X, X, X,
    #  X, X, X, X, X, X, X, X, X, X, X, X]

    # fen: rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1
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

    __board_size = 12

    # Used to convert from board to displayable pieces. Currently the X in the
    # middle can be used to display the boundary board. Note that the board
    # uses negative numbers for black. This works well with python which allows
    # negative indeces.

    __piece_chars = [".", "P", "N", "B", "R", "Q", "K", "X", "k", "q", "r",
                     "b", "n", "p"]

    __pieces_lookup = ["empty", "white_pawn", "white_knight", "white_bishop",
                       "white_rook", "white_queen", "white_king", "black_king",
                       "black_queen", "black_rook", "black_bishop",
                       "black_knight", "black_pawn"]

    def __init__(self, fen=None):
        """ Sets up initial bored configuration """

        # The array to store the board
        self.board = Board.__start_board

        if fen is not None:
            self.read_position(fen)

        self.castle_available = [True, True, True, True]
        self.en_passant_target = ""

        # Determine which  player's turn it is. White is True and Black is
        # False.
        self.cur_player_white = True

    def __str__(self):
        """ Print in reverse order, (black in back) """

        output_string = ''

        # Used to split the line after each 8th piece
        file_count = 0
        for i in range(9, 1, -1):
            for j in range(2, 10):
                file_count += 1

                # Use lookup table to translate pieces to strings. Then add
                # the piece and a space to the output string.

                output_string += Board.__piece_chars[
                    self.board[i * 12 + j]] + " "

                if file_count == 8:
                    output_string += "\n"
                    file_count = 0

        return output_string

    def read_position(self, fen):
        """
        1. Process Board position:
            Each row is seperated by a /, the finaly (8th) row is ended with a
            space.

            For each of the 8 rows:
                Process each letter individually
                4 = 4 empty spaces

        sample:

        Starting position:
        rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1

        2: rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1
        """

        num_spaces = fen.count(" ")
        num_slashes = fen.count("/")

        # Simple pattern to match all the valid characters until the first
        # space in an fen string
        fen_board = re.search('^([rkqrbnpKQRBNP/12345678])+', fen).group(0)

        # Create a list containing each rank
        prev_index = -1
        cur_index = 0
        ranks = []
        for i in range(7):
            cur_index = fen_board.index('/', prev_index + 1)
            ranks.append(fen_board[prev_index + 1:cur_index])
            prev_index = cur_index
        ranks.append(fen_board[prev_index + 1:len(fen_board)])

        for i in range(len(ranks)):
            cur_rank = ranks[i]

            # Location on the board to start placing pieces
            starting_indices = [110, 98, 86, 74, 62, 50, 38, 26]

            # Convert empty squares to dots.
            # for each letter l:
            #     if l in lookup_table:
            #        location(l).replace_with(dot_lookup[l - 1])

            # Solved through trial and error. I don't actually know how this
            # works
            # TODO Document and/or rewrite
            digit_lookup = ['1', '2', '3', '4', '5', '6', '7', '8']
            num_dots_lookup = ['.', '..', '...', '....', '.....', '......',
                               '.......', '........']
            tmp = ranks[i]
            j = 0
            while j < len(tmp):
                num_empty_str = tmp[j]
                if num_empty_str in digit_lookup:
                    num_empty = digit_lookup.index(num_empty_str)

                    tmp = tmp[:j] + num_dots_lookup[num_empty] + \
                        tmp[j + 1:len(tmp)]

                    j = 0
                j += 1

            for k in range(8):
                start_index = starting_indices[i]
                piece = Board.__piece_chars.index(tmp[k])
                # Use negative values for black. The "X" is the last, non-black
                # piece in the array.
                if piece > Board.__piece_chars.index("X"):
                    piece -= 14
                self.board[start_index + k] = piece

        return ranks

    def get_fen(self):
        # TODO Return an fen representation of the current board
        pass

    def get_all_moves(self):
        """ Returns a list of all valid moves from the current position in
        algebraic notation """

        # Theory of operation:
        #
        # The plan will be to search for every possible move by looking for
        # every piece the current player controls and then using a lookup table
        # for non 'ray' pieces to look for all their potention moves.
        #
        # Steps
        #
        # 1. Find the location of every piece the current player controls.
        #
        # 2. TODO If the piece is a 'ray piece', i.e. Bishop, Rook, Queen
        #
        # 3. Else if it is any other piece, use a lookup table to find all
        # potential moves
        #
        # 3.1 Offset Arrays: For many of the moves I used array containing
        # position offsets. These work by storing the relative location in the
        # array for all of the possible moves of the following pieces: pawns,
        # knights and kings. Then the program seperately checks the validity of
        # each of moving to each of these locations.
        #
        # For example: TODO Knight example since it is cleaner than pawn code

        # Stores the index of each of the current players pieces.
        cur_pieces_list = []

        # List of legal moves.
        moves = []

        # Find the location of each of the current players pieces.
        for i in range(len(self.board) - 1):
            if self.cur_player_white and self.board[i] in [1, 2, 3, 4, 5, 6]:
                cur_pieces_list.append(i)

            elif not self.cur_player_white:
                if self.board[i] in [-1, -2, -3, -4, -5, -6]:
                    cur_pieces_list.append(i)

        # Check all possible moves for each piece
        for i in cur_pieces_list:
            piece = self.__pieces_lookup[self.board[i]]

            candidate_moves = []

            enemy_pieces_lookup = []
            if self.cur_player_white:
                enemy_pieces_lookup = [-1, -2, -3, -4, -5, -6]
            else:
                enemy_pieces_lookup = [1, 2, 3, 4, 5, 6]

            # Temporarily ignore rooks, bishops and queens
            # TODO Write code for "ray" pieces
            if piece in [3, 4, 5, -3, -4, -5]:
                pass

            # Pawn movement
            elif piece == "white_pawn" or piece == "black_pawn":
                # Currently pawns are the only implemented piece
                candidate_moves += self.get_legal_pawn_moves(
                    i, enemy_pieces_lookup)

            # Knight movement
            elif piece == "white_knight" or piece == "black_knight":
                candidate_moves += self.get_knight_moves(i,
                                                         enemy_pieces_lookup)

            elif piece == "white_king" or piece == "black_king":
                candidate_moves += self.get_king_moves(i, enemy_pieces_lookup)

            # Convert moves to uci
            for j in range(len(candidate_moves)):
                moves.append(
                    Board.get_algebraic_from_index(i) +
                    Board.get_algebraic_from_index(
                        candidate_moves[j]))

        # TODO Check if king left in check

        return moves

    def get_legal_pawn_moves(self, i, enemy_pieces_lookup):
        candidate_moves = []

        # Pawn moves are surprisingly complicated compared to the rest of the
        # pieces.
        #
        # 1. The direction a pawn can move depends on it's color
        #
        # 2. A pawn can move twice only on it's first move
        #
        # 3. A pawn can capture en passant
        #
        # 4. A pawn captures in a diffent way than it moves

        # Pawn offset
        #
        # There are four potential moves for a pawn:
        #
        # 1. 1 forward (unless blocked
        # or pinned),
        #
        # 2. 2 forward (if not blocked or pinned, and if starting on
        # initial square)
        #
        # 3. capture on adjacent diagonal squares (if not pinned and an
        # oppenents piece is on the square, or if en passant is allowed).

        if self.cur_player_white:
            pawn_move_offset = i + 12
            pawn_captures_offsets = [i + 11, i + 13]
            pawn_move_double_offset = i + 24
        else:
            pawn_move_offset = i - 12
            pawn_captures_offsets = [i - 11, i - 13]
            pawn_move_double_offset = i - 24

        # Single move

        location = pawn_move_offset

        # The space is unnocupied
        if self.board[location] == 0:
            candidate_moves.append(location)

        # Captures
        for j in range(len(pawn_captures_offsets)):
            location = pawn_captures_offsets[j]
            if self.board[location] in enemy_pieces_lookup:
                candidate_moves.append(location)
            # TODO Check for en passant here

        # Move double
        pawn_double_lookup = [[38, 39, 40, 41, 42, 43, 44, 45],
                              [98, 99, 100, 101, 102, 103, 104, 105]]

        if ((self.cur_player_white and i in pawn_double_lookup[0]) or
                (self.cur_player_white and i not in pawn_double_lookup[1])):
            location = pawn_move_double_offset

            # TODO Rewrite if condition for readability
            if self.board[location] == 0:
                if ((self.cur_player_white and (self.board[location - 12]
                                                == 0))
                    or (not self.cur_player_white
                        and self.board[location + 12] == 0)):
                    candidate_moves.append(location)

        return candidate_moves

    def get_knight_moves(self, i, enemy_pieces_lookup):
        candidate_moves = []

        # Knight offsets
        #
        # The knight has less complicated movement than the pawn. Every offset
        # needs the exact same checks done for validity.

        knight_offsets = [i - (12 * 2) - 1, i - (12 * 2) + 1, i - 12 - 1, i -
                          12 + 1, i + 12 - 1, i + 12 + 1, i + 24 - 1, i + 24 +
                          1]

        valid_locations = enemy_pieces_lookup + [0]

        # Moves and captures
        for location in knight_offsets:
            if self.board[location] in valid_locations:
                candidate_moves.append(location)

        return candidate_moves

    def get_king_moves(self, i, enemy_pieces_lookup):
        candidate_moves = []

        # King Movement
        #
        # The king is simple, like the knight. The only complicated case is
        # castling.
        #
        # TODO Castling

        king_offsets = [i - 13, i - 12, i - 11, i - 1, i + 1, i + 11, i + 12, i
                        + 13]
        valid_locations = enemy_pieces_lookup + [0]

        # Moves and captures
        for location in king_offsets:
            if self.board[location] in valid_locations:
                candidate_moves.append(location)

        return candidate_moves

    def get_algebraic_from_index(index):
        # Convert from a board location array index to algebraic board location
        # i = 26 -> a1, i = 38 -> a2

        algebraic = ""

        # a: 26, 38, 50, 62, 74, 86, 98, 110

        # From location
        if index in [26, 38, 50, 62, 74, 86, 98, 110]:
            algebraic += "a" + str(((index - 2) // 12) - 1)

        elif index in [27, 39, 51, 63, 75, 87, 99, 111]:
            algebraic = "b" + str(((index - 3) // 12) - 1)

        elif index in [28, 40, 52, 64, 76, 88, 100, 112]:
            algebraic = "c" + str(((index - 4) // 12) - 1)

        elif index in [29, 41, 53, 65, 77, 89, 101, 113]:
            algebraic = "d" + str(((index - 5) // 12) - 1)

        elif index in [30, 42, 54, 66, 78, 90, 102, 114]:
            algebraic = "e" + str(((index - 6) // 12) - 1)

        elif index in [31, 43, 55, 67, 79, 91, 103, 115]:
            algebraic = "f" + str(((index - 7) // 12) - 1)

        elif index in [32, 44, 56, 68, 80, 90, 104, 116]:
            algebraic = "g" + str(((index - 8) // 12) - 1)

        elif index in [33, 45, 57, 69, 81, 93, 105, 117]:
            algebraic = "h" + str(((index - 9) // 12) - 1)

        return algebraic

    def get_board_layout():
        """ Returns a string with a visual representation of how the board is
        mapped to an array. The Outer section of the board, the part used for
        out of bounds detection, is not shown. """

        output_string = ""

        for i in range(9, 1, -1):
            for j in range(9, 1, -1):
                output_string += str((i * 12) + j) + "\t"
            output_string += "\n"

        return output_string
