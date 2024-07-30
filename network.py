import socket
import threading

class Network:
    def __init__(self, host='localhost', port=12345):
        self.host = host
        self.port = port
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.clients = []
        self.player_data = {}

    def start_server(self):
        try:
            self.socket.bind((self.host, self.port))
            self.socket.listen()
            print("Server started on {}:{}".format(self.host, self.port))
            while True:
                conn, addr = self.socket.accept()
                print(f"Connected by {addr}")
                self.clients.append(conn)
                threading.Thread(target=self.handle_client, args=(conn, addr)).start()
        except Exception as e:
            print(f"Server error: {e}")
            self.socket.close()

    def handle_client(self, conn, addr):
        while True:
            try:
                data = conn.recv(1024)
                if not data:
                    break
                # Here you would handle incoming messages and update game state
                print(f"Received data from {addr}: {data.decode()}")
                self.broadcast(data, conn)
            except:
                break
        conn.close()

    def broadcast(self, message, source):
        for client in self.clients:
            if client != source:
                client.sendall(message)

    def connect_to_server(self):
        try:
            self.socket.connect((self.host, self.port))
            print(f"Connected to server at {self.host}:{self.port}")
            threading.Thread(target=self.receive_data, daemon=True).start()
        except Exception as e:
            print(f"Unable to connect to server: {e}")

    def receive_data(self):
        while True:
            try:
                data = self.socket.recv(1024)
                if not data:
                    break
                # Update local game state based on data
                print(f"Received: {data.decode()}")
            except:
                break
        self.socket.close()

    def send_data(self, data):
        try:
            self.socket.sendall(data.encode())
        except Exception as e:
            print(f"Failed to send data: {e}")