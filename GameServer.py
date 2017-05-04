from threading import Thread
import socketserver
import sys

HOST, PORT = "localhost", 12000
mode = ''

games = []
available_players = []
busy_players = []

class GameTCPHandler(socketserver.BaseRequestHandler):

    # Handler for connection request to server
    def handle(self):
        self.input = self.request.recv(1024).strip()
        response = handle_command(self.input)
        if (response is not None):
            self.request.sendall(response)

    def handle_command(comm):
        if (comm == 'games'):
        elif (comm == 'who'):
        elif (comm == 'play'):
        else:


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
