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
