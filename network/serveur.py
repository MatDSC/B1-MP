import socket
import threading

HOST = "0.0.0.0"
PORT = 65432

clients = []

def handle_client(conn):
    while True:
        data = conn.recv(1024)
        if not data:
            break
        for c in clients:
            if c != conn:
                c.sendall(data)

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print("Server lancé, en attente d'un joueur...")

        while len(clients) < 2:
            conn, addr = s.accept()
            print(f"Connecté à {addr}")
            clients.append(conn)
            threading.Thread(target=handle_client, args=(conn,), daemon=True).start()

        print("Deux joueurs connectés. Début de la partie. ")

if __name__ == "__main__":
    main()
