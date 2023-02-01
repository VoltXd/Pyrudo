import socket
import tkinter as tk

class PyrudoClientTkinter(tk.Tk):
    def __init__(self) -> None:
        # Initialise window
        tk.Tk.__init__(self)
        self.title("Pyrudo")
        self.width = 1280
        self.height = 720
        self.geometry(str(self.width) + "x" + str(self.height))

        # Frames
        connection_frame = tk.LabelFrame(self, text="Connexion", borderwidth=2, relief=tk.GROOVE)
        connection_frame.pack(side=tk.TOP, padx=10, pady=10, fill="x")
        game_frame = tk.LabelFrame(self, text="Jeu", borderwidth=2, relief=tk.GROOVE)
        game_frame.pack(side=tk.TOP, padx=10, fill="both", expand="yes")
        choice_frame = tk.LabelFrame(self, text="Choix", borderwidth=2, relief=tk.GROOVE)
        choice_frame.pack(side=tk.TOP, padx=10, fill="x")
        
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
        
        
        for i in range(len(self.entries_ip)):
            # Default value
            self.entries_ip[i].insert(0, "0")
            
            # Unpacks
            self.entries_ip[i].pack(side=tk.LEFT)

            # separator label
            label_str = "."
            if i == len(self.entries_ip) - 1:
                label_str = ":"
            tk.Label(connection_frame, text=label_str).pack(side=tk.LEFT)
        
        # Default value + Unpack 
        self.entry_port.insert(0, "0")
        self.entry_port.pack(side=tk.LEFT)        

        # Button
        self.button_connection = tk.Button(connection_frame, text="Connexion", command=self._connect)
        self.button_connection.pack(side=tk.RIGHT, padx=20, pady=2)
        
        # ----- Game frame -----
        self.canvas = tk.Canvas(game_frame, background="white")
        self.canvas.pack(fill="both", expand="yes")

        # ----- Choice frame -----
        self.spinbox_number_of_dice = tk.Spinbox(choice_frame)
        self.list_dice_face = tk.Listbox(choice_frame)
        self.button_overbid = tk.Button(choice_frame, text="Surenchérir", state="disabled")
        self.button_dodo = tk.Button(choice_frame, text="Dodo", state="disabled")
        self.button_calza = tk.Button(choice_frame, text="Calza", state="disabled")

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
            else:
                self.is_connected = False
        except socket.timeout:
            #TODO: Message dans tkinter
            print("Server didn't respond.")
        self.server_socket.settimeout(None)

        # Server responded, disable connections
        self.button_connection["state"] = "disabled"
        self.entry_port["state"] = "disabled"
        for i in range(len(self.entries_ip)):
            self.entries_ip[i]["state"] = "disabled"

        return


def main():
    app = PyrudoClientTkinter()



    # Run
    app.mainloop()



    # ------------------------Vieux code------------------------ #

    # Connect to server 
    server_address = ("127.0.0.1", 8081)
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    server_socket.connect(server_address)

    # Wait & print message (for testing purpose)

    game_running = True

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
            elif message == "Update: END":
                game_running = False


    # End connection
    server_socket.close()

if __name__ == "__main__":
    main()