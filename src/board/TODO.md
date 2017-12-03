# Board TODO #

Allow for moves to be made

Output fen representation of current board

Currently many features are half implemented. The following are incomplete

* Fen only imports position, not board state such as current player

Code is hacky and not well thought out. Needs to be restructured and
documented

Proper testing framework

* Currently a python script is used and edited by hand every time the code is
  changed.

# What is implemented? #

All legal moves can be generated. This appears to be implemented correctly, but
more testing is required

The board position can be read from an fen string, but not the rest of the
string (current player, castling availablity, en passant, move counter). This
has been tested.

# Features that need to be tested #

Test move generation

Test algebriac conversion

Test fen import
