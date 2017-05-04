#from threading import Thread
import threading
from Game import Game
from Player import Player
import json
import socketserver
import sys

HOST, PORT = "localhost", 12000

games = []
available_players = []
busy_players = []

help_menu = ('login [name]       Log into TicTacToe with username <name>\n'
             'place [1-9]        Place piece on box <1-9> during your turn\n'
             'exit               Exits TicTacToe ending current game\n'
             'games              Display list of ongoing games and info\n'
             'who                Display list of available players\n'
             'play [name]        Challenge player <name>\n'
             'observe [gameid]   Observe game <gameid>\n'
             'unobserve [gameid] Stop observing game <gameid>')

usage = 'Usage:\npython GameServer.py [single, multiple]'

class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass

class GameTCPHandler(socketserver.BaseRequestHandler):

    # Handler for connection request to server
    def handle(self):
        print('START');
        while(1):
            self.input = self.request.recv(1024).decode().strip()
            #self.request.sendall(('200 OK').encode())
            try:
                resp = self.handle_command(self.input)
                jsonStr = self.encode_json('200 OK', resp)
                self.request.sendall(jsonStr.encode())
                print('GOOD SHIT')
            except Exception as msg:
                print('BAD SHIT')
                err_json = self.encode_json('400 ERROR', msg.args[0])
                self.request.sendall(err_json.encode())

    def handle_command(self, comm):
        commands = comm.split(" ")
        if(commands[0] == 'login'):
            self.create_player(commands[1])
            return 'Logged in as ' + commands[1]

        elif (commands[0] == 'games'):
            return self.print_games()

        elif (commands[0] == 'who'):
            global available_players
            avail = ''
            for player in available_players:
                avail = avail.join(player.name + ' ')
            return avail

        elif (commands[0] == 'play'):
            return self.play(commands[1])

        elif (commands[0] == 'place'):
            self.place(commands[1])

        else:
            return help()

    def print_games(self):
        gameString = ''
        for game in games:
            gameString += ('Game Id: ' + self.game.gameid +
                           '\tPlayer 1: ' + game.player1.name + '\n'
                           '\tPlayer 2: ' + game.player2.name + '\n')

        return gameString

    def create_player(self,name):
        player = Player(name,self)
        available_players.append(player)
        self.curr_player = player

    def help():
        print(help_menu)

    def play(self, other_player):
        if any(player.name == other_player for player in available_players):
            player2 = next((player for player in available_players
                            if player.name == other_player), None)
            new_game = Game(len(games), self.curr_player, player2)
            games.append(new_game)
            self.game = new_game
        else:
            return 'Player not available to play'

    def place(self, n):
        self.game.place(self.curr_player, n)

    def notify_player(self, msg):
        self.request.sendall(msg)

    def encode_json(self, status, content):
        obj = {'status': status, 'content': content}
        return json.dumps(obj)



def __exit(code):
    if (code == 1):
        print(help_menu)
    exit(code)

def main(argv):
    if (len(argv) != 2):
        print(usage)
        return 1

    # Create server and loop
    #server = socketserver.TCPServer((HOST, PORT), GameTCPHandler)
    #server.serve_forever()
    server = ThreadedTCPServer((HOST, PORT), GameTCPHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()

if __name__ == '__main__':
    main(sys.argv)
