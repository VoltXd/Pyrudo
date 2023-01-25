import socket

class PyrudoPlayer:

    def __init__(self, player_socket: socket.socket) -> None:
        self.number_of_dices = 5
        self.player_socket = player_socket
        self.is_palifico_done = False
        return

    def __str__(self) -> str:
        string = "{ Player: "
        string += str(self.number_of_dices)
        string += " }"
        return string

    def reset(self) -> None:
        self.number_of_dices = 5
        self.is_palifico_done = False
        return

    def lose_round(self) -> str:
        # If round lost, withdraw a dice
        self.number_of_dices -= 1

        # Palifico, round lost, or continue
        if self.number_of_dices == 1 and not self.is_palifico_done:
            return "Palifico!"
        elif self.number_of_dices == 0:
            return "Dead"
        else: 
            return "Ok"

    def win_calza(self) -> None:
        # Calza won => get one dice back
        if self.number_of_dices < 5:
            self.number_of_dices += 1
        return
    
    def send_update(self, update: str) -> None:
        # Send updates about the current game's state
        self.player_socket.send(("update:" + update).encode("utf-8"))
        return
    
    def send_message(self, message: str) -> None:
        # Send a message for the client to print
        self.player_socket.send(("msg:" + message).encode("utf-8"))
        return
