import threading
from Game import Game
from Player import Player
import json
import socketserver
import sys

HOST, PORT = "localhost", 12000

games = []
players = []

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
        self.game_ended = False
        while(1):
            # Accept request from player
            self.input = self.request.recv(1024).decode()
            try:
                # Handle command
                resp = self.handle_command(self.input)
                # Send encoded response to player in json
                if(self.game_ended is True):
                    resp_json = self.encode_json('300 WIN', resp)
                    self.game_ended = False
                else:
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

        elif (commands[0] == 'games'):
            return self.print_games()

        elif (commands[0] == 'who'):
            return self.print_players()

        elif (commands[0] == 'play'):
            return self.play(commands[1])

        elif (commands[0] == 'place'):
            return self.place(commands[1])

        elif (commands[0] == 'update'):
            if (('update ' + self.game.status) != comm or self.game.game_over is True):
                return self.game.status
            else:
                raise Exception('No update')

        elif (commands[0] == 'exit'):
            return 'Exiting TicTacToe...'

        else:
            return help_menu

    # Print list of current games
    def print_games(self):
        gameString = ''
        global games
        for game in games:
            gameString += ('Game Id: ' + str(game.gameid) +
                           '\tPlayer 1: ' + game.player1.name + '\n'
                           '\tPlayer 2: ' + game.player2.name + '\n')
        return gameString

    # Print list of available players
    def print_players(self):
        global players
        avail = 'Available Players: \n'
        for player in players:
            if (player.state == 'available'):
                avail += ('ID: '+ player.name +'\n' +
                '\tWins: '+str(player.wins)+ '\n'+
                '\tLosses: '+str(player.losses)+'\n'+
                '\tDraws: ' + str(player.draws)+'\n')
        return avail

    # Create new player object for new login
    def create_player(self, name):
        for player in players:
            if player.name == name:
                return "Player " + name + " already exists."
        player = Player(name, self)
        players.append(player)
        self.curr_player = player
        return "Logged in as " + name

    # Remove player from records
    def player_exit(self):
        global players
        players.remove(self.curr_player)

    # Challenge player to a game
    def play(self, other_player):
        # Check if player is available
        if any(player.name == other_player and player.state == 'available'
               for player in players):
            player2 = next((player for player in players
                            if player.name == other_player), None)
            # Check if same player, if not start new game
            if self.curr_player is not player2:
                new_game = Game(len(games), self.curr_player, player2)
                games.append(new_game)
                return 'Game started with ' + other_player
            else:
                return 'Cannot start game with same player'
        else:
            return 'Player not available to play'

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
