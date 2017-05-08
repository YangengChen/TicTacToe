from GameBoard import GameBoard


class Game:

    def __init__(self, gameid, player1, player2):
        self.gameid = gameid
        self.game_over = False
        self.player1 = player1
        self.player2 = player2
        self.board = GameBoard()
        self.spectators = []
        self.status = ''
        self.movecount = '0'
        self.player1.tcphandler.game = self
        self.player2.tcphandler.game = self
        self.player1.start_game(self.board, 'X', player2.name)
        self.player2.start_game(self.board, 'O', player1.name)

    # Adds spectator to game
    def add_spectator(self, spectator):
        self.spectators.append(spectator)

    # Remove spectator from game
    def remove_spectator(self, spectator):
        self.spectators.pop(spectator)

    # Attempt to place player's piece at n
    def place(self, player, n):
        # Check who is trying to place
        currplayer = None
        otherplayer = None
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
        x = int((n - 1) / 3)
        y = int((n - (x * 3)) - 1)
        gamestate = self.board.place(currplayer.piece, x, y)

        # Switch turns and notify players of changes
        if (gamestate is None):  # Still playing
            currplayer.remove_turn()
            otherplayer.give_turn()
            self.status = self.board.to_string()
            self.movecount = str(int(self.movecount) + 1)
        else:
            if (gamestate == 'draw'):  # Draw
                self.end_game(currplayer, otherplayer, draw=True)
            elif (gamestate == 'win'):  # Winner
                self.end_game(currplayer, otherplayer)
            self.movecount = '!'  # Complete
        return self.status

    def leave_game(self, leaver):
        if (leaver == self.player1):
            otherplayer = self.player1
        else:
            otherplayer = self.player2
        leaver.end_game()
        otherplayer.end_game()
        self.status = leaver.name + ' has left the game.'
        self.movecount = '!'

    def end_game(self, winner, loser, draw=None):
        # Update player state
        winner.end_game('win')
        loser.end_game('lose')
        # Update game state
        if (draw is None):
            self.status = (self.board.to_string() + winner.name +
                           ' wins the game.')
        else:
            self.status = self.board.to_string() + 'The game ends in a draw.'
