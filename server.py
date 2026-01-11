import socket
import threading

HOST = "185.254.205.240"
PORT = 8080

server = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
server.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, 1)
server.bind((HOST, PORT))
server.listen()

clients = []

print("Сервер запущен")

def broadcast(message):
    for client in clients:
        try:
            client.send(message)
        except:
            clients.remove(client)

def handle_client(client):
    while True:
        try:
            msg = client.recv(1024)
            if not msg:
                break
            broadcast(msg)
        except:
            break

    clients.remove(client)
    client.close()

while True:
    client, addr = server.accept()
    print("Подключился:", addr)
    clients.append(client)

    threading.Thread(target=handle_client, args=(client,), daemon=True).start()
