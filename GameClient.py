from socket import *
import sys

help_menu = ("login [name]       Log into TicTacToe with username <name>\n"
             "place [1-9]        Place piece on box <1-9> during your turn\n"
             "exit               Exits TicTacToe ending current game\n"
             "games              Display list of ongoing games and info\n"
             "who                Display list of available players\n"
             "play [name]        Challenge player <name>\n"
             "observe [gameid]   Observe game <gameid>\n"
             "unobserve [gameid] Stop observing game <gameid>")


def print_help():
    print(help_menu)


def login(name):
    clientSocket.send("login " + name)
    response = clientSocket.recv(1024)
    print("Server: "+response)


def place(pos):
    clientSocket.send("place " + pos)
    response = clientSocket.recv(1024)
    print("Server: "+response)


def games():
    clientSocket.send("games")
    response = clientSocket.recv(1024)
    print("Server: "+response)


def who():
    clientSocket.send("who")
    response = clientSocket.recv(1024)
    print("Server: "+response)


def play(name):
    clientSocket.send("play " + name)
    response = clientSocket.recv(1024)
    print("Server: "+response)


def observe(gameID):
    clientSocket.send("observe " + gameID)
    response = clientSocket.recv(1024)
    print("Server: "+response)


def unobserve(gameID):
    clientSocket.send("unobserve " + gameID)
    response = clientSocket.recv(1024)
    print("Server: "+response)


def exit_server():
    clientSocket.send("exit")
    response = clientSocket.recv(1024)
    print("Server: "+response)
    exit()


def check_command(command):
    command = command.split()
    if len(command) == 1:
        if command[0] == "help":
            print_help()
        elif command[0] == "games":
            games()
        elif command[0] == "who":
            who()
        elif command[0] == "exit":
            exit_server()
        else:
            print("Unsupported command")
    elif len(command) == 2:
        if command[0] == "login":
            login(command[1])
        elif command[0] == "place":
            place(command[1])
        elif command[0] == "play":
            play(command[1])
        elif command[0] == "observe":
            observe(command[1])
        elif command[0] == "unobserve":
            unobserve(command[1])
        else:
            print("Unsupported command")
    else:
        print("Unsupported command")


def main(argv):
    if (len(argv) != 3):
        print_help()
        return 1

    host = argv[1]
    port = int(argv[2])
    clientSocket = socket(AF_INET, SOCK_STREAM)
    clientSocket.connect((host, port))

    while(1):
        command = raw_input("Enter a command: ")
        check_command(command)
    return 0


if __name__ == '__main__':
    main(sys.argv)
