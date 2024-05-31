import socket
import threading
import uuid

class ClientThread(threading.Thread):
    def __init__(self, client_address, client_socket):
        threading.Thread.__init__(self)
        self.csocket = client_socket
        self.id = str(uuid.uuid4())


        self.x = None
        self.y = None

        self.csocket.send("0:{}".format(self.id).encode())
        print("New connection added: ", client_address)

    def run(self):
        print("Connection from : ", client_address)
        while True:
            data = self.csocket.recv(2048).decode()
            if not data:
                break

            string = data
            array = string.split(':')

            if array[0] == '1':

                if self.x == None and self.y == None:
                    self.x = float(array[1])
                    self.y = float(array[2])
                else:

                    # sent x and y cant be more than 10 units away from current x and y
                    if -10 < self.x - float(array[1]) < 10 and -10 < self.y - float(array[2]) < 10:
                        self.x = float(array[1])
                        self.y = float(array[2])
                    else:
                        print("Invalid movement detected", self.x - float(array[1]), self.y - float(array[2]))

                print("[",self.id ,"] coords", self.x, self.y)

            #self.csocket.send(data)
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