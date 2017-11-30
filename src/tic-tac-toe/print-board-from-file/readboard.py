filename = 'board.bin'
board = []


def readBoard():
    f = open(filename, 'r')

    # The newlines at the end of every line are counted as one extra byte per
    # line.
    size = 8 * 9
    board_text_from_file = f.read(size)

    return board_text_from_file


# TODO checkboard()
def checkBoard():
    ''' Returns None if the board is valid. Otherwise a message describing what
    is wrong with the board is returned. '''

    error_message = None

    return error_message


def printBoard():
    print(board)


if __name__ == '__main__':
    board = readBoard()

    error = checkBoard()

    if error == None:
        printBoard()
    else:
        print(error)
