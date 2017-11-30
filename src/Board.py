# defines a game board and handles piece movement initalizes to a new game state
class Board:
    chess_board=[]
    #constructor for board class
    def __init__(self):
        print("Hello From Board")
        self.new_board()
        
    #checks if piece can move and then if moveable changes the location of the piece
    def movePiece(start,end):
        firstValues= "abcdefgh"
        secondValues="12345678"
        if len(start)&len(end) == 2:
            if start[0]in firstValues & start[1]in secondValues:
                if end[0]in firstValues & end[1]in secondValues:
                    # figure out if piece can move now
                    pass

    #resets bord to new game state white == upper black  ==  lower
    def new_board(self):
        self.chess_board=["RNBQKBNR",
                          "PPPPPPPP",
                          "00000000",
                          "00000000",
                          "00000000",
                          "00000000",
                          "pppppppp",
                          "rnbqkbnr"]

    # check the valididty of a move return true if valid move
    #x,y should be in terms of array values
    def checkMove(self,xStart,yStart,xEnd,yEnd):
        piece=self.chess_board[xStart][yStart]
        #check piece movement
        if piece == 'p' | piece == 'P':
            return checkPawn(self.chess_board,piece,xStart,yStart,xEnd,yEnd)
        elif piece == 'R' | piece == 'r':
            return checkRook(self.chess_board,piece,xStart,yStart,xEnd,yEnd)

    #roock movement logic hidden here
    def checkRook(board,piece,xStart,yStart,xEnd,yEnd):
        if xStart == xEnd:
            slc=[yStart,yEnd]
            slc.sort()
            for i in board[xEnd][slc[0]:slc[1]]:
                if i != '0':
                    return False
            return True
        elif yStart == yEnd:
            slc=[xStart,x,End]
            slc.sort()
            for i in board[slc[0]:slc[1]][yEnd]:
                if i != '0':
                    return False
            return True
        else:
            return False

    #pawn logic hidden here
    def checkPawn(board,piece,xStart,yStart,xEnd,yEnd):
    #todo add En passant eventually needs check lastmove varialbe
        #black pawn logic
        if piece == 'p':
            if yStart == 7:
                if yStart-2 == yEnd:
                    if xStart == xEnd:
                        if board[xEnd][yEnd] == '0':
                            return True
                        else:
                            return False
                    else:
                        return False
            elif yStart-1 == yEnd:
                if xStart == xEnd:
                    if board[xEnd][yEnd] == '0':
                        return True
                    else:
                        return False
                elif xStart-1 == xEnd | xStart+1 == xEnd:
                    if board[xEnd][yEnd]!='0':
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False

        #white pawn logic
        elif piece == 'P':
            if yStart == 2:
                if yStart+2 == yEnd:
                    if xStart == xEnd:
                        if board[xEnd][yEnd] == '0':
                            return True
                        else:
                            return False
                    else:
                        return False
            elif yStart-1 == yEnd:
                if xStart == xEnd:
                    if board[xEnd][yEnd] == '0':
                        return True
                    else:
                        return False
                elif xStart+1 == xEnd | xStart+1 == xEnd:
                    if board[xEnd][yEnd]!='0':
                        return True
                    else:
                        return False
                else:
                    return False
            else:
                return False
