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
    
    def count_dices(self, value):
        #Count how many dices are of the concerned value
        count = 0
        for i in range(self.players_alive):
            if value == 1 :
                count += self.players[i].dict[1]
            else :
                count += self.players[i].dict[value] + self.players[i].dict[1]
        return count
    
    
    def check_message(self,message,player):
        if message == "Dead":
            del self.players_alive[player]
        elif message == "Palifico!":
            self.is_palifico = True
    
    def check_dodo(self, current_bid, current_player, last_player):
        count = self.count_dices(current_bid[1])
        
       #Check who loses the round
        if count < current_bid[0]:
            message = self.players[last_player].lose_round() 
            self.check_message(message, last_player)
        else :
            message = self.players[current_player].lose_round()
            self.check_message(message,current_player)
            
        
    def check_calza(self,current_bid, current_player):
        count = self.count_dices(current_bid[1])
        
        #Check who loses the round
        if count == current_bid[0]:
            self.players[current_player].win_calza()
        else : 
            message = self.players[current_player].lose_round()
            self.check_message(message,current_player)
        
    
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
            current_bid = [0, 0]
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