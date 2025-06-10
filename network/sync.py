# network/sync.py – synchronisation des actions multijoueur
import socket
import threading

class NetworkSync:
    def __init__(self, host, port=65432):
        self.socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self.conn = None
        self.is_host = host == 'host'
        self.running = False
        self.inbox = []

        if self.is_host:
            self.socket.bind(("0.0.0.0", port))
            self.socket.listen(1)
            print("[Serveur] En attente de connexion...")
            self.conn, _ = self.socket.accept()
            print("[Serveur] Joueur connecté")
        else:
            self.socket.connect((host, port))
            self.conn = self.socket
            print("[Client] Connecté à l'hôte")

        self.running = True
        threading.Thread(target=self.listen, daemon=True).start()

    def listen(self):
        while self.running:
            try:
                data = self.conn.recv(1024)
                if data:
                    self.inbox.append(data.decode())
            except:
                break

    def send(self, message):
        if self.conn:
            try:
                self.conn.sendall(message.encode())
            except:
                self.running = False

    def receive(self):
        if self.inbox:
            return self.inbox.pop(0)
        return None

    def close(self):
        self.running = False
        if self.conn:
            self.conn.close()
        self.socket.close()
