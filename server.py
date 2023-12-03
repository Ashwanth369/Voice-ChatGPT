import socket
import select
import time

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get local machine name
host = socket.gethostname()

# Define the port on which you want to communicate
port = 12345

# Bind the socket to a specific address and port
server_socket.bind((host, port))

# Set the socket to listening mode
server_socket.listen(5)

print(f"Server listening on {host}:{port}")

while True:
    # Accept the connection from the client
    client_socket, addr = server_socket.accept()
    print(f"Got connection from {addr}")

    while True:
        # Wait for data from the client or timeout after 30 seconds
        ready_to_read, _, _ = select.select([client_socket], [], [], 5)

        if not ready_to_read:
            # No data received from the client within the timeout period, close the connection
            print(f"No data received from {addr}. Closing connection.")
            break

        # Receive data from the client
        data = client_socket.recv(1024).decode('utf-8')

        # If the client sends an empty message, it means the client wants to close the connection
        if not data:
            print(f"Connection with {addr} closed by the client.")
            break

        print(f"Received message from {addr}: {data}")

    # Close the connection with the client
    client_socket.close()
