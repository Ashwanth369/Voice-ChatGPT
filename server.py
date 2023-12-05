import socket
import select
import time
import subprocess
import cpgt

# Create a socket object
server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get local machine name
host = socket.gethostname()

# Define the port on which you want to communicate
port = 12345

# Define the packet that you desire to split up the message to be sent back to the client in chunks
packet_size = 1024

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

    # Sending the text from the client to ChatGPT and storing the response received from it
    textFromChatGPT = cpgt.sendToGPT(data)

    # Sending back the response received from ChatGPT to the client in chunks
    for i in range(0, len(textFromChatGPT), packet_size):
        msg_chunk = textFromChatGPT[i:i+packet_size]
        client_socket.send(msg_chunk.encode('utf-8'))

    # client_socket.send(textFromChatGPT.encode('utf-8'))

    # Close the connection with the client
    client_socket.close()
