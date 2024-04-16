import socket
import threading
from RSA import generateRSAkeys, encrypt, decrypt
import json
import ast
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
        message = self.s.recv(8096).decode()
        self.server_key = json.loads(message.split(": ")[1])
        send = ("KEY: "+json.dumps(self.public_key)).encode('utf-8')
        self.s.send(send)
        print("Keys exchanged!")
        # receive the encrypted secret key
        serv_secret = self.s.recv(131072).decode()
        self.server_secret = ast.literal_eval(decrypt(serv_secret, self.private_key))
        print(self.server_secret)
        print(isinstance(self.server_secret, str))
        print("Secret key received!")
        
        message_handler = threading.Thread(target=self.read_handler,args=())
        message_handler.start()
        input_handler = threading.Thread(target=self.write_handler,args=())
        input_handler.start()

    def read_handler(self):
        while True:
            message = self.s.recv(16192)
            # decrypt message with the secrete key - done

            # validate hash here.

            message = decrypt(message, self.private_key)
            print(message)

    def write_handler(self):
        while True:
            message = input()

            # encrypt message with the secrete key

            message = encrypt(message, self.server_key)

            self.s.send(message)

if __name__ == "__main__":
    cl = Client("127.0.0.1", 9001, "b_g")
    cl.init_connection()
