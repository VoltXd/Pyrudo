import socket

# Connect to server 
server_address = ("127.0.0.1", 8081)
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server_socket.connect(server_address)

# Wait & print message (for testing purpose)
msg = server_socket.recv(4096)
print(msg.decode("utf-8"))

# End connection
server_socket.close()