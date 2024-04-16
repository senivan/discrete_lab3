import socket
import threading
from RSA import generateRSAkeys, encrypt, decrypt
import json


class Server:

    def __init__(self, port: int) -> None:
        self.host = '127.0.0.1'
        self.port = port
        self.clients = []
        self.username_lookup = {}
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    


    def start(self):
        self.s.bind((self.host, self.port))
        self.s.listen(100)

        # generate keys - done
        server_pub_key, server_priv_key = generateRSAkeys()
        self.public_key = server_pub_key
        self.private_key = server_priv_key
        print("Keys generated!")
        while True:
            c, addr = self.s.accept()
            username = c.recv(1024).decode()
            print(f"{username} tries to connect")
            self.broadcast(f'new person has joined: {username}')
            self.username_lookup[c] = [username]
            self.clients.append(c)

            # send public key to the client  - done
            msg = ("KEY: "+json.dumps(self.public_key)).encode('utf-8')
            c.send(msg)

            client_pub_key = c.recv(1024).decode()
            self.username_lookup[c].append(json.loads(client_pub_key.split(": ")[1]))
            print("Public keys exchanged")

            # encrypt the secret with the clients public key

            
            c.send(encrypt(json.dumps(self.private_key), self.username_lookup[c][1]))

            # send the encrypted secret to a client 

            print("Secret key sent!(encrypted ofc)")

            threading.Thread(target=self.handle_client,args=(c,addr,)).start()

    def broadcast(self, msg: str):
        for client in self.clients: 

            # encrypt the message

            msg = encrypt(msg, self.public_key)

            client.send(msg)

    def handle_client(self, c: socket, addr): 
        while True:
            msg = c.recv(1024)

            for client in self.clients:
                if client != c:
                    client.send(msg)

if __name__ == "__main__":
    s = Server(9001)
    s.start()

