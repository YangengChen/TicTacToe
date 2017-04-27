import GameBoard
import Player

help_menu = 'login [name]       Log into TicTacToe with username <name>\n' +
            'place [1-9]        Place piece on box <1-9> during your turn\n' +
            'exit               Exits TicTacToe ending current game\n' + 
            'games              Display list of ongoing games and info\n' +
            'who                Display list of available players\n' +
            'play [name]        Challenge player <name>\n' +
            'observe [gameid]   Observe game <gameid>\n' +
            'unobserve [gameid] Stop observing game <gameid>'


def help():
    return print(help_menu)


def 
