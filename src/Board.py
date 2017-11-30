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
    __start_board = [4, 2, 3, 5, 6, 3, 2, 4,
                     1, 1, 1, 1, 1, 1, 1, 1,
                     0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0,
                     0, 0, 0, 0, 0, 0, 0, 0,
                     -1, -1, -1, -1, -1, -1, -1, -1,
                     -4, -2, -3, -5, -6, -3, -2, -4]
    board = __start_board
