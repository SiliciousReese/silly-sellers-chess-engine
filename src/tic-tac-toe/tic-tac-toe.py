#!/usr/bin/env python

# Uses regular expressions for
import re

# Allow user to add pieces to a tic tac toe board
#
# 1. Create board
#
# 2. Ask user to enter a location on the board
#
# 3. Parse and validate Location
#
# 3a. Ask user to re-enter invalid location
#
# 3a1. Location is valid if and only if the location is empty on the board and
# the row and column numbers are greater than or equal to 1 and less than or
# equal to the length of the board
#
# 4. Add piece to board
#
# 5. Repeat until board is full
#
# TODO Make function documentation consistent


# Size of board. The board is a square, so this is the number of columns in a
# row and the number of rows in a column. This should work for numbers large
# than 3, but it hasn't been tested. The limiting factor for the size, other
# than game difficulty, is how much space drawing the board will take up.
B_SIZE = 3

# Player characters to show on board
P1_CHAR = 'X'
P2_CHAR = 'O'


def init_board():
    '''
    Return a matrix with both height and width of B_SIZE initialized with all
    zeros.
    '''

    game_board = []

    # Simple, default case. This entire function would be one line in a
    # typical tic-tac-toe program, but I want to make the program work with
    # any board size.
    if B_SIZE == 3:
        game_board = [[' ', ' ', ' '],
                      [' ', ' ', ' '],
                      [' ', ' ', ' ']]

    else:
        game_board = []

        # The game board is currently implemented as a list of lists. This
        # creates the inner list, which will be a list of length B_SIZE filled
        # with a single space character to indicate an empty position on the
        # board.
        empty_inner_board = []

        for i in range(B_SIZE):
            empty_inner_board.append(' ')

        for i in range(B_SIZE):
            game_board.append(empty_inner_board)

    return game_board


def get_input(board):
    '''
    Get user input and return a list with the first element being the row and
    the second element being the column of an empty location on the game board.
    '''
    # Stores the location the user is going to enter.
    location = [0, 0]

    user_in_text = input(
        'Enter the location in row,column form. Eg: 1,1 for the\n'
        'top-left most location on the board, 3,2 for the third\n'
        'row, second column. ')
    valid = False

    # Ask the user to Enter the location again if it is invalid. Otherwise
    # convert the location to a list.
    while not valid:
        # Return true if the given input string is valid. The string is
        # considered valid if and only if it is an integer, followed by a
        # comma, followed by another integer. Both integers must be positive,
        # and no symbols other than digits and commas are allowed.
        #
        # TODO Check for 0's, currently these are treated as if the user meant 1
        while re.fullmatch('\d+,\d+', user_in_text) == None:
            user_in_text = input('Invalid input detected. Please try again. ')

        location = parse_location_text(user_in_text)
        # Clear the text so if validation fails the regex will test won't be
        # passed from the old input.
        user_in_text = ''
        valid = validate_location(board, location[0], location[1])

    return location


def parse_location_text(user_input):
    '''
    Parse a string and return a list where the first element is the integer
    before a comma and the and the second digit is the integer after the comma.
    '''

    location = [0, 0]

    # Convert the string to two integers. Then subtract 1 because the user was
    # told that 1,1 is the top left location on the board, but the index of the
    # board list is 0,0. If the user did not understand instructions and uses a
    # 0 in the array, which currently passes the input validation, change it to
    # a 1.
    matches = re.findall('\d+', user_input)
    for i in range(2):
        location[i] = int(matches[i]) - 1

        if location[i] == -1:
            location[i] = 0
            print("0 entered for location, assuming you meant 1 instead.")

    return location


def validate_location(board, row, col):
    ''' Return true if the location is available for a piece to be placed at on
    the given board.  '''

    valid = True

    # Checks that the row number is in the range of rows on the board
    valid = valid and row >= 0 and row < B_SIZE
    # Does the same for the column.
    valid = valid and col >= 0 and col < B_SIZE
    # Tests that the location on the board is empty.
    valid = valid and board[row][col] == ' '

    return valid


