from socket import *
import json
import sys
from time import sleep

usage = 'Usage:\npython GameClient.py [host] [port]'

clientSocket = None
gamestatus = ''


def print_resp(resp_json):
    print(resp_json['content'])


def observe(command):
    global clientSocket, gamestatus
    while (1):
        sleep(0.5)
        clientSocket.send(('observe ' + command[1] + ' ' + gamestatus).encode())
        update = clientSocket.recv(1024).decode()
        update_json = json.loads(update)
        # Check if board has changed
        if (update_json['status'] == '200 OK'):
            print(update_json['content'])
            gamestatus = update_json['content']
        elif (update_json['status'] == '300 WIN'):
            return
        else:
            print(update_json['content'])
            return


def place(command):
    # Send place request
    global clientSocket
    clientSocket.send((command[0] + ' ' + command[1]).encode())
    resp = clientSocket.recv(1024).decode()
    resp_json = json.loads(resp)
    print_resp(resp_json)
    if (resp_json['status'] == '400 ERROR'):
        return
    global gamestatus
    gamestatus = resp_json['content']

    # Continue to send for opponent's move or game end
    while (1):
        sleep(1)
        clientSocket.send(('update ' + gamestatus).encode())
        update = clientSocket.recv(1024).decode()
        update_json = json.loads(update)
        # Check if board has changed
        if (update_json['status'] == '200 OK'):
            print(update_json['content'])
            gamestatus = update_json['content']
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
            observe(command)
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
