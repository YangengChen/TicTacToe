from threading import Thread
import Game
import Player
import socketserver
import sys

HOST, PORT = "localhost", 12000
mode = ''

games = []
available_players = []
busy_players = []

help_menu = 'login [name]       Log into TicTacToe with username <name>\n' +
            'place [1-9]        Place piece on box <1-9> during your turn\n' +
            'exit               Exits TicTacToe ending current game\n' + 
            'games              Display list of ongoing games and info\n' +
            'who                Display list of available players\n' +
            'play [name]        Challenge player <name>\n' +
            'observe [gameid]   Observe game <gameid>\n' +
            'unobserve [gameid] Stop observing game <gameid>'

class GameTCPHandler(socketserver.BaseRequestHandler):

    # Handler for connection request to server
    def handle(self):
        self.input = self.request.recv(1024).strip()
        response = handle_command(self.input)
        if (response is not None):
            self.request.sendall(response)

    def handle_command(comm):
    	commands = comm.split(" ")
    	if(commands[0] == 'login'):
    		create_player(commands[1])

        if (commands[0] == 'games'):
        	return print_games()

        elif (commands[0] == 'who'):
        	avail = ', '.join(names)
        	return avail;

        elif (commands[0] == 'play'):
        	#implement play
        else:
        	return help()

    def print_games():
    	gameString = '';
    	for game in games:
    		gameString += 'Game Id: '+
    		 				'\tPlayer 1: '+game.player1.name+'\n'
    		 				'\tPlayer 2: '+game.player2.name+'\n'

    	return gameString

    def create_player(name):
    	player = Player(name)
    	available_players.append(player)


	def help():
    	return print(help_menu)

    def play(other_player):
    	if any(player.name == other_player for player in available_players)
    		player2 = next((player for player in available_players if player.name == other_player), None)
    		new_game = Game


    	else:
    		return 'Player not available to play'




    def notify_player(msg):
        self.request.sendall(msg)


def __exit(code):
    if (code == 1):
        print_usage()
    exit(code)


if __name__ == '__main__':
    mode = ''.join(sys.argv[1])
    
    # Check for bad args
    if (mode != 'single' and mode != 'multiple'):
        __exit(1)

    # Create server and loop
    server = sockeserver.TCPServer((HOST, PORT), GameTCPHandler)
    server.serve_forever()