def print_board(board):

    '''
    Print the given board to a text display.

    Should look similar to this:

    #  --- --- ---
    # |   | O |   |
    #  --- --- ---
    # | X | O |   |
    #  --- --- ---
    # |   |   |   |
    #  --- --- ---
    '''

    # Prints board two lines at a time. The first line is the 3 dashes above
    # each box. The second line consists of a pipe at the beginning of each box,
    # then either three spaces if the space is empty, or a space and the
    # character of the current player, then a closing pipe. There is only one
    # pipe connecting each box, so it does not add a closing pipe if there are
    # more boxes to draw. Prints 3 lines on the final iteration because the
    # board ends with a row of dashes
    for i in range(B_SIZE):
        # out_text will store a buffer for the text before it is written on the
        # screen. It must be cleared after each loop.
        out_text = ''

        # for each row print one space and 3 dashes
        for j in range(B_SIZE):
            out_text += ' ---'

        print(out_text)

        out_text = ''
        # Then print one pipe and 2 spaces with the piece at the current
        # board location in between them
        for j in range(B_SIZE):
            out_text += '| ' + str(board[i][j] + ' ')

        # Previous loop misses the final pipe.
        out_text += '|'
        print(out_text)

        out_text = ''
        # This finishes the shape because the previous loops do not finish the
        # last row.
        if i + 1 == B_SIZE:
            for j in range(B_SIZE):
                if j + 1 == B_SIZE:
                    out_text += ' ---'
                    print(out_text)
                else:
                    out_text += ' ---'


def check_win(board):
    '''
    for each player check if they have 3 in one row. Each of the tests works
    by assuming the game is has been won by each method, and then looking for
    a location on the board that proves this wrong
    '''
    for char in [P1_CHAR, P2_CHAR]:
        for i in range(B_SIZE):
            is_won = True
            for j in range(B_SIZE):
                is_won &= board[i][j] == char

            if is_won:
                break
        if is_won:
            return True

        # For each player check if they have 3 in one column
        for j in range(B_SIZE):
            is_won = True
            for i in range(B_SIZE):
                is_won &= board[i][j] == char

            if is_won:
                break
        if is_won:
            return True

        # For each player, check the diagonal starting at the top left most
        # space
        is_won = True
        for i in range(B_SIZE):
            is_won &= board[i][i] == char

        if is_won:
            return True

        # For each player, check the diagonal starting at the top right most
        # space
        is_won = True
        for i in range(B_SIZE):
            is_won &= board[i][B_SIZE - i - 1] == char

        if is_won:
            return True
    return False


print('This program will loop until all the locations on a board are filled'
      'Enter locations in row,column form. Eg: 1,1 for the\n'
      'top-left most location on the board, 3,2 for the third\n'
      'row, second column. ')

# Keeps track of the remaining number of moves that will be made before the
# board is full. This is used to allow the program to know when to stop asking
# for more input from the user.
num_moves = B_SIZE * B_SIZE

game_board = init_board()

# Uses to alternate between players and to determine which symbol to add to the
# board.
player = P1_CHAR

# num_moves is decremented every loop. This is a quick way to check if the board
# is full. The loop exits at the end after the last player moves. Note that the
# loop exits prematurely when a player wins, so the code after the loop will
# always run.
while num_moves > 0:

    print_board(game_board)

    location = get_input(game_board)

    # Place the move on the board.
    game_board[location[0]][location[1]] = player

    # Print win text and exit loop if the current player just won.
    if check_win(game_board):
        print_board(game_board)
        print("Game over. " + player + " is the winner!.")
        break

    num_moves -= 1

    # Alternate between players
    if player == P1_CHAR:
        player = P2_CHAR
    else:
        player = P1_CHAR

if num_moves == 0:
    print_board(game_board)
    print('The board is full. There is nothing more to do.')
