from socket import *
import json
import sys
from time import sleep

usage = 'Usage:\npython GameClient.py [host] [port]'

clientSocket = None


def print_resp(resp_json):
    print('Status: ' + resp_json['status'] + '\n' +
          'Server: ' + resp_json['content'])


def place(command):
    # Send place request
    global clientSocket
    clientSocket.send((command[0] + ' ' + command[1]).encode())
    resp = clientSocket.recv(1024).decode()
    resp_json = json.loads(resp)
    print_resp(resp_json)
    if (resp_json['status'] == 'ERROR'):
        return

    # Continue to send for opponent's move or game end
    while (1):
        sleep(1)
        clientSocket.send(('update').encode())
        update = clientSocket.recv(1024).decode()
        update_json = json.loads(update)
        # Check if board has changed
        if (update_json['status'] == 'OK'):
            print(update_json['content'])
            return


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
            place(command)
            return False
        elif command[0] == "play":
            return True
        elif command[0] == "observe":
            return False
        elif command[0] == "unobserve":
            return True
    print('Unsupported command.')
    return False


def main(argv):
    if (len(argv) != 3):
        print(usage)
        return 1

    host = argv[1]
    port = int(argv[2])
    global clientSocket
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((host, port))

    while(1):
        command = input('ttt> ')
        # Check if command can be handled with one message to server
        if (check_command(command)):
            clientSocket.send(command.encode())
            response = clientSocket.recv(1024)
            responseObj = json.loads(response.decode())
            print("Status: " + responseObj['status'] + '\n' +
                  "Server: " + responseObj['content'])
            if (command == 'exit'):
                break
    return 0


if __name__ == '__main__':
    main(sys.argv)
