import socket

# Connects to server
server_address = ("127.0.0.1", 8081)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.connect(server_address)


game_running = True

while game_running:
    msg = server_socket.recv(4096).decode("utf-8")
    print(msg)
    # Impossible to receive a message at a time with the TCP protocol
    # --> necessity to split the received "message" with the new line character
    messages = msg.split("\n")
    for message in messages:
        # Does the received message require an input from the client?
        if message == "Msg: À ton tour !" or message == "Msg: Veuillez choisir une action possible":
            client_input = input(
                "Que souhaites-tu faire ? (Overbid:nb,valeur_de, Dodo, Calza) : ")
            if client_input == "":
                client_input = "d"
            server_socket.send(client_input.encode("utf-8"))
        # Checks if the game is over
        elif message == "Update: END":
            game_running = False


# End connection
server_socket.close()
