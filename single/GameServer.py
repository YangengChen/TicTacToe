import threading
from Game import Game
from Player import Player
import json
import socketserver
import sys

HOST, PORT = "localhost", 12000

game = None
players = []

help_menu = ('login [name]       Log into TicTacToe with username <name>\n'
             'place [1-9]        Place piece on box <1-9> during your turn\n'
             'exit               Exits TicTacToe ending current game\n'

usage = 'Usage:\npython GameServer.py [single, multiple]'


class ThreadedTCPServer(socketserver.ThreadingMixIn, socketserver.TCPServer):
    pass


class GameTCPHandler(socketserver.BaseRequestHandler):

    # Handler for connection request to server
    def handle(self):
        self.game_ended = False
        while(1):
            # Accept request from player
            self.input = self.request.recv(1024).decode()
            try:
                # Handle command
                resp = self.handle_command(self.input)
                # Send encoded response to player in json
                resp_json = self.encode_json('200 OK', resp)
                self.request.sendall(resp_json.encode())
                if (resp == 'Exiting TicTacToe...'):
                    break
            except Exception as msg:
                # Something went wrong, send error message to player
                err_json = self.encode_json('400 ERROR', str(msg.args))
                self.request.sendall(err_json.encode())
        # Player exiting
        self.player_exit()
        return 0

    # Checks input and calls related functionality
    def handle_command(self, comm):
        commands = comm.split(" ")
        if(commands[0] == 'login'):
            return self.create_player(commands[1])

        elif (commands[0] == 'place'):
            return self.place(commands[1])

        elif (commands[0] == 'update'):
            if (('update ' + self.game.status) != comm or
                self.game.game_over is True):
                return self.game.status
            else:
                raise Exception('No update')

        elif (commands[0] == 'exit'):
            return 'Exiting TicTacToe...'

        else:
            return help_menu

    # Create new player object for new login
    def create_player(self, name):
        global players
        if ('curr_player' in self and self.curr_player is not None):
            return "Already logged in as " + self.curr_player.name
        if (len(players) == 2):
            return 'Server can only accept two players'
        for player in players:
            if player.name == name:
                return "Player " + name + " already exists."
        player = Player(name, self)
        players.append(player)
        self.curr_player = player

        # Start new game
        if (len(players) == 2):
            global game
            game = Game(0, self.curr_player, players[0])
            return 'Game started with ' + players[0].name
        else:
            return 'Waiting for additional player...'

    # Remove player from records
    def player_exit(self):
        global players
        players.remove(self.curr_player)

    # Attempt to place piece at location n
    def place(self, n):
        return self.game.place(self.curr_player, n)

    # Encode the response to player in json
    def encode_json(self, status, content):
        obj = {'status': status, 'content': content}
        return json.dumps(obj)


def main(argv):
    if (len(argv) != 2):
        print(usage)
        return 1

    # Create server and loop
    server = ThreadedTCPServer((HOST, PORT), GameTCPHandler)
    server_thread = threading.Thread(target=server.serve_forever)
    server_thread.start()


if __name__ == '__main__':
    main(sys.argv)
