import socket
import PyrudoReferee
import time
import os

CONNECTION_TIMEOUT = 60
MAX_PLAYERS = 6

number_of_players = 0
players = []

# Opening a socket
socket_address = ("", 8081)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(socket_address)
server_socket.listen()

start = time.time()
end = time.time()

elapsed_time = end - start

if os.name == "nt":
    os.system("cls")
elif os.name == "posix":
    os.system("clear")
else:
    print("\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n\n")

print("******** Serveur Pyrudo ********")
print("En attente d'une première connexion...")

# The game doesn't start until the server has been waiting for a minute or if players can still join
while (elapsed_time < CONNECTION_TIMEOUT and number_of_players < MAX_PLAYERS):
    try:
        client_socket, adrr = server_socket.accept()
        players.append(client_socket)
        if number_of_players == 0:
            start = time.time()
        number_of_players += 1
    except socket.timeout:
        pass
    end = time.time()
    elapsed_time = end - start
    # New socket will have a connection timeout of the remaining connexion time
    server_socket.settimeout(max(CONNECTION_TIMEOUT - elapsed_time, 0))
    # Waiting message for waiting players to keep them busy
    waiting_message = "En attente de connexion... Actuellement {} joueur(s) connecté(s)... {} seconde(s) restante(s)".format(
        len(players), int(CONNECTION_TIMEOUT-elapsed_time))
    for client in players:
        client.send(waiting_message.encode("utf-8"))
    print(elapsed_time)

# A game will start only if player(s) have joined
if len(players) > 0:
    pyrudo_referee = PyrudoReferee.PyrudoReferee(server_socket, players)

    pyrudo_referee.play_game()

    # Closing of the players sockets at the end of the game
    for client in players:
        client.close()

#Closing of the server socket at the end of the game
server_socket.close()