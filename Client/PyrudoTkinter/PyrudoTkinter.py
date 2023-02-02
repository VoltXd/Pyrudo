import socket
import tkinter as tk
import threading

class PyrudoClientTkinter(tk.Tk):
    DICE_UNICODE = ["\u2680", "\u2681", "\u2682", "\u2683", "\u2684", "\u2685"]

    def __init__(self) -> None:
        # Initialise window
        tk.Tk.__init__(self)
        self.running = True

        self.title("Pyrudo")
        self.width = 1280
        self.height = 720
        self.geometry(str(self.width) + "x" + str(self.height))

        # ----- Frames ----- 
        connection_frame = tk.LabelFrame(self, text="Connexion", borderwidth=2, relief=tk.GROOVE)
        connection_frame.pack(side=tk.TOP, padx=10, pady=10, fill="x")
        game_frame = tk.LabelFrame(self, text="Jeu", borderwidth=2, relief=tk.GROOVE)
        game_frame.pack(side=tk.TOP, padx=10, fill="both", expand="yes")
        choice_frame = tk.LabelFrame(self, text="Choix", borderwidth=2, relief=tk.GROOVE)
        choice_frame.pack(side=tk.TOP, padx=10, pady=10, fill="x")
        
        # ----- Connection frame -----
        # Entries
        ip_validate_command = (self.register(self._ip_number_validation), "%P", "%S")
        port_validate_command = (self.register(self._port_number_validation), "%P", "%S")
        self.entries_ip = []
        self.entries_ip.append(tk.Entry(connection_frame, validate="key", validatecommand=ip_validate_command, width=3))
        self.entries_ip.append(tk.Entry(connection_frame, validate="key", validatecommand=ip_validate_command, width=3))
        self.entries_ip.append(tk.Entry(connection_frame, validate="key", validatecommand=ip_validate_command, width=3))
        self.entries_ip.append(tk.Entry(connection_frame, validate="key", validatecommand=ip_validate_command, width=3))
        self.entry_port = tk.Entry(connection_frame, validate="key", validatecommand=port_validate_command, width=5)
        self.connection_label = tk.Label(connection_frame, text="Déconnecté")
        
        # Default value
        self.entries_ip[0].insert(0, "127")
        self.entries_ip[1].insert(0, "0")
        self.entries_ip[2].insert(0, "0")
        self.entries_ip[3].insert(0, "1")
        
        for i in range(len(self.entries_ip)):
            
            # Unpacks
            self.entries_ip[i].pack(side=tk.LEFT)

            # separator label
            label_str = "."
            if i == len(self.entries_ip) - 1:
                label_str = ":"
            tk.Label(connection_frame, text=label_str).pack(side=tk.LEFT)
        
        # Default value + Unpack 
        self.entry_port.insert(0, "8081")
        self.entry_port.pack(side=tk.LEFT)        

        # Button
        self.button_connection = tk.Button(connection_frame, text="Connexion", command=self._connect)
        self.button_connection.pack(side=tk.RIGHT, padx=20, pady=2)        

        # Connection Label
        self.connection_label.pack(side=tk.RIGHT, padx=10)
        
        # ----- Game frame -----
        # Player frames
        info_frame = tk.LabelFrame(game_frame, text="Informations", borderwidth=2, relief=tk.GROOVE)
        bid_frame = tk.LabelFrame(info_frame, text="Enchère", borderwidth=2, relief=tk.GROOVE)
        turn_frame = tk.LabelFrame(info_frame, text="Tour", borderwidth=2, relief=tk.GROOVE)
        player_frame = tk.LabelFrame(game_frame, text="Joueur", borderwidth=2, relief=tk.GROOVE)
        opponent1_frame = tk.LabelFrame(game_frame, text="Adversaire 1", borderwidth=2, relief=tk.GROOVE)
        opponent2_frame = tk.LabelFrame(game_frame, text="Adversaire 2", borderwidth=2, relief=tk.GROOVE)
        opponent3_frame = tk.LabelFrame(game_frame, text="Adversaire 3", borderwidth=2, relief=tk.GROOVE)
        opponent4_frame = tk.LabelFrame(game_frame, text="Adversaire 4", borderwidth=2, relief=tk.GROOVE)
        info_frame.pack(side=tk.TOP, padx=10, fill="both", expand="yes")
        bid_frame.pack(side=tk.LEFT, padx=10, fill="both", expand="yes", pady=2)
        turn_frame.pack(side=tk.LEFT, padx=10, fill="both", expand="yes", pady=2)
        player_frame.pack(side=tk.LEFT, padx=10, fill="both", expand="yes")
        opponent1_frame.pack(side=tk.TOP, padx=10, fill="both", expand="yes")
        opponent2_frame.pack(side=tk.TOP, padx=10, fill="both", expand="yes")
        opponent3_frame.pack(side=tk.TOP, padx=10, fill="both", expand="yes")
        opponent4_frame.pack(side=tk.TOP, padx=10, fill="both", expand="yes")

        self.bid_number_label = tk.Label(bid_frame, text='', font=("Helvetica", 25))
        self.bid_face_label = tk.Label(bid_frame, text='', font=("Helvetica", 25))
        self.bid_number_label.pack(side=tk.LEFT)
        self.bid_face_label.pack(side=tk.LEFT)

        self.turn_label = tk.Label(turn_frame, text='')
        self.turn_label.pack(side=tk.LEFT)

        self.player_dice_labels = []
        self.opponent1_dice_labels = []
        self.opponent2_dice_labels = []
        self.opponent3_dice_labels = []
        self.opponent4_dice_labels = []

        for i in range(5):
            self.player_dice_labels.append(tk.Label(player_frame, text='', font=("Helvetica", 100)))
            self.opponent1_dice_labels.append(tk.Label(opponent1_frame, text='', font=("Helvetica", 50)))
            self.opponent2_dice_labels.append(tk.Label(opponent2_frame, text='', font=("Helvetica", 50)))
            self.opponent3_dice_labels.append(tk.Label(opponent3_frame, text='', font=("Helvetica", 50)))
            self.opponent4_dice_labels.append(tk.Label(opponent4_frame, text='', font=("Helvetica", 50)))
            self.player_dice_labels[i].pack(side=tk.LEFT)
            self.opponent1_dice_labels[i].pack(side=tk.LEFT)
            self.opponent2_dice_labels[i].pack(side=tk.LEFT)
            self.opponent3_dice_labels[i].pack(side=tk.LEFT)
            self.opponent4_dice_labels[i].pack(side=tk.LEFT)

        # ----- Choice frame -----
        # Number Spinbox
        self.spinbox_number_of_dice = tk.Spinbox(choice_frame, from_=1, to=100)
        
        # Face Listbox
        self.list_dice_face = tk.Listbox(choice_frame, height=6)
        self.list_dice_face.insert(1, "Paco")
        self.list_dice_face.insert(2, "2")
        self.list_dice_face.insert(3, "3")
        self.list_dice_face.insert(4, "4")
        self.list_dice_face.insert(5, "5")
        self.list_dice_face.insert(6, "6")

        # Choice buttons
        self.button_overbid = tk.Button(choice_frame, text="Surenchérir", state="disabled", command=self._on_overbid)
        self.button_dodo = tk.Button(choice_frame, text="Dodo", state="disabled", command=self._on_dodo)
        self.button_calza = tk.Button(choice_frame, text="Calza", state="disabled", command=self._on_calza)


        # Unpack
        tk.Label(choice_frame, text="Nombre : ").pack(side=tk.LEFT)
        self.spinbox_number_of_dice.pack(side=tk.LEFT)
        tk.Label(choice_frame, text="Face : ").pack(side=tk.LEFT)
        self.list_dice_face.pack(side=tk.LEFT)
        self.button_overbid.pack(side=tk.LEFT, padx=20, pady=2)
        self.button_dodo.pack(side=tk.LEFT, padx=20, pady=2)
        self.button_calza.pack(side=tk.LEFT, padx=20, pady=2)

        # ----- Socket -----
        self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.is_connected = False
        self.listening_thread = None
        return

    def _ip_number_validation(self, string, char):
        if not char.isdigit():
            self.bell()
            return False
        
        if string == "":
            return True
        
        if 0 <= int(string) and int(string) < 256:
            return True
        else:
            return False
            
    def _port_number_validation(self, string, char):
        if not char.isdigit():
            self.bell()
            return False
        
        if string == "":
            return True
        
        if 0 <= int(string) and int(string) < 65536:
            return True
        else:
            return False

    def _connect(self):
        # Verify entries are not empty
        ip_address = ""
        for i in range(len(self.entries_ip)):
            ip_str = self.entries_ip[i].get() 
            if ip_str == "":
                return
        port_str = self.entry_port.get()
        if port_str == "":
            return
        
        # Create IP string
        for i in range(len(self.entries_ip)):
            ip_str = self.entries_ip[i].get() 
            ip_address += str(int(ip_str))
            if i != len(self.entries_ip) - 1:
                ip_address += "."
        
        # Create server's address
        server_address = (ip_address, int(port_str))
        try:
            self.server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
            self.server_socket.connect(server_address)
        except ConnectionRefusedError:
            print("Server not found.")
            return

        # Wait for server's response
        self.server_socket.settimeout(15)
        try:
            server_response = self.server_socket.recv(4096)
            if server_response.decode("utf-8") == "CONNECTED TO PYRUDO":
                self.is_connected = True
                self.connection_label.config(text="Connecté à " + str(server_address))
            else:
                self.is_connected = False
                self.server_socket.close()
                return
        except socket.timeout:
            #TODO: Message dans tkinter
            print("Server didn't respond.")
        
        # Non blocking behaviour
        self.server_socket.settimeout(0)

        # Server responded, disable connections
        self.button_connection["state"] = "disabled"
        self.entry_port["state"] = "disabled"
        for i in range(len(self.entries_ip)):
            self.entries_ip[i]["state"] = "disabled"

        # Run listen thread
        self.listening_thread = threading.Thread(target=self._listen_server)
        self.listening_thread.start()

        return

    def _listen_server(self):
        while self.is_connected and self.running:
            msg = ""
            try:
                msg = self.server_socket.recv(4096).decode("utf-8")
                print(msg)
            except BlockingIOError:
                pass
            messages = msg.split("\n")
            for message in messages :
                if "Msg: À ton tour !" in message or "Msg: Veuillez choisir une action possible" in message:
                    # C'est à notre tour =>
                    # Autoriser les appuies boutons
                    self.button_overbid["state"] = "active"
                    self.button_dodo["state"] = "active"
                    self.button_calza["state"] = "active"
                    self.turn_label.config(text="À ton tour !")
                elif "Msg: C'est au tour de" in message:
                    numbers = [int(s) for s in message.split() if s.isdigit()]
                    self.turn_label.config(text="C'est au tour de " + str(numbers[0]))
                elif "Update: Tu as tiré :" in message:
                    current_dice_index = 0
                    # Reset dices
                    for i in range(len(self.player_dice_labels)):
                        self.player_dice_labels[i].config(text="")
                    roll_msg_index = messages.index("Update: Tu as tiré :")
                    for i in range(roll_msg_index + 1, roll_msg_index + 7):
                        number_of_dice_and_face = messages[i].split(" ")
                        for _ in range(int(number_of_dice_and_face[0])):
                            self.player_dice_labels[current_dice_index].config(text=self.DICE_UNICODE[i - 1 - roll_msg_index])
                            current_dice_index += 1
                elif "Msg: Nouvelle enchère :" in message:
                    bid = self._extract_bid(message)
                    self.bid_number_label.config(text=bid[0])
                    self.bid_face_label.config(text=self.DICE_UNICODE[bid[1]-1])
                elif "Update: END" in message:
                    # La partie est finie =>
                    # Fermer le socket
                    self.server_socket.close()
                    self.is_connected = False

                    # Autoriser la connexion
                    self.button_connection["state"] = "active"
                    self.entry_port["state"] = "normal"
                    for i in range(len(self.entries_ip)):
                        self.entries_ip[i]["state"] = "normal"

                    # Interdire les actions 
                    self.button_overbid["state"] = "disabled"
                    self.button_dodo["state"] = "disabled"
                    self.button_calza["state"] = "disabled"

                    # Mettre à jour l'affichage
                    self.connection_label.config(text="Déconnecté")
                    for i in range(5):
                        self.player_dice_labels[i].config(text="")
                        self.opponent1_dice_labels[i].config(text="")
                        self.opponent2_dice_labels[i].config(text="")
                        self.opponent3_dice_labels[i].config(text="")
                        self.opponent4_dice_labels[i].config(text="")
                    self.bid_face_label.config(text="")
                    self.bid_number_label.config(text="")
                    self.turn_label.config(text="")
        return
    
    def _on_overbid(self):
        # Get values
        number_of_dice = self.spinbox_number_of_dice.get()
        dice_face = self.list_dice_face.get(tk.ACTIVE)
        if dice_face == "Paco":
            dice_face = "1"
        
        # Send message
        self.server_socket.send(("Overbid:" + number_of_dice + "," + dice_face).encode("utf-8"))
        self.button_overbid["state"] = "disabled"
        self.button_dodo["state"] = "disabled"
        self.button_calza["state"] = "disabled"
        return

    def _on_dodo(self):
        self.server_socket.send(("Dodo").encode("utf-8"))
        self.button_overbid["state"] = "disabled"
        self.button_dodo["state"] = "disabled"
        self.button_calza["state"] = "disabled"
        return  

    def _on_calza(self):
        self.server_socket.send(("Calza").encode("utf-8"))    
        self.button_overbid["state"] = "disabled"
        self.button_dodo["state"] = "disabled"
        self.button_calza["state"] = "disabled"    
        return

    def _extract_bid(self, msg: str):
        char_was_digit = False
        number_retrieved = False

        number = 0
        face = 0
        for i in msg:
            if i.isdigit() and not number_retrieved:
                if char_was_digit:
                    number *= 10
                number += int(i)
            elif char_was_digit and not number_retrieved:
                number_retrieved = True
            elif i.isdigit() and number_retrieved:
                face = int(i)
                
            char_was_digit = i.isdigit()

        bid = (number, face)
        return (number, face)

    def close(self):
            self.running = False
            return


def main():
    app = PyrudoClientTkinter()

    # Run
    app.mainloop()
    app.close()
    
if __name__ == "__main__":
    main()