class GameBoard:
	
	def __init__(self):
		self.board = [['.' for x in range(3)] for y in range(3)]
		
	def place(piece, x, y):
		if (self.board[x][y] != '.'):
			raise Exception('Position already used')
		
		self.board[x][y] = piece
		return __check_win(x, y)
			
		
	def __check_win():
		# Check rows and columns
		for i in range(3):
			if (board[i][0] == board[i][1] and board[i][0] == board[i][2] or
				board[0][i] == board[1][i] and board[0][i] == board[2][i]):
				return board[i][0]
		
		# Check diagonals
		if (board[0][0] == board[1][1] and board[0][0] == board[2][2] or
			board[0][2] == board[1][1] and board[0][2] == board[2][0]):
			return board[0][0]
		
		# No win found
		return None
		
	def to_string():
		display = ''
		for i in range(0, 3):
			for i in range(0, 3):
				display.join(board[i][j])
			display.join('\n')
		return display
		
class Player:
	
	def __init__(self, name):
		self.name = name
		self.state = 'available'
		self.wins = 0
		self.losses = 0
		
	def start_game(board, piece):
		self.state = 'busy'
		self.piece = piece
		self.has_turn = (piece == 'X')
		
	def give_turn():
		self.has_turn = True
		
	def place(n):
		if (self.has_turn is False):
			raise Exception('Turn is not yours')
		if (n > 9 or n < 1):
			raise Exception('Invalid cell ' + str(n))
		
		try:
			winner = board.place(self.piece, x, y)
			if (winner = None):
				
			elif (winner == self.piece):
				win()
			else:
				lose()
				
	def win():
		self.wins += 1
		# print('You Win!\nWins: ' + self.wins + '\nLosses: ' + self.losses)
		return
		
	def lose():
		self.losses += 1
		# print('You Lose!\nWins: ' + self.wins + '\nLosses: ' + self.losses)
		return
			
			
			
			
			
			
			