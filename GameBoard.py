class GameBoard:
    def __init__(self):
        self.board = [['.' for x in range(3)] for y in range(3)]

    def place(self, piece, x, y):
        if (self.board[x][y] != '.'):
            raise Exception('Position already used')

        self.board[x][y] = piece
        return self.check_win()

    def check_win(self):
        # Check rows and columns
        for i in range(3):
            if (self.board[i][0] == self.board[i][1] and
                self.board[i][0] == self.board[i][2] or
                self.board[0][i] == self.board[1][i] and
                self.board[0][i] == self.board[2][i]):
                return self.board[i][0]

        # Check diagonals
        if (self.board[0][0] == self.board[1][1] and
            self.board[0][0] == self.board[2][2] or
            self.board[0][2] == self.board[1][1] and
            self.board[0][2] == self.board[2][0]):
            return self.board[0][0]

        # Check draw
        for i in range(3):
            for j in range(3):
                if (self.board[i][j] != '.'):
                    return None

        # Draw found
        return 'draw'

    def to_string(self):
        display = ''
        for i in range(0, 3):
            for j in range(0, 3):
                display.join(self.board[i][j])
                display.join('\n')
        return display
