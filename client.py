import socket
import threading
from RSA import generateRSAkeys, encrypt, decrypt
import json
class Client:
    def __init__(self, server_ip: str, port: int, username: str) -> None:
        self.server_ip = server_ip
        self.port = port
        self.username = username

    def init_connection(self):
        self.s = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        try:
            self.s.connect((self.server_ip, self.port))
        except Exception as e:
            print("[client]: could not connect to server: ", e)
            return

        self.s.send(self.username.encode())

        # create key pairs - done
        client_public_key, client_private_key = generateRSAkeys()
        self.public_key = client_public_key
        self.private_key = client_private_key
        print("Keys generated!")
        # exchange public keys
        message = self.s.recv(1024).decode()
        self.server_key = json.loads(message.split(": ")[1])
        send = ("KEY: "+json.dumps(self.public_key)).encode('utf-8')
        self.s.send(send)
        print("Keys exchanged!")
        # receive the encrypted secret key

        
        message_handler = threading.Thread(target=self.read_handler,args=())
        message_handler.start()
        input_handler = threading.Thread(target=self.write_handler,args=())
        input_handler.start()

    def read_handler(self): 
        while True:
            message = self.s.recv(1024).decode()
            # decrypt message with the secrete key

            message = decrypt(message, self.private_key, self.public_key)
            print(message)

    def write_handler(self):
        while True:
            message = input()

            # encrypt message with the secrete key

            # ...

            self.s.send(message.encode())

if __name__ == "__main__":
    cl = Client("127.0.0.1", 9001, "b_g")
    cl.init_connection()
