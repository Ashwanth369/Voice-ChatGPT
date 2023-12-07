import cpgt
import socket
import threading
import time

def handle_client(client_socket, address, packet_size=1024, timeout=60):
    print(f"Connected to client: {address}")
    client_request = ""
    start_time = time.time()
    while time.time() - start_time <= timeout:
        data = client_socket.recv(1024).decode('utf-8')
        if "!REQUEST!" in data:
            client_request += data.split("!REQUEST!")[0]
            print("SERVER: ", client_request)
            try:
                client_response = cpgt.sendToGPT(client_request)
            except Exception:
                client_response = "Sorry! I Couldn't understand that."

            print("SERVER: ", client_response)
            for i in range(0, len(client_response), packet_size):
                msg_chunk = client_response[i:i+packet_size]
                client_socket.send(msg_chunk.encode('utf-8'))
            client_socket.send("!RESPONSE!".encode('utf-8'))
        if not data:
            client_request = ""
        else:
            client_request += data
            start_time = time.time()

    print(f"Client {address} Disconnected")
    client_socket.close()

def main():
    server_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    host = socket.gethostname()
    port = 12345
    server_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
    server_socket.bind((host, port))
    server_socket.listen(5)
    print(f"Server listening on {host}:{port}")

    client_threads = []

    try:
        while True:
            client_socket, address = server_socket.accept()
            client_thread = threading.Thread(target=handle_client, args=(client_socket, address))
            client_thread.start()
            client_threads.append(client_thread)

    except KeyboardInterrupt:
        print("\nServer is shutting down...")
        for client_thread in client_threads:
            client_thread.join()
        server_socket.close()

if __name__ == "__main__":
    main()
