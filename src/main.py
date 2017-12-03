#!/usr/bin/env python

# Python logging
import logging

# Chess board
from board.Board import Board


def main():
    # TODO implement better file handling.
    __res_file_name = "res/"
    __log_file_name = __res_file_name + "chess-engine-log.log"

    # Start logger
    logging.basicConfig(filename=__log_file_name, level=logging.DEBUG)

    logging.info("Started chess engine")

    # Test board logging
    Board()

    logging.info("Exiting chess engine")


if __name__ == '__main__':
    main()
