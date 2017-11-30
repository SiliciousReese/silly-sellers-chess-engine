# defines a game board and handles piece movement initalizes to a new game state
class Board:
    chess_board=[]
    #constructor for board class
    def __init__(self):
        print("Hello From Board")
        self.new_board()
        
    #checks if piece can move and then if moveable changes the location of the piece
    def movePiece(start,end):
        values="abcdefgh12345678"
        if len(start)&len(end)==2:
            if start[0]in values & start[1]in values:
                if end[0]in values & end[1]in values:
                    # figure put if piece can move now
                    pass
    def new_board(self):
        self.chess_board=["RNBQKBNR",
                          "PPPPPPPP",
                          "00000000",
                          "00000000",
                          "00000000",
                          "00000000",
                          "pppppppp",
                          "rnbqkbnr"]
