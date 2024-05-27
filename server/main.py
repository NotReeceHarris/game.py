import socket
import threading

class ClientThread(threading.Thread):
    def __init__(self, client_address, client_socket):
        threading.Thread.__init__(self)
        self.csocket = client_socket
        print("New connection added: ", client_address)

    def run(self):
        print("Connection from : ", client_address)
        while True:
            data = self.csocket.recv(2048)
            if not data:
                break
            print("from client", data)
            self.csocket.send(data)
        print("Client at ", client_address, " disconnected...")

LOCALHOST = "127.0.0.1"
PORT = 8008

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((LOCALHOST, PORT))

print("Server started")
print("Waiting for client request..")

while True:
    server.listen(1)
    client_sock, client_address = server.accept()
    new_thread = ClientThread(client_address, client_sock)
    new_thread.start()