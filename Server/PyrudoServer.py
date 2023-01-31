import socket
import PyrudoReferee
import time

CONNECTION_TIMEOUT = 10
MAX_PLAYERS = 6

number_of_players = 0
players = []

# Opening a socket
socket_address = ("", 8081)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.settimeout(10)
server_socket.bind(socket_address)
server_socket.listen()

start = time.time()
end = time.time()

elapsed_time = end - start

while (elapsed_time < CONNECTION_TIMEOUT and number_of_players < MAX_PLAYERS):
    try:
        client_socket, adrr = server_socket.accept()
        players.append(client_socket)
        number_of_players += 1
    except socket.timeout:
        pass
    end = time.time()
    elapsed_time = end - start
    waiting_message = "En attente de connexion... Actuellement {} joueur(s) connecté(s)... {} seconde(s) restante(s)".format(
        len(players), int(CONNECTION_TIMEOUT-elapsed_time))
    for client in players:
        client.send(waiting_message.encode("utf-8"))
    print(elapsed_time)

pyrudo_referee = PyrudoReferee.PyrudoReferee(server_socket, players)

pyrudo_referee.play_game()

for client in players:
    client.close()

server_socket.close()
# For testing puspose only
# s1, a1 = server_socket.accept()
# s2, a2 = server_socket.accept()

# pyrudo_referee = PyrudoReferee.PyrudoReferee(server_socket, [s1, s2])


# Closing the socket
# s1.close()
# s2.close()
