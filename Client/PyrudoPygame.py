import socket
import pygame

#TODO: Pygame

def main() -> None:    
    # Connect to server 
    server_address = ("127.0.0.1", 8081)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect(server_address)

    pygame.init()
    window = pygame.display.set_mode((1280, 720))

    # Wait & print message (for testing purpose)

    game_running = True

    while game_running :
        # Inputs/Events
        for event in pygame.event.get():
            if event.type == pygame.QUIT:
                game_running = False
        
        # Update

        # Render

        
        msg = server_socket.recv(4096).decode("utf-8")
        print(msg)
        messages = msg.split("\n")
        for message in messages :
            if message == "Msg: À ton tour !" or message == "Msg: Veuillez choisir une action possible":
                client_input = input("Que souhaites-tu faire ? (Overbid:nb,valeur_de, Dodo, Calza) : ")
                if client_input == "":
                    client_input = "d"
                server_socket.send(client_input.encode("utf-8"))
            elif message == "Update: END":
                game_running = False


    # End connection
    server_socket.close()
    return

if __name__ == "__main__":
    main()