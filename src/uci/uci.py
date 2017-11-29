''' See README_UCI for more information on uci protocol and support '''

''' TODO All commands '''
''' supported commands:

    from gui:

        uci: tell engine to use uci

        isready: engine responds with readyok

        ucinewgame: tells engine the next position will be from the start
        position

        go: start calculating the best move

        stop: stop calculating as soon as possible

        quit: quit the program as soon as possible

    to gui:

       'id name' and 'id author': should be sent when uci is recieved

       readyok: when the engine has processed all input and is ready for more

       bestmove <move1>: the engine has found the best move
       o
'''
