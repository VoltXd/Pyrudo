import socket
import random

class PyrudoPlayer:

    def __init__(self, player_socket: socket.socket) -> None:
        self.number_of_dices = 5
        self.player_socket = player_socket
        self.is_palifico_done = False
        self.dices = {}
        for i in range(0, 6):
            self.dices[i] = 0
        return

    def __str__(self) -> str:
        string = "{ Player: "
        string += str(self.number_of_dices)
        string += " }"
        return string

    def reset(self) -> None:
        #Reset the changing attributes of the player
        self.number_of_dices = 5
        self.is_palifico_done = False
        return

    def dice_roll(self) -> None:
        #Rolls the dice for the player and prints the result
        for i in range(0, 6):
            self.dices[i] = 0
        for dice in range(self.number_of_dices):
            roll_value = random.randrange(0, 6)
            self.dices[roll_value] += 1
        str_number_of_dice = "Il te reste {} dés ! \n".format(self.number_of_dices)
        str_dices = "Tu as tiré :\n{} Paco(s)\n{} fois 2\n{} fois 3\n{} fois 4\n{} fois 5\n{} fois 6\nBonne chance !\n".format(
            self.dices[0], self.dices[1], self.dices[2], self.dices[3], self.dices[4], self.dices[5])
        self.send_update(str_number_of_dice)
        self.send_update(str_dices)

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
        return "Ok"

    def send_update(self, update: str) -> None:
        # Send updates about the current game's state
        self.player_socket.send(("Update: " + update).encode("utf-8"))
        return

    def send_message(self, message: str) -> None:
        # Send a message for the client to print
        self.player_socket.send(("Msg: " + message).encode("utf-8"))
        return
