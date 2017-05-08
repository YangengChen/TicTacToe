from socket import *
import json
import sys
from time import sleep

usage = 'Usage:\npython GameClient.py [host] [port]'

clientSocket = None
movecount = ''


def place(command):
    # Send place request
    global clientSocket
    clientSocket.send((command[0] + ' ' + command[1]).encode())
    resp = clientSocket.recv(1024).decode()
    resp_json = json.loads(resp)
    print(resp_json['content'][2:])
    if (resp_json['status'] == '400 ERROR'):
        return
    global movecount
    movecount = resp_json['content'][0:1]
    if (movecount == '!'):
        return

    # Continue to send for opponent's move or game end
    while (1):
        sleep(1)
        clientSocket.send(('update ' + movecount).encode())
        update = clientSocket.recv(1024).decode()
        update_json = json.loads(update)
        content = update_json['content']
        # Check if board has changed
        if (update_json['status'] == '200 OK'):
            print(content[2:])
            movecount = content[0:1]
            return


def check_command(command):
    command = command.split()
    if len(command) == 1:
        if command[0] == "help":
            return True
        elif command[0] == "exit":
            return True
    elif len(command) == 2:
        if command[0] == "login":
            return True
        elif command[0] == "place":
            place(command)
            return False
    print('Unsupported command.')
    return False


def main(argv):
    if (len(argv) != 3):
        print(usage)
        return 1

    host = argv[1]
    port = int(argv[2])
    global clientSocket, lfg_thread, ingame, lfg
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((host, port))

    while(1):
        command = input('ttt> ')
        # Check if command can be handled with one message to server
        if (check_command(command)):
            clientSocket.send(command.encode())
            response = clientSocket.recv(1024)
            responseObj = json.loads(response.decode())
            print(responseObj['content'])
            if (command == 'exit'):
                break
    return 0


if __name__ == '__main__':
    main(sys.argv)
