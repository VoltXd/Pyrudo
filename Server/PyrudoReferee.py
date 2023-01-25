import PyrudoPlayer
import socket
import random

class PyrudoReferee:

    DICE_FACES = {1: "Paco", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6"}
    PLAYER_CHOICES = { "Overbid", "Dodo", "Calza" }

    def __init__(self, server_socket, clients_sockets) -> None:
        self.players = []
        for i in range(len(clients_sockets)):
            self.players.append(PyrudoPlayer.PyrudoPlayer(clients_sockets[i]))

        self.server_socket = server_socket
        return

    def play_game(self) -> None:
        # Initialize players and variables
        players_alive = []
        for i in range(len(self.players)):
            self.players[i].reset()
            players_alive.append(i)
        is_game_finished = False

        # Start the game, run until game is finished
        while not is_game_finished:
            # Initialize the next round
            current_player_index = random.randrange(len(players_alive))
            current_bid = (0, 0)
            is_round_finished = False
            is_palifico = False

            # Start a round, run until round is finished 
            while not is_round_finished:
                # Round begin messages
                self.players[current_player_index].send_message("À ton tour !\n")
                for i in [x for x in range(len(self.players)) if x != current_player_index]:
                    self.players[i].send_message("C'est au tour de {}\n".format(current_player_index))

                #TODO: Wait for auction
                # Verify auction (wrong player ? wrong auction ?)
                # If good auction:
                #     Bid, Dodo, calza
                #     End round

                # Test
                is_game_finished = True
                is_round_finished = True

        
        return

if __name__ == "__main__":
    print(PyrudoReferee.DICE_FACES)