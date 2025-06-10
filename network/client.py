import socket
import threading

SERVER_IP = input("Adresse IP de l'hôte : ")
PORT = 65432

def receive(sock):
    while True:
        data = sock.recv(1024)
        if data:
            print(f"Reçu : {data.decode()}")

def main():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.connect((SERVER_IP, PORT))
        threading.Thread(target=receive, args=(s,), daemon=True).start()

        print("Connecté. Tapez vos actions.")
        while True:
            msg = input()
            s.sendall(msg.encode())


if __name__ == "__main__":
    main()
