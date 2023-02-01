import PyrudoPlayer
import socket
import random
import time
import os


class PyrudoReferee:

    DICE_FACES = {1: "Paco", 2: "2", 3: "3", 4: "4", 5: "5", 6: "6"}
    PLAYER_CHOICES = {"Overbid", "Dodo", "Calza"}

    def __init__(self, server_socket, clients_sockets) -> None:
        self.players = []
        for i in range(len(clients_sockets)):
            self.players.append(PyrudoPlayer.PyrudoPlayer(clients_sockets[i]))

        self.server_socket = server_socket
        self.players_alive = []
        return

    def next_player(self, current_player):
        # Determines the next player to play
        if (current_player != self.players_alive[-1]):
            idx = self.players_alive.index(current_player) + 1
            while idx not in self.players_alive:
                idx += 1
            return idx
        else:
            return self.players_alive[0]

    def count_dices(self, value):
        # Counts how many dices are of the concerned value
        count = 0
        for i in range(len(self.players_alive)):
            if value == 1:
                count += self.players[i].dices[0]
            # Paco counts as any other value
            else:
                count += self.players[i].dices[value] + \
                    self.players[i].dices[0]
        return count

    def check_status(self, status, player):
        # Action depending on the status of the game at the end of the round
        if status == "Dead":
            del self.players_alive[player]
            self.dead_message(player)
        elif status == "Palifico!":
            self.is_palifico = True
            # Everyone is updated that the game is in a palifico state
            palifico_msg = "Nous sommes en Palifico ! Rappel : vous ne pouvez que surenchérir sur le nombre de dés, la valeur du dé reste identique !"
            for i in [x for x in range(len(self.players))]:
                self.players[i].send_update(palifico_msg)
            time.sleep(0.5)
        return

    def check_dodo(self, current_bid, current_player, last_player):
        count = self.count_dices(current_bid[1])
        losing_player = -1

       # Checks who loses the round
        if count < current_bid[0]:
            # Dodo player was right !
            status = self.players[last_player].lose_round()
            if status == "Dead":
                # Who's next player if last bidder is dead
                losing_player = self.next_player(last_player)
            else:
                losing_player = last_player
            # Update of the game state regarding last bidder current state
            self.check_status(status, last_player)
            self.end_round_message(current_player, current_bid, count, True)
        else:
            # Dodo player was wrong !
            status = self.players[current_player].lose_round()
            if status == "Dead":
                # Who's next player if Dodo player is dead
                losing_player = self.next_player(current_player)
            else:
                losing_player = current_player
            # Update of the game state regarding Dodo player current state
            self.check_status(status, current_player)
            self.end_round_message(current_player, current_bid, count, False)
        self.is_round_finished = True
        return losing_player

    def check_calza(self, current_bid, current_player):
        count = self.count_dices(current_bid[1])

        # Checks who loses the round
        if count == self.current_bid[0]:
            # Calza won!
            self.players[current_player].win_calza()
            self.end_round_message(current_player, current_bid, count, True)
        else:
            # Calza lost!
            status = self.players[current_player].lose_round()
            # Update of the game state regarding Calza player current state
            self.check_status(status, current_player)
            self.end_round_message(current_player, current_bid, count, False)
        self.is_round_finished = True
        return

    def check_bid(self, new_bid, bid_number):
        # Checks if the bid is correct
        if new_bid[0] <= 0 or (new_bid[1] not in self.DICE_FACES.keys()):
            is_bid_correct = False
        elif bid_number > 1:
            # Rule of going from value to Paco
            if (self.current_bid[1] != 1 and new_bid[1] == 1):
                is_bid_correct = (new_bid[0] >= round(self.current_bid[0]/2))
            # Rule of going from Paco to any other value
            elif (self.current_bid[1] == 1 and new_bid[1] != 1):
                is_bid_correct = (new_bid[0] >= (2*self.current_bid[0] + 1))
            # Palifico rule
            elif self.is_palifico:
                is_bid_correct = (
                    new_bid[1] == self.current_bid[1] and new_bid[0] > self.current_bid[0])
            # Regular rule
            else:
                is_bid_correct = (new_bid[0] == self.current_bid[0] and new_bid[1] > self.current_bid[1]) or (
                    new_bid[1] == self.current_bid[1] and new_bid[0] > self.current_bid[0])
        else:
            # If the round begins and the bid is made of existing values, it is automatically correct
            return True
        return is_bid_correct

    def check_message(self, message, current_player_index, bid_number):
        # Check whether the message received by the server is correct or not
        # Return : is_bid_correct, new_bid, action whatever action has been chosen
        action = message[0]
        # Is it an existing action?
        if action in self.PLAYER_CHOICES:
            # Is it an overbid?
            if len(message) == 2:
                try:
                    # Converts the bid string to a tuple
                    new_bid = tuple(map(int, message[1].split(',')))
                except ValueError:
                    new_bid = [-1, -1]
                is_bid_correct = self.check_bid(new_bid, bid_number)
                if not is_bid_correct:
                    self.players[current_player_index].send_message(
                        "Veuillez choisir une action possible\n")
                return is_bid_correct, new_bid, action
            elif bid_number > 1:
                return True, (0, 0), action
            # A player can't Dodo or Calza at the first round
            else:
                self.players[current_player_index].send_message(
                    "Veuillez choisir une action possible\n")
                return False, False, False
        else:
            self.players[current_player_index].send_message(
                "Veuillez choisir une action possible\n")
            return False, False, False

    def check_action(self, action, bid, current_player, last_player):
        # Performs the correct action selected by the current player
        # Returns the player who will starts the next round
        next_round_starting_player = -1
        if action == "Overbid":
            # Update of the current bid
            self.current_bid = bid
            # Updates every plays of the new current bid
            for i in range(len(self.players)):
                self.players[i].send_message(
                    "Nouvelle enchère : " + str(self.current_bid))
        elif action == "Dodo":
            next_round_starting_player = self.check_dodo(
                self.current_bid, current_player, last_player)
        elif action == "Calza":
            self.check_calza(self.current_bid, current_player)
            next_round_starting_player = current_player
        return next_round_starting_player

    def end_round_message(self, current_player, bid, count, has_won):
        # Sends a message to every players at the end of the round
        # Specific message is sent to the winner/loser
        if has_won:
            self.players[current_player].send_update(
                "Tu as gagné ! Il y avait {} dés de valeur {} \n".format(count, self.DICE_FACES[bid[1]]))
            for i in [x for x in range(len(self.players)) if x != current_player]:
                self.players[i].send_update(
                    "Le joueur {} a eu raison, il y avait {} dés de valeur {}\n".format(current_player, count, self.DICE_FACES[bid[1]]))
        else:
            self.players[current_player].send_update(
                "Tu as perdu ! Il y avait {} dés de valeur {} \n".format(count, bid[1]))
            for i in [x for x in range(len(self.players)) if x != current_player]:
                self.players[i].send_update(
                    "Le joueur {} a eu tort, il y avait {} dés de valeur {}\n".format(current_player, count, self.DICE_FACES[bid[1]]))
        time.sleep(0.5)
        return

    def dead_message(self, dead_player):
        # Sends a message when a players dies
        # Specific message is sent to the dead player
        dead_msg = "Tu es éliminé de la partie, tu retenteras une prochaine fois !\n"
        self.players[dead_player].send_update(dead_msg)
        for i in [x for x in self.players_alive if x != dead_player]:
            self.players[i].send_update(
                "Le joueur {} est éliminé de la partie, il reste {} joueurs !\n".format(dead_player, len(self.players_alive)))
        time.sleep(0.5)
        return

    def end_game_message(self):
        # Sends a message to every players at the end of the game
        # Specific message is sent to the winner
        winner = self.players_alive[0]
        winner_msg = "Félicitations, tu as gagné cette partie de Pyrudo ! Il te restait {} dé(s) !".format(
            self.players[winner].number_of_dices)
        self.players[winner].send_update(winner_msg)
        for i in [x for x in range(len(self.players)) if x != winner]:
            self.players[i].send_update(
                "Le joueur {} a gagné cette partie de Pyrudo ! Il lui restait {} dé(s) !".format(winner, self.players[winner].number_of_dices))
        time.sleep(0.5)
        # Message who starts the closure of the game for everyone
        for i in range(len(self.players)):
            self.players[i].send_update("END")
        return

    def play_round(self, starting_player_index):
        # Initializes the next round
        current_player_index = starting_player_index
        self.current_bid = (0, 0)
        self.is_round_finished = False
        self.is_palifico = False
        last_player_index = 0
        bid_number = 0
        # Dice roll for everyone!
        for player in self.players_alive:
            self.players[player].dice_roll()

        while not self.is_round_finished:
            # Round begin messages
            self.players[current_player_index].send_message("À ton tour !\n")
            for i in [x for x in range(len(self.players)) if x != current_player_index]:
                self.players[i].send_message(
                    "C'est au tour de {}\n".format(current_player_index))
            is_message_correct = False
            bid_number += 1
            # Waiting for a CORRECT message from the CURRENT player
            while not is_message_correct:
                received_message = self.players[current_player_index].player_socket.recv(
                    1024)
                received_message = received_message.decode("utf-8")
                # Shaping of the received message before checking it
                received_message = received_message.split(":")
                # Checks the message
                is_message_correct, new_bid, action = self.check_message(
                    received_message, current_player_index, bid_number)
            # Performs the action chosen by the current player
            next_round_starting_player = self.check_action(
                action, new_bid, current_player_index, last_player_index)
            last_player_index = current_player_index
            # Who's next to play?
            if not self.is_round_finished:
                current_player_index = self.next_player(current_player_index)

        return next_round_starting_player

    def play_game(self) -> None:
        # Initializes players and variables
        for i in range(len(self.players)):
            self.players[i].reset()
            self.players_alive.append(i)
        is_game_finished = False
        # Each player receives the rules of the game
        texte = "Règles :"
        try:
            fich = open("rules.txt", "r", encoding="utf-8")
            texte = fich.read()
        except FileNotFoundError:
            print("Warning: rules.txt not found in " + os.getcwd() + "\n")

        for i in [x for x in range(len(self.players))]:
            self.players[i].send_message(texte)
        # Starting player of the game is randomly chosen
        starting_player_index = random.choice(self.players_alive)

        # Starts the game, run until game is finished
        while not is_game_finished:

            # Start a round, run until round is finished
            starting_player_index = self.play_round(starting_player_index)
            # Is the game over?
            is_game_finished = (len(self.players_alive) == 1)
        # Sends a message to close the game
        self.end_game_message()
        return


if __name__ == "__main__":
    print(PyrudoReferee.DICE_FACES)
