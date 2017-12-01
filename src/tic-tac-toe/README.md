# Tic Tac Toe #

'Why is there a complete tic tac toe implentation inside of a chess program?'
you ask. I may change my mind later, but for now my reasoning is thus:

1. Tic Tac Toe has a few similarities to chess:

    a. Sum Zero: If one player wins the other loses. This allows for mini-max
    to solve both tic tac toe and chess, given unlimited time and space.

    b. Simple children's game: Both are easy to understand, and program.

2. Analyzing positions is super easy in tic tac toe. I once wrote a java
   program that could solve the game through brute force in under 10 seconds.
   Many positions in chess are impossible to analyze completely.
