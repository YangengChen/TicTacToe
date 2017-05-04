class Player:

    def __init__(self, name):
        self.name = name
        self.state = 'available'
        self.wins = 0
        self.losses = 0
        self.draws = 0

    def start_game(self, board, piece):
        self.board = board
        self.state = 'busy'
        self.piece = piece
        self.has_turn = (piece == 'X')

    def end_game(self):
        self.board = None
        self.state = 'available'

    def give_turn(self):
        self.has_turn = True

    def place(self, n):
        if (self.has_turn is False):
            raise Exception('Turn is not yours')
        if (n > 9 or n < 1):
            raise Exception('Invalid cell ' + str(n))
        x = n / 3
        y = n % 3
        return self.board.place(self.piece, x, y)
