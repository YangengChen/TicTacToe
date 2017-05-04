import GameBoard
import Player

class Game:

    def __init__(self, player1, player2):
        self.player1 = player1
        self.player2 = player2
        self.board = GameBoard()
        self.player1.start_game(self.board, 'X')
        self.player2.start_game(self.board, 'O')

    def end_game():
        self.player1.end_game()
        self.player2.end_game()

    def get_board():
        return self.board.toString()
