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

            # [3] An unnamed sicilian variation (1. e4 c5 2. e5 d5)
            "rnbqkbnr/pp2pppp/8/2ppP3/8/8/PPPP1PPP/RNBQKBNR w KQkq d6 0 3",

            # [4] A line in the sicilian
            "r2q3r/5k1p/p2p2p1/1p2n1bQ/4P3/2N5/PPP4P/1K1R1B1R w - - 0 19",

            # [5] A line in the french
            "rnbqk2r/1ppnb2p/p3p1pQ/3pPpB1/3P3P/2N5/PPP2PP1/R3KBNR "
            "b KQkq - 1 9",

            # [6] The French Defense
            "rnbqkbnr/ppp2ppp/4p3/3p4/3PP3/8/PPP2PPP/RNBQKBNR w KQkq - 0 3"]

    # board = Board()
    str(Board())

    board = Board(fens[0])
    print(board)
    print(board.get_all_moves())
    print()

    # Test fen processing and board drawing and move generation
    print()
    print("# Testing fens 0 through " + str(len(fens) - 1) + " #")
    print()
    for fen in fens:
        board.read_position(fen)
        print(Board.get_board_layout())
        print(board)
        print(board.get_all_moves())
        print()
