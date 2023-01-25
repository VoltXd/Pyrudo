import socket
import PyrudoReferee

# Opening a socket
socket_address = ("", 8081)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.bind(socket_address)
server_socket.listen()

# For testing puspose only
s1, a1 = server_socket.accept()
s2, a2 = server_socket.accept()
pyrudo_referee = PyrudoReferee.PyrudoReferee(server_socket, [s1, s2])
pyrudo_referee.play_game()

# Closing the socket
server_socket.close()