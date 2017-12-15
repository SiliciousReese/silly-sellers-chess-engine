# Board representation. Backend for chess engine.

# Regular expression. Currently used for parsing fen string.
import re

# Python logging.
import logging


class Board():
    """ A sample python implementation of a chess board. Typically c plus plus
    is used for speed, and this may be ported to c plus plus in the future. """

    # TODO Implement logging with built-in python logging module.

    # TODO Hide some helper methods from public api.

    # Start position
    #
    # Capital is white, underscore is empty
    #
    # bottom left of board, a1 in algebraic notation, is index 0, bottom right
    # is index 7, top right is 63.

    # Here is a visualization of the board. This is backwards, black is in
    # front but king is on the correct file, because of the way the array is
    # arranged.

    # [X, X, X, X, X, X, X, X, X, X, X, X,
    #  X, X, X, X, X, X, X, X, X, X, X, X,
    #  X, X, R, N, B, Q, K, B, N, R, X, X,
    #  X, X, P, P, P, P, P, P, P, P, X, X,
    #  X, X, _, _, _, _, _, _, _, _, X, X,
    #  X, X, _, _, _, _, _, _, _, _, X, X,
    #  X, X, _, _, _, _, _, _, _, _, X, X,
    #  X, X, _, _, _, _, _, _, _, _, X, X,
    #  X, X, p, p, p, p, p, p, p, p, X, X,
    #  X, X, r, n, b, Q, k, b, n, r, X, X,
    #  X, X, X, X, X, X, X, X, X, X, X, X,
    #  X, X, X, X, X, X, X, X, X, X, X, X]

    # empty location is 0, pawn 1, knight 2, bishop 3, rook 4, queen 5, king 6.
    # Black is negative eg -1 is a black pawn. A 7 is a boundary square to
    # prevent going off the edge of the board, or out of bounds of the array.

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

    # Named constant to help explain some math.
    __board_size = 12

    # Used to convert from board to displayable pieces. Currently the X in the
    # middle can be used to display the boundary board. Note that the board
    # uses negative numbers for black. This works well with python which allows
    # negative indeces.
    #
    # Also used in processing fen strings. For that it is important that the
    # pieces use the same characters as are used in FEN.

    __piece_chars = [".", "P", "N", "B", "R", "Q", "K", "X", "k", "q", "r",
                     "b", "n", "p"]

    # This is currently used to address pieces by name instead of by value on
    # the board. Currently both value and name are used, but name is preffered
    # for readability and potential future re-implentation of the board.
    __pieces_lookup = ["empty", "white_pawn", "white_knight", "white_bishop",
                       "white_rook", "white_queen", "white_king",
                       "out_of_bounds", "black_king", "black_queen",
                       "black_rook", "black_bishop", "black_knight",
                       "black_pawn"]

    def get_board_size(self):
        return Board.__board_size

    def get_piece_chars(self):
        return Board.List(__piece_chars)

    def get_pieces_lookup(self):
        return Board.List(__pieces_lookup)

    def __init__(self, fen=None):
        """ Sets the board to the start position or a position from an fen. """

        # The array to store the board
        self.board = list(Board.__start_board)

        # Determine which player's turn it is. White is True and Black is
        # False.
        self.cur_player_white = True

        self.castle_available = [True, True, True, True]
        self.en_passant_target = ""

        # TODO implement move counter

        if fen is not None:
            self.read_position(fen)

    def __str__(self):
        """ Return an ascii representation of the current board. """

        # The string that will be built from the board and then returned.
        output_string = ""

        # Used to split the line after each 8th piece
        file_count = 0

        # 9 through 1 and 2 through 10 are used to skip Displaying the outer
        # boundaries of the board and only show the center 8x8 board that the
        # player is interested in.
        #
        # The board representation has white in back. The outer index controls
        # which rank is displayed. By iterating backwards through that index,
        # white is shown in front.
        for i in range(9, 1, -1):
            for j in range(2, 10):
                file_count += 1

                # Use lookup table to translate pieces to strings. Then add
                # the piece and a space to the output string.
                p_chars = Board.__piece_chars

                # The location in the board list
                board_loc = i * Board.__board_size + j

                output_string += p_chars[self.board[board_loc]] + " "

                # Add a newline at the edge of the board.
                if file_count == 8:
                    output_string += "\n"
                    file_count = 0

        return output_string

    def read_position(self, fen):
        """ Import a board position from a fen string. """

        # TODO This function needs better documentation. I was in a hurry to
        # get some test input for the board and needed a way to get boards into
        # the engine for debugging.

        # 1. Process Board position:
        #     Each row is seperated by a /, the final (8th) row is ended with
        #     a space.

        #     For each of the 8 rows:
        #         Process each letter individually
        #
        #     Numbers in the board indicated a number of blank spaces, eg.
        #     4 = 4 empty spaces

        # Starting position in fen:
        # rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1

        # Simple pattern to match all the valid characters until the first
        # space in an fen string.
        fen_board = re.search("^([kqrbnpKQRBNP1-8/])+", fen).group(0)

        # Match either " w" or " b". Then remove the initial space. Then use
        # the match to assign the current player.
        fen_cur_player = re.search(" [wb]", fen).group(0)[1]
        self.cur_player_white = (fen_cur_player == "w")

        # Create a list containing each rank.
        prev_index = -1
        cur_index = 0
        ranks = []
        for i in range(7):
            cur_index = fen_board.index('/', prev_index + 1)
            ranks.append(fen_board[prev_index + 1:cur_index])
            prev_index = cur_index
        ranks.append(fen_board[prev_index + 1:len(fen_board)])

        for i in range(len(ranks)):
            # cur_rank = ranks[i]

            # Location on the board to start placing pieces
            starting_indices = [110, 98, 86, 74, 62, 50, 38, 26]

            # Convert empty squares to dots.

            # Pseudo-code
            #
            # for each letter l:
            #     if l in lookup_table:
            #        location(l).replace_with(dot_lookup[l - 1])

            # Solved through trial and error. I don't actually know how this
            # works
            # TODO Document and/or rewrite
            digit_lookup = ['1', '2', '3', '4', '5', '6', '7', '8']
            num_dots_lookup = ['.', '..', '...', '....', '.....', '......',
                               '.......', '........']

            # TODO What is tmp? It appears to be an array of the current rank,
            # storing a single character for each character in the fen string.
            # Then converting the number of empty locations in the fen string
            # to dots, which are what this board uses for empty spaces.
            tmp = ranks[i]
            j = 0
            while j < len(tmp):
                num_empty_str = tmp[j]
                if num_empty_str in digit_lookup:
                    num_empty = digit_lookup.index(num_empty_str)

                    tmp = tmp[:j] + num_dots_lookup[num_empty] + \
                        tmp[j + 1:]

                    j = 0
                j += 1

            for k in range(8):
                start_index = starting_indices[i]

                # Uses a constant intended for converting board data to
                # displayable characters. This works because FEN uses the same
                # characters as this board. The only difference is how empty
                # spaces are represented.
                piece = Board.__piece_chars.index(tmp[k])

                # Use negative values for black. The "X" is the last, non-black
                # piece in the array.
                if piece > Board.__piece_chars.index("X"):
                    piece -= len(self.__piece_chars)

                self.board[start_index + k] = piece

        return ranks

    def get_fen(self):
        # TODO Return an fen representation of the current board
        pass

    def get_all_moves(self, checking_king=False):
        """ checking_king should be true if the function is used to check if
        the king is in check. This prevents endless recursion.

        Returns a list of all valid moves from the current position in
        algebraic notation.

        TODO Currently returns moves in uci notation. """

        # Theory of operation:
        #
        # Search for every possible move by looking for every piece the current
        # player controls and then using a lookup table for non 'ray' pieces
        # (bishop, rook, queen) to look for all their potention moves.
        #
        # Steps
        #
        # 1. Find the location of every piece the current player controls.
        #
        # 2. If the piece is a 'ray piece', i.e. Bishop, Rook, Queen then
        # continue to 2.1, else go to 3
        #
        # 2.1 Ray pieces are easier to process by searching for the first
        # non-empty square in each direction the piece can move.
        #
        # TODO Bishop example
        #
        # 3. Else if it is any other piece, use a lookup table to find all
        # potential moves
        #
        # 3.1 Offset Arrays: For many of the moves, use arrays containing
        # position offsets. These work by storing the relative location in the
        # array for all of the possible moves of the following pieces: pawns,
        # knights and kings. Then the program seperately checks the validity of
        # each of moving to each of these locations.
        #
        # For example: If it's white's turn then find the location of every
        # white knight. For each white knight use the offset table (see source
        # code below for example values) to get the location of all eight
        # potential destination square for the knight. Do validity checks, ie
        # is the destination square empty or contains an enemy piece, for each
        # potential destination square.
        #
        # If the square is off the board nothing special happens, as there will
        # be an "X" at the location and since that isn't an empty square or an
        # opponent piece, the algorithm will just skip over it. That is the
        # benefit of using a 12 by 12 board.
        #
        # With the following board, there a 4 squares for the white knight on
        # g1 to move to, marked with question marks. 5 of these square are off
        # the board, and 1 of them is the white pawn on e3. The only two valid
        # moves are f3 and h3.

        # X, X,?X, X,?X, X, X, X, X, X, X, X
        # X,?X, X, X, X,?X, X, X, X, X, X, X
        # X, X, R, N, B, K, Q, B, N, R, X, X
        # X,?X, P, P, P,?P, P, P, P, P, X, X
        # X, X,?_, _,?_, _, _, _, _, _, X, X
        # X, X, _, _, _, _, _, _, _, _, X, X
        # X, X, _, _, _, _, _, _, _, _, X, X
        # X, X, _, _, _, _, _, _, _, _, X, X
        # X, X, p, p, p, p, p, p, p, p, X, X
        # X, X, r, n, b, k, q, b, n, r, X, X
        # X, X, X, X, X, X, X, X, X, X, X, X
        # X, X, X, X, X, X, X, X, X, X, X, X

        # Stores the index of each of the current players pieces.
        cur_pieces_list = []

        # List of legal moves.
        moves = []

        # Find the location of each of the current players pieces.
        # TODO Subtracting one was unintentional here. This will make it skip
        # the last element of the array. However, this is not bad because that
        # section of the array is of the board, so there is no reason to check
        # there. Therefor, this should be changed to avoid checking any
        # off-board location.
        # TODO use piece names instead of values for compatibility with board
        # changes. See __pieces_lookup.
        for i in range(len(self.board) - 1):
            if self.cur_player_white and (self.board[i] in [1, 2, 3, 4, 5, 6]):
                cur_pieces_list.append(i)

            elif not self.cur_player_white and \
                    (self.board[i] in [-1, -2, -3, -4, -5, -6]):
                cur_pieces_list.append(i)

        # TODO Potentially merge this with previous pieces list code.
        if self.cur_player_white:
            enemy_pieces_lookup = [-1, -2, -3, -4, -5, -6]
        else:
            enemy_pieces_lookup = [1, 2, 3, 4, 5, 6]

        # Check all possible moves for each piece.
        # TODO For all helper functions, rename i argument.
        for i in cur_pieces_list:
            piece = self.__pieces_lookup[self.board[i]]

            candidate_moves = []

            # Bishop, Rook and queen movement
            if piece in ["white_bishop", "black_bishop",
                         "white_rook", "black_rook",
                         "white_queen", "black_queen"]:
                candidate_moves += (
                    self.get_ray_piece_moves(i, enemy_pieces_lookup))

            # Pawn movement
            elif piece == "white_pawn" or piece == "black_pawn":
                # Currently pawns are the only implemented piece
                candidate_moves += self.get_legal_pawn_moves(
                    i, enemy_pieces_lookup)

            # Knight movement
            elif piece == "white_knight" or piece == "black_knight":
                candidate_moves += self. \
                    get_knight_moves(i, enemy_pieces_lookup)

            # King detection and movement
            elif piece == "white_king" or piece == "black_king":
                candidate_moves += self.get_king_moves(i, enemy_pieces_lookup)

            # Convert moves to uci (similar to algebraic notation, but uses
            # source location instead of source piece). See uci documentation.
            for j in candidate_moves:
                # If being used to determine if king is in check, do not check
                # if next player would be left in check (short circuit to avoid
                # infinite recursion), but do still add moves. Otherwise, if
                # the king is left in check, do not allow moves.
                if (checking_king) or (not self.is_king_in_check(i)):
                    moves.append(get_algebraic_from_index(i) +
                                 get_algebraic_from_index(j))

        return moves

    def get_legal_pawn_moves(self, i, enemy_pieces_lookup):
        """ Return the potential pawn moves from the current position.

        TODO pawn moves are not fully checked for legality. """

        # Pawn moves are surprisingly complicated compared to the rest of the
        # pieces for the following reasons:
        #
        # 1. The direction a pawn can move depends on it's color
        #
        # 2. A pawn can move twice only on it's first move
        #
        # 3. A pawn can capture en passant
        #
        # 4. A pawn captures in a diffent way than it moves
        #
        # Pawn offset
        #
        # There are four potential moves for a pawn:
        #
        # 1. 1 forward (unless blocked or pinned),
        #
        # 2. 2 forward (if starting on initial square, and not blocked or
        # pinned)
        #
        # 3. capture on adjacent diagonal squares (if not pinned and an
        # oppenents piece is on the square, or if en passant is allowed).
        #
        # 4. TODO En passant capture
        #
        # 5. TODO Promotion on final Rank

        # X, X, X, X, X, X, X, X, X, X, X, X
        # X, X, X, X, X, X, X, X, X, X, X, X
        # X, X, R, N, B, K, Q, B, N, R, X, X
        # X, X, P, P, _, P, P, P, P, P, X, X
        # X, X, _, _, _, _, _, _, _, _, X, X
        # X, X, _, _, _, _, _, _, _, _, X, X
        # X, X, _, _, P, p, p, _, _, _, X, X
        # X, X, _,?_,?_,?_, _, _, _, _, X, X
        # X, X, p, p,?p, _, _, p, p, p, X, X
        # X, X, r, n, b, k, q, b, n, r, X, X
        # X, X, X, X, X, X, X, X, X, X, X, X
        # X, X, X, X, X, X, X, X, X, X, X, X

        candidate_moves = []

        pawn_double_lookup = [
                              # White offsets
                              [38, 39, 40, 41, 42, 43, 44, 45],

                              # Black offsets
                              [98, 99, 100, 101, 102, 103, 104, 105]]

        # Short repeated use of board size
        b_size = Board.__board_size

        # The currently tested potential destination location for the pawn.
        # location = 0

        if self.cur_player_white:
            pawn_move_offset = i + b_size
            pawn_captures_offsets = [i + b_size - 1,
                                     i + b_size + 1]
            pawn_move_double_offset = i + 2 * b_size
        else:
            pawn_move_offset = i - b_size
            pawn_captures_offsets = [i - b_size + 1, i - b_size - 1]
            pawn_move_double_offset = i - 2 * b_size

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

        # If the pawn is at a location where it can move double.
        if ((self.cur_player_white and (i in pawn_double_lookup[0])) or
                (not self.cur_player_white and (i in pawn_double_lookup[1]))):
            location = pawn_move_double_offset

            # TODO Rewrite if condition for readability
            if self.board[location] == 0:
                if (self.cur_player_white and
                    (self.board[location - Board.__board_size] == 0)
                    or (not self.cur_player_white
                        and self.board[location + Board.__board_size] == 0)):
                    candidate_moves.append(location)

        return candidate_moves

    def get_knight_moves(self, i, enemy_pieces_lookup):
        candidate_moves = []

        # Knight offsets
        #
        # The knight has less complicated movement than the pawn. Every offset
        # needs the exact same checks done for validity. There are exactly 8
        # moves checked for every knight.
        #
        # For an example of how this algorithm works, look at the move
        # generation function that calls this function.

        b_size = Board.__board_size

        # Knight moves two in one direction and two the other direction.
        knight_offsets = [i - 2 * b_size - 1, i - 2 * b_size + 1,
                          i - b_size - 2, i - b_size + 2,
                          i + b_size - 2, i + b_size + 2,
                          i + 2 * b_size - 1, i + 2 * b_size + 1]

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

        # X, X, X, X, X, X, X, X, X, X, X, X
        # X, X, X, X,?X,?X,?X, X, X, X, X, X
        # X, X, R, N,?B, K,?Q, B, N, R, X, X
        # X, X, P, P,?P,?P,?P, P, P, P, X, X
        # X, X, _, _, _, _, _, _, _, _, X, X
        # X, X, _, _, _, _, _, _, _, _, X, X
        # X, X, _, _, _, _, _, _, _, _, X, X
        # X, X, _, _, _, _, _, _, _, _, X, X
        # X, X, p, p, p, p, p, p, p, p, X, X
        # X, X, r, n, b, k, q, b, n, r, X, X
        # X, X, X, X, X, X, X, X, X, X, X, X
        # X, X, X, X, X, X, X, X, X, X, X, X

        # TODO Write offsets relative to board size.
        king_offsets = [i - 13, i - 12, i - 11, i - 1, i + 1, i + 11, i + 12, i
                        + 13]
        valid_locations = enemy_pieces_lookup + [0]

        # Moves and captures
        for location in king_offsets:
            if self.board[location] in valid_locations:
                candidate_moves.append(location)

        return candidate_moves

    def get_ray_piece_moves(self, i, enemy_pieces_lookup):
        # These tests will be different from the other pieces. Instead of
        # checking a set of specific locations, I will test a range of
        # locations and stop checking after the range is blocked or the range
        # goes off the edge of the board.

        # TODO More documentation of ray pieces code

        candidate_moves = []

        piece = Board.__pieces_lookup[self.board[i]]

        valid_locations_lookup = enemy_pieces_lookup + [0]

        if piece == "white_bishop" or piece == "black_bishop":
            candidate_moves = self.get_bishop_moves(i, valid_locations_lookup)
        elif piece == "white_rook" or piece == "black_rook":
            candidate_moves = self.get_rook_moves(i, valid_locations_lookup)
        elif piece == "white_queen" or piece == "black_queen":
            # Queen can be treated like a combination of a bishop and a rook
            candidate_moves = self. \
                get_bishop_moves(i, valid_locations_lookup) \
                + self.get_rook_moves(i, valid_locations_lookup)

        return candidate_moves

    def get_bishop_moves(self, i, valid_locations_lookup):

        # X, X, X, X, X, X, X, X, X, X, X, X
        # X, X, X,?X, X,?X, X, X, X, X, X, X
        # X, X, R, N,?B, K, Q, B, N, R, X, X
        # X, X, P,?P, P,?_, P, P, P, P, X, X
        # X, X, _, _, _, _,?_, _, _, _, X, X
        # X, X, _, _, _, P, _,?_, _, _, X, X
        # X, X, _, _, _, _, _, _,?_, _, X, X
        # X, X, _, _, _, p, _, _, _,?_, X, X
        # X, X, p, p, p, _, p, p, p, p,?X, X
        # X, X, r, n, b, k, q, b, n, r, X, X
        # X, X, X, X, X, X, X, X, X, X, X, X
        # X, X, X, X, X, X, X, X, X, X, X, X

        candidate_moves = []

        # Simplifies searching for next square.
        direction_table = [[-1, -1], [-1, 1],
                           [+1, -1], [+1, 1]]
        for k in range(len(direction_table)):
            cur_direction = direction_table[k]

            # Used to determine whether to continue a looking for the next
            # location. This is changed to true whenever the next location
            # contains anything other than an empty space.
            end_of_diagonal = False

            # The longest possible diagonal is the fianchetto. With the bishop
            # on a1, the diagonal would take 8 squares to find the edge of the
            # board.
            for j in range(1, 8):
                next_piece_location = \
                    i + (j * (12 * cur_direction[0])) + (j * cur_direction[1])
                piece = self.board[next_piece_location]
                location_empty_val = Board.__pieces_lookup.index("empty")

                # Sets end_of_diagonal to False if anything other than an empty
                # location is encountered. Otherwise sets it to True to end the
                # loop.
                end_of_diagonal = piece != location_empty_val

                # If piece in enemy lookup table or square is empty, mark
                # location as a valid target square. Else mark the square
                # invalid.
                if piece in valid_locations_lookup:
                    candidate_moves.append(next_piece_location)

                # Do not continue searching after the first non-empty square is
                # located. This speeds up the search and prevents any need for
                # array bounds checking.
                if end_of_diagonal:
                    break

        return candidate_moves

    def get_rook_moves(self, i, valid_locations_lookup):
        """ Return valid rook moves """

        # X, X, X, X, X, X, X, X, X, X, X, X
        # X, X,?X, X, X, X, X, X, X, X, X, X
        # X,?X,?R,?N, B, K, Q, B, N, R, X, X
        # X, X,?_, P, P, P, P, P, P, P, X, X
        # X, X,?_, _, _, _, _, _, _, _, X, X
        # X, X,?P, _, _, _, _, _, _, _, X, X
        # X, X, _, _, _, _, _, _, _, _, X, X
        # X, X, _, _, _, _, _, _, _, _, X, X
        # X, X, p, p, p, p, p, p, p, p, X, X
        # X, X, r, n, b, k, q, b, n, r, X, X
        # X, X, X, X, X, X, X, X, X, X, X, X
        # X, X, X, X, X, X, X, X, X, X, X, X

        candidate_moves = []

        # First, generate two diagonals for the bishop.

        # Simplifies searching for next square.
        direction_table = [[-1, 0], [1, 0],
                           [0, -1], [0, 1]]
        for k in range(4):
            cur_direction = direction_table[k]

            # Used to determine whether to continue a looking for the next
            # location. This is changed to true whenever the next location
            # contains anything other than an empty space.
            end_of_diagonal = False

            # The longest possible diagonal is the fianchetto. With the bishop
            # on a1, the diagonal would take 8 squares to find the edge of the
            # board.
            for j in range(1, 8):
                next_piece_location = (i + (j * (12 * cur_direction[0]))
                                       + (j * cur_direction[1]))
                piece = self.board[next_piece_location]
                location_empty_val = Board.__pieces_lookup.index("empty")

                # Sets end_of_diagonal to False if anything other than an empty
                # location is encountered. Otherwise sets it to True to end the
                # loop.
                end_of_diagonal = piece != location_empty_val

                # If piece in enemy lookup table or square is empty, mark
                # location as a valid target square. Else mark the square
                # invalid.
                if piece in valid_locations_lookup:
                    candidate_moves.append(next_piece_location)

                # Do not continue searching after the first non-empty square is
                # located. This speeds up the search and prevents any need for
                # array bounds checking.
                # TODO add this condition to for loop?
                if end_of_diagonal:
                    break

        return candidate_moves

    def is_king_in_check(self, king_location):
        ''' Return True if the current player's king is attacked by an enemy
        piece. '''

        # Strategy: Find a list of every square that an enemy piece is
        # attacking and check if the king is on one of those squares.
        # Potentially this will be very similar to regular move generation,
        # perhaps I can just call it with the current player inverted.

        king_in_check = False

        self.cur_player_white = not self.cur_player_white
        enemy_moves = self.get_all_moves(checking_king=True)
        self.cur_player_white = not self.cur_player_white

        # 1. Store king location in algebraic
        king_algebriac = get_algebraic_from_index(king_location)

        # Break is used to leave the loop early if an attacker if found.
        for move in enemy_moves:

            # 2. Check if second algebraic location of each move in enemy_moves
            # matches the king's location. The algebriac location of the
            # attacked square in uci notation is the last two characters in the
            # move notation.
            attacked_square = move[2] + move[3]
            if attacked_square == king_algebriac:
                king_in_check = True
                break

        return king_in_check

    def make_move(self, from_algebraic_location, to_algebraic_location=None):
        """ Make a move on the board. Test whether the move is valid, perhaps
        by testing if get_all_moves returns the given move, before calling
        function. If the move is invalid, a runtime exception will be raised.
        If only from_algebraic_location is given, the move is assumed to be a 4
        character string representing both moves.  """

        if to_algebraic_location is None:
            # TODO Only allow length 4 string here
            move = from_algebraic_location
            self.make_move(move[0] + move[1], move[2] + move[3])
        else:
            move_from_index = move_to_index = piece = 0

            move_algebraic = from_algebraic_location + to_algebraic_location

            # Test if move is valid
            valid_moves = self.get_all_moves()

            if move_algebraic not in valid_moves:
                logging.exception("Invalid move played " + move_algebraic)
                logging.info("Moves: " + str(valid_moves))
                logging.info("Board: " + str(self))
                raise RuntimeError("Move not valid")

            # Convert from algebraic to board indices

            move_from_index = Board. \
                get_index_from_algebraic(from_algebraic_location)
            move_to_index = Board. \
                get_index_from_algebraic(to_algebraic_location)

            # remove piece at old location
            piece = self.board[move_from_index]
            self.board[move_from_index] = self.__pieces_lookup.index("empty")
            self.board[move_to_index] = piece

            # Alternate current players
            self.cur_player_white = not self.cur_player_white


