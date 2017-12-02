# Board TODO #

Currently many features are half implemented. The following are incomplete

* Fen only imports position, not board state such as current player

* Only white pawns have move generation

Code is hacky and not well thought out. Needs to be restructured and
documented

Piece move generation is started.

* White pawn movement is implemented and tested

* Black pawn movement needs to be tested

* No other pieces have been implemented

Proper testing framework

* Currently a python script is used and edited by hand every time the code is
  changed.

# What is implemented? #

Currently white pawn movement generation (ignoring pins and en passant) has
been tested to work correctly.

The board position can be read from an fen string, but not the rest of the
string (current player, castling availablity, en passant, move counter). This
has been tested.
