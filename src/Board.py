''' Board representation '''


class Board():

    ''' Start position

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

     blank is 0, pawn 1, knight 2, bishop 3, rook 4, queen 5, king 6

     black is negative eg -1 black pawn
     '''
    __start_board = [+4, +2, +3, +5, +6, +3, +2, +4,
                     +1, +1, +1, +1, +1, +1, +1, +1,
                     +0, +0, +0, +0, +0, +0, +0, +0,
                     +0, +0, +0, +0, +0, +0, +0, +0,
                     +0, +0, +0, +0, +0, +0, +0, +0,
                     +0, +0, +0, +0, +0, +0, +0, +0,
                     -1, -1, -1, -1, -1, -1, -1, -1,
                     -4, -2, -3, -5, -6, -3, -2, -4]

    ''' Used to convert from board to displayable pieces '''
    __piece_chars = [".", "P", "N", "B", "R", "Q", "K", "k", "q", "r", "b", "n",
                     "p"]

    def __init__(self):
        self.board = Board.__start_board

    def get_all_moves(self):
        ''' Returns a list of all valid moves from the current position in
        algebraic notation '''

        ''' TODO Get moves '''

        ''' TODO Start with uci notation since it is easier to parse, then
        translate to algebriac '''
        pass

    def print_board(self):
        ''' TODO Print the board to standard out '''

        ''' Print in reverse order, (black in back) '''
        ''' TODO use string builder '''

        line = ''

        ''' Used to split the line after each 8th piece '''
        ''' TODO Board prints with white in back, which isn't wrong but white
        looks better in front '''
        file_count = 0
        for i in Board.__start_board:
            file_count += 1

            ''' Add piece and space to string '''
            line += Board.__piece_chars[i] + " "

            if file_count == 8:
                line += '\n'
                file_count = 0

        print(line)
