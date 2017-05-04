import GameBoard


class Game:

    def __init__(self, gameid, player1, player2):
        self.gameid = gameid
        self.player1 = player1
        self.player2 = player2
        self.board = GameBoard()
        self.spectators = []
        self.player1.start_game(self.board, 'X', player2.name)
        self.player2.start_game(self.board, 'O', player1.name)

    def add_spectator(self, spectator):
        self.spectators.append(spectator)

    def remove_spectator(self, spectator):
        self.spectators.pop(spectator)

    def place(self, player, n):
        # Check who is trying to place
        if (player == self.player1):
            currplayer = self.player1
            otherplayer = self.player2
        else:
            currplayer = self.player2
            otherplayer = self.player1

        # Check for bad move
        if (currplayer.has_turn is False):
            raise Exception('Turn is not yours')
        n = int(n)
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
            self.notify_all()
        elif (gamestate == 'draw'):
            self.end_game(currplayer, otherplayer, draw=True)
        elif (gamestate == currplayer.piece):  # Winner
            self.end_game(currplayer, otherplayer)

    def notify_all(self, msg=None):
        if (msg is None):
            msg = self.get_board()
        for spectator in self.spectators:
            spectator.notify(msg)
        self.player1.notify(msg)
        self.player2.notify(msg)

    def leave_game(self, leaver):
        if (leaver == self.player1):
            otherplayer = self.player1
        else:
            otherplayer = self.player2
        leaver.end_game()
        otherplayer.end_game()
        self.notify_all(leaver.name + ' has left the game.')

    def end_game(self, winner, loser, draw=None):
        # Update player state
        winner.end_game()
        loser.end_game()
        # Notify players of games conclusion
        if (draw is not None):
            winner.notify('The game ends in a draw.')
            loser.notify('The game ends in a draw.')
        else:
            winner.notify('You win.')
            loser.notify('You lose.')

    def get_board(self):
        return self.board.toString()
