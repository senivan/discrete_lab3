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

            
            # c.send(encrypt(json.dumps(self.private_key), self.username_lookup[c][1]))
            # Client has no need of our secret key.
            # send the encrypted secret to a client 

            # print("Secret key sent!(encrypted ofc)")

            threading.Thread(target=self.handle_client,args=(c,addr,)).start()

    def broadcast(self, msg: str):
        for client in self.clients: 

            # encrypt the message
            # generate hash here
            to_send = encrypt(msg, self.username_lookup[client][1])

            client.send(to_send)

    def handle_client(self, c: socket, addr): 
        try:
            while True:
                msg = c.recv(16192).decode()
                msg = decrypt(msg, self.private_key)

                # validate message integrity here

                for client in self.clients:
                    if client != c:
                        msg = encrypt(msg, self.username_lookup[client][1])
                        client.send(msg)
        except Exception as e:
            print(f"Clients {addr} disconnected")
            self.clients.remove(c)
            self.broadcast(f"{self.username_lookup[c][0]} has left")
            c.close()

if __name__ == "__main__":
    s = Server(9001)
    s.start()

