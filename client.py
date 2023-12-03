import socket, time

# Create a socket object
client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)

# Get local machine name
host = socket.gethostname()

# Define the port on which you want to connect
port = 12345

# Connect to the server
client_socket.connect((host, port))

message = "A"*8000

for i in range(0, len(message), 1024):
    # Get input from the user to send to the server
    m = message[i:i+1024]

    # Send the message to the server
    client_socket.send(m.encode('utf-8'))
    time.sleep(10)

    try:
        # Attempt to receive a small amount of data to check if the connection is still open
        client_socket.recv(1)
    except socket.error:
        # If an exception is raised, the connection is closed
        print("Server closed the connection. Reconnecting...")
        
        # Close the current connection
        client_socket.close()

        # Create a new socket and connect again
        client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        client_socket.connect((host, port))


# Close the connection with the server
client_socket.close()