def get_algebraic_from_index(index):
    """ Convert from a board location array index to algebraic board
    location

    index = 26 -> a1, index = 38 -> a2 """

    algebraic = ""

    # TODO Document how algebraic values are retrieved from tables and
    # math.
    if index in [26, 38, 50, 62, 74, 86, 98, 110]:
        algebraic = "a" + str(((index - 2) // 12) - 1)

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

    elif index in [32, 44, 56, 68, 80, 92, 104, 116]:
        algebraic = "g" + str(((index - 8) // 12) - 1)

    elif index in [33, 45, 57, 69, 81, 93, 105, 117]:
        algebraic = "h" + str(((index - 9) // 12) - 1)

    return algebraic


def get_index_from_algebraic(algebraic):
    """ Return the board index of a given algebraic board location. """

    # A simple table that has the unique algebraic strings at the correct
    # location on the board. Some spaces have been removed on purpose to
    # keep the line length under 80 without damaging readability.
    algebraic_conversion_table = \
        ["", "", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "", "",
            "", "", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "  ", "", "",
            "", "", "a1", "b1", "c1", "d1", "e1", "f1", "g1", "h1", "", "",
            "", "", "a2", "b2", "c2", "d2", "e2", "f2", "g2", "h2", "", "",
            "", "", "a3", "b3", "c3", "d3", "e3", "f3", "g3", "h3", "", "",
            "", "", "a4", "b4", "c4", "d4", "e4", "f4", "g4", "h4", "", "",
            "", "", "a5", "b5", "c5", "d5", "e5", "f5", "g5", "h5", "", "",
            "", "", "a6", "b6", "c6", "d6", "e6", "f6", "g6", "h6", "", "",
            "", "", "a7", "b7", "c7", "d7", "e7", "f7", "g7", "h7", "", "",
            "", "", "a8", "b8", "c8", "d8", "e8", "f8", "g8", "h8"]

    return algebraic_conversion_table.index(algebraic)


def get_board_layout():
    """ Returns a string with a visual representation of how the board is
    mapped to an array. Useful for debugging. The Outer section of the
    board, the part used for out of bounds detection, is not shown. """

    output_string = ""
    board = Board()

    for i in range(9, 1, -1):
        for j in range(2, 10):
            output_string += str((i * board.get_board_size()) + j) + "\t"
        output_string += "\n"

    return output_string
