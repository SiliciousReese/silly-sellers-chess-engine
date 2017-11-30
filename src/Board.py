# defines a game board and handles piece movement initalizes to a new game state
class Board:
    #constructor for board class
    def __init__(self):
        print("Hello From Board")
        self.chess_board=["rnbqkbnr",
                          "pppppppp",
                          "00000000",
                          "00000000",
                          "00000000",
                          "00000000",
                          "pppppppp",
                          "rnbqkbnr"]    
