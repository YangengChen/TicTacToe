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
