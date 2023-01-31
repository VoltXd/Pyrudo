import socket

# Connect to server 
server_address = ("127.0.0.1", 8081)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.connect(server_address)

# Wait & print message (for testing purpose)

game_running = True
is_full_message = False

while game_running :
    msg = server_socket.recv(4096).decode("utf-8")
    print(msg)
    messages = msg.split("\n")
    for message in messages :
        if message == "Msg: À ton tour !" or message == "Msg: Veuillez choisir une action possible":
            client_input = input("Que souhaites-tu faire ? (Overbid:nb,valeur_de, Dodo, Calza) : ")
            if client_input == "":
                client_input = "d"
            server_socket.send(client_input.encode("utf-8"))


# End connection
server_socket.close()