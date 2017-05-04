class Player:

    def __init__(self, name, tcphandler):
        self.name = name
        self.tcphandler = tcphandler
        self.state = 'available'
        self.wins = 0
        self.losses = 0
        self.draws = 0

    def start_game(self, piece, opponentname):
        self.state = 'busy'
        self.piece = piece
        self.has_turn = (piece == 'X')
        self.notify('Starting game against ' + opponentname)

    def end_game(self):
        self.board = None
        self.state = 'available'

    def give_turn(self):
        self.has_turn = True

    def remove_turn(self):
        self.has_turn = False

    def notify(self, msg):
        self.tcphandler.notify_player(msg)
