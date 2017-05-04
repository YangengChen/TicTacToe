import GameBoard


class Game:

    def __init__(self, gameid, player1, player2):
        self.gameid = gameid
        self.player1 = player1
        self.player2 = player2
        self.board = GameBoard()
        self.player1.start_game(self.board, 'X')
        self.player2.start_game(self.board, 'O')

    def place(self, playername, n):
        # Check who is trying to place
        if (playername == self.player1.name):
            currplayer = self.player1
            otherplayer = self.player2
        else:
            currplayer = self.player2
            otherplayer = self.player1

        # Check for bad move
        if (currplayer.has_turn is False):
            raise Exception('Turn is not yours')
        if (n < 1 or n > 9):
            raise Exception('Invalid position ' + str(n))

        # Make move and update game state
        x = n / 3
        y = n % 3
        gamestate = self.board.place(self.piece, x, y)

        # Switch turns and notify players of changes
        if (gamestate is None):  # Still playing
            currplayer.remove_turn()
            otherplayer.give_turn()
            currplayer.notify(self.get_board())
            otherplayer.notify(self.get_board())
        elif (gamestate == 'draw'):
            self.end_game(currplayer, otherplayer, True)
        elif (gamestate == currplayer.piece):  # Winner
            self.end_game(currplayer, otherplayer, False)

    def end_game(self, winner, loser, draw):
        # Update player state
        winner.end_game()
        loser.end_game()
        # Notify players of games conclusion
        if (draw):
            winner.notify('The game ends in a draw.')
            loser.notify('The game ends in a draw.')
        else:
            winner.notify('You win.')
            loser.notify('You lose.')

    def get_board(self):
        return self.board.toString()
