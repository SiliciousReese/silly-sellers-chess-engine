#!/usr/bin/env python

from Board import Board

""" A Standalone program to debug board features """

if __name__ == '__main__':
    board = Board()
    board.print_board()
    print(board.get_all_moves())
