#!/usr/bin/env python

from Board import Board

# A Standalone program to debug board features

if __name__ == '__main__':

    # Some sample fen strings for testing. fens[0] is Start position. fens[1]
    # is the common open game. [2] is a knight endgame. [3] is from another
    # opening. [4] is from a sicilian game.
    fens = [
            # [0] start position
            "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",

            # [1] Open Game
            "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1",

            # [2] King and knight drawn ending
            "k7/8/8/4N3/8/8/8/3K4 b - - 13 56",

            # [3] An unnamed sicilian variation (1. e4 c5 2. e5? d5?)
            "rnbqkbnr/pp2pppp/8/2ppP3/8/8/PPPP1PPP/RNBQKBNR w KQkq d6 0 3",

            # [4] A line in the sicilian
            "r2q3r/5k1p/p2p2p1/1p2n1bQ/4P3/2N5/PPP4P/1K1R1B1R w - - 0 19",

            # [5] A line in the french
            "rnbqk2r/1ppnb2p/p3p1pQ/3pPpB1/3P3P/2N5/PPP2PP1/R3KBNR "
            "b KQkq - 1 9",

            # [6] The French defense
            "rnbqkbnr/ppp2ppp/4p3/3p4/3PP3/8/PPP2PPP/RNBQKBNR w KQkq - 0 3",

            # [7] Sample position with bishop on h1 with empty diagonal. Used
            # to test bishop movement
            "1nbqkbnr/r3ppp1/1p1p3p/p1p1P3/7P/6P1/PPPP1P1R/RNBQK1NB w Qk - 2 8"
           ]

    valid_moves_from_fens = [
        # [0]
        ['a2a3', 'a2a4', 'b1a3', 'b1c3', 'b2b3', 'b2b4', 'c2c3', 'c2c4',
         'd2d3', 'd2d4', 'e2e3', 'e2e4', 'f2f3', 'f2f4', 'g1f3', 'g1h3',
         'g2g3', 'g2g4', 'h2h3', 'h2h4'],
        # [1]
        None,
        # [2]
        None,
        # [3]
        None,
        # [4]
        None,
        # [5]
        None,
        # [6]
        None,
        # [7]
        None,
        # [8]
        None
    ]

    board = Board()
    str(board)

    # Test fen processing and board drawing and move generation
    print()
    print(Board.get_board_layout())
    print("# Testing fens 0 through " + str(len(fens) - 1) + " #")
    print()
    for i in range(len(fens)):
        board.read_position(fens[i])
        # print(Board.get_board_layout())

        print("# Testing fen string number:", str(i), "#")

        if valid_moves_from_fens[i] is not None:
            moves = sorted(board.get_all_moves())
            correct_moves = valid_moves_from_fens[i]
            if moves == correct_moves:
                print("# PASSED move generation #")
            else:
                print("# FAILED move generation #")
                print("Correct response:", correct_moves)
                print("Actual response:", moves)
            print(board)
        else:
            print("# NOT TESTED: correct moves not known #")
            print(board)
            print(sorted(board.get_all_moves()))
        print()
        print()
