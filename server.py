import socket
import threading
import random
import math

PRIME_LIST = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
                     31, 37, 41, 43, 47, 53, 59, 61, 67,
                     71, 73, 79, 83, 89, 97, 101, 103,
                     107, 109, 113, 127, 131, 137, 139,
                     149, 151, 157, 163, 167, 173, 179,
                     181, 191, 193, 197, 199, 211, 223,
                     227, 229, 233, 239, 241, 251, 257,
                     263, 269, 271, 277, 281, 283, 293,
                     307, 311, 313, 317, 331, 337, 347, 349]
class Server:

    def __init__(self, port: int) -> None:
        self.host = '127.0.0.1'
        self.port = port
        self.clients = []
        self.username_lookup = {}
        self.s = socket.socket(socket.AF_INET,socket.SOCK_STREAM)
    
    def random_n_bit_number(self, n):
        return random.randrange(2**(n-1)+1, 2**n - 1)
    
    def millerRabinTest(self, number, iterations=20):
        max_div_by_two = 0
        even_comp = number - 1
        while even_comp % 2 == 0:
            even_comp >>= 1
            max_div_by_two += 1
        assert 2**max_div_by_two*even_comp == number - 1

        def trialComposite(round_tester): 
            if pow(round_tester, even_comp, number) == 1: 
                return False
            for i in range(max_div_by_two): 
                if pow(round_tester, 2**i * even_comp, number) == number-1: 
                    return False
            return True
        for i in range(iterations): 
            round_tester = random.randrange(2, number) 
            if trialComposite(round_tester): 
                return False
        return True
    
    def get_big_prime(self, len_bits):
        while True:
            flag = False
            prime_cand = self.random_n_bit_number(len_bits)
            for divisor in PRIME_LIST:
                if prime_cand % divisor == 0 and divisor ** 2 <= prime_cand:
                    flag = True
            if flag and self.millerRabinTest(prime_cand):
                return prime_cand

    def generateRSAkeys(self):
        E = 65537 # very common value for open exponent
        P = self.get_big_prime(512)
        Q = self.get_big_prime(512)
        while math.gcd((P-1)*(Q-1), E) != 1:
            P = self.get_big_prime(512)
            Q = self.get_big_prime(512)
        PHI = (P-1)(Q-1)
        N = P*Q
        #d*e = 1 mod(λ(n))
        # λ(n) is Carmichael's function
        # λ(n) = lcm(p-1, q-1) = ((p-1)/gcd(p-1, q-1))(q-1);
        # Using the first equating we get:
        # e*d = 1 mod(((p-1)/gcd(p-1, q-1))(q-1))
        D = pow(E, -1, PHI)
        return ((N, E), D)


    def start(self):
        self.s.bind((self.host, self.port))
        self.s.listen(100)

        # generate keys ...
        server_pub_key, server_priv_key = self.generateRSAkeys()

        while True:
            c, addr = self.s.accept()
            username = c.recv(1024).decode()
            print(f"{username} tries to connect")
            self.broadcast(f'new person has joined: {username}')
            self.username_lookup[c] = username
            self.clients.append(c)

            # send public key to the client 

            # ...

            # encrypt the secret with the clients public key

            # ...

            # send the encrypted secret to a client 

            # ...

            threading.Thread(target=self.handle_client,args=(c,addr,)).start()

    def broadcast(self, msg: str):
        for client in self.clients: 

            # encrypt the message

            # ...

            client.send(msg.encode())

    def handle_client(self, c: socket, addr): 
        while True:
            msg = c.recv(1024)

            for client in self.clients:
                if client != c:
                    client.send(msg)

if __name__ == "__main__":
    s = Server(9001)
    s.start()
