#!/usr/bin/env python
from Board import Board


def main():
    board = Board()
    board.print_board()
    board.get_all_moves()

if __name__ == '__main__':
    main()
