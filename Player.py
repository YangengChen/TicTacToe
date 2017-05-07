class Player:

    def __init__(self, name, tcphandler):
        self.name = name
        self.tcphandler = tcphandler
        self.state = 'available'
        self.wins = 0
        self.losses = 0
        self.draws = 0

    # Set player state to new game
    def start_game(self, board, piece, opponentname):
        self.state = 'busy'
        self.board = board
        self.piece = piece
        self.has_turn = (piece == 'X')

    # Set player state to no game
    def end_game(self, outcome):
        self.board = None
        self.state = 'available'
        if outcome == "win":
            self.wins += 1
        elif outcome == "lose":
            self.losses += 1
        else:
            self.draws += 1

    # Set player as having turn
    def give_turn(self):
        self.has_turn = True

    # Set player as finished turn
    def remove_turn(self):
        self.has_turn = False

    # Send message to player
    def notify(self, msg):
        self.tcphandler.notify_player(msg)
