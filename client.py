import socket

class ClientApp:

    def __init__(self, host=socket.gethostname(), port=12345, packet_size=100):
        self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.host = host
        self.port = port
        self.packet_size = packet_size
        self.client_socket.connect((self.host, self.port))

    def closeConnection(self):
        self.client_socket.close()

    def sendMessage(self, message):
        for i in range(0, len(message), self.packet_size):
            msg_chunk = message[i:i+self.packet_size]
            try:
                self.client_socket.send(msg_chunk.encode('utf-8'))
            except socket.error:
                self.client_socket.close()
                self.client_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
                self.client_socket.connect((self.host, self.port))

        self.client_socket.send("!REQUEST!".encode('utf-8'))

        response = ""
        while True:
            chunk = self.client_socket.recv(self.packet_size).decode('utf-8')
            if "!RESPONSE!" in chunk:
                response += chunk.split("!RESPONSE!")[0]
                break
            response += chunk
        
        return response
    

if __name__ == "__main__":
    ca = ClientApp()
    print(ca.sendMessage("How are you doing"))