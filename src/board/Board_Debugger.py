#!/usr/bin/env python

from Board import Board

""" A Standalone program to debug board features """

if __name__ == '__main__':
    board = Board()

    board.print_board()

    """ Start position """
    fens =["rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1",
           "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1",
           "k7/8/8/4N3/8/8/8/3K4 b - - 13 56",
           "rnbqkbnr/pp2pppp/8/2ppP3/8/8/PPPP1PPP/RNBQKBNR w KQkq d6 0 3"]

    print("trying fen 3")
    board.read_position(fens[2])
    board.print_board()
    print()

    print("trying fen 4")
    board.read_position(fens[3])
    board.print_board()
    print()

    # print("printing result of fen1")
    # print(board.read_position(fen1))
    # print()

    #board.print_board()

    # print(board.get_all_moves())
