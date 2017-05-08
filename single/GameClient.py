from socket import *
import json
import sys
from time import sleep

usage = 'Usage:\npython GameClient.py [host] [port]'

clientSocket = None
movecount = ''


def communicate(message):
    global clientSocket
    clientSocket.send(message.encode())
    resp = clientSocket.recv(1024).decode()
    return json.loads(resp)


def update():
    global movecount
    # Continue to send for opponent's move or game end
    while (1):
        sleep(1)
        update_json = communicate('update ' + movecount)
        content = update_json['content']
        # Check if board has changed
        if (update_json['status'] == '200 OK'):
            print(content[2:])
            movecount = content[0:1]
            return


def place(command):
    # Send place request
    resp_json = communicate(command[0] + ' ' + command[1])
    print(resp_json['content'][2:])
    if (resp_json['status'] == '400 ERROR'):
        return
    global movecount
    movecount = resp_json['content'][0:1]
    if (movecount == '!'):
        return
    # Check for updates
    update()


def login(command):
    resp_json = communicate(command[0] + ' ' + command[1])
    print(resp_json['content'])
    if (resp_json['content'][0:1] == 'G'):
        return

    while (1):
        sleep(1)
        meet_json = communicate('meet')
        # Check if additional player logged in
        if (meet_json['status'] == '200 OK'):
            print(meet_json['content'])
            update()
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
            login(command)
            return False
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
    global clientSocket
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((host, port))

    while(1):
        command = input('ttt> ')
        # Check if command can be handled with one message to server
        if (check_command(command)):
            resp_json = communicate(command)
            print(resp_json['content'])
            if (command == 'exit'):
                break
    return 0


if __name__ == '__main__':
    main(sys.argv)
