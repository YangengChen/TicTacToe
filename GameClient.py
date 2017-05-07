from socket import *
import json
import sys

usage = 'Usage:\npython GameClient.py [host] [port]'


def check_command(command):
    command = command.split()
    if len(command) == 1:
        if command[0] == "help":
            return True
        elif command[0] == "games":
            return True
        elif command[0] == "who":
            return True
        elif command[0] == "exit":
            return True
    elif len(command) == 2:
        if command[0] == "login":
            return True
        elif command[0] == "place":
            return True
        elif command[0] == "play":
            return True
        elif command[0] == "observe":
            return True
        elif command[0] == "unobserve":
            return True
    return False


def main(argv):
    if (len(argv) != 3):
        print(usage)
        return 1

    host = argv[1]
    port = int(argv[2])
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((host, port))

    while(1):
        command = input('ttt> ')
        if (check_command(command)):
            clientSocket.send(command.encode())
            response = clientSocket.recv(1024)
            responseObj = json.loads(response.decode())
            print("Status: " + responseObj['status'])
            print("Server: " + responseObj['content'])
            if (command == 'exit'):
                break
        else:
            print('Unsupported command.')
    return 0


if __name__ == '__main__':
    main(sys.argv)
