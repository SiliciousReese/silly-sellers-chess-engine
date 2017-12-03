#!/usr/bin/env python


# Check if resource folder exists
import os

# Python logging
import logging

# Chess board
from board.Board import Board


def main():
    # TODO implement better file handling.

    __res_file_name = "res/"

    # Temporarily avoid using res folder to avoid runtime error if folder
    # does not exist.
    res_file_exists = os.path.exists(__res_file_name)
    if not res_file_exists:
        __res_file_name = "./"

    __log_file_name = __res_file_name + "chess-engine-log.log"

    # Start logger
    logging.basicConfig(filename=__log_file_name, level=logging.DEBUG)

    logging.info("Started chess engine")

    # Test board logging
    Board()

    logging.info("Exiting chess engine")


if __name__ == '__main__':
    main()
