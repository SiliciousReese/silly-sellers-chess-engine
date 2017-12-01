#!/usr/bin/env python

from Board import Board

""" A Standalone program to debug board features """

if __name__ == '__main__':
    board = Board()

    """ Start position """
    fen1 = "rnbqkbnr/pppppppp/8/8/8/8/PPPPPPPP/RNBQKBNR w KQkq - 0 1"
    fen2 = "rnbqkbnr/pppppppp/8/8/4P3/8/PPPP1PPP/RNBQKBNR b KQkq e3 0 1"

    # print("trying fen 1")
    # board.read_position(fen1)
    # print()

    print("trying fen 2")
    board.read_position(fen2)
    print()

    # print("printing result of fen1")
    # print(board.read_position(fen1))
    # print()

    board.print_board()

    # print(board.get_all_moves())
