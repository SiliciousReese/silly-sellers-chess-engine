# Chess Design #

I will use this document to help brainstorm the design of a chess engine

# Misc #

* Uci: standard engine interface. In the short term we should hack together a
  minimal engine, possibly picking random legal moves. It may allow better
  debugging.

* tic tac toe: Sample min max algorithm. Good practice

# Engine position analyses #

* minimax

* alpha beta pruning

## Static position analyses ## 

Point value: 

* Pawn = 1

* Knight and bishop = 3 

* Rook = 5

* Queen = 9

* K = infinite

    * It probably shouldn't be possible to analyze a king-less position. The
      engine should stop using static analyses befor mate in 1.

Positional elements:

* Pieces in center

* Bishop pair

* doubled pawns

* Pawn structure

* King safety

* mobility

* center control

# Board #

## Intuitive Board Representation ##

Pieces

* Empty location: 0

* Pawn: 1

* Knight: 2

* ..

* King: 6

* Unused: 7

8 x 8 grid

boolean for queen-side and king-side castling 

* 4 booleans total, 2 for each side

en pessant (0 - 7)

total bits (8 * 8 * 3) + 2 + 3 bits used

* 64 states unused due to unused board location state

# Calculation Moves #

Simple Brute force algorithm

general movement rules:

* Can't leave king in check

* Can't move through other pieces (except knights)

* Can capture opponents pieces

Pawn movement:

* en pessant

* 1 forward, 2 forward at start

* Capture only on diagonal

* can promote to other pieces

King movement: 

* Can't move into check

* Castle

    * Can't castle through or out of check

    * Can't castle after rook or king move

* can move 1 in any direction
