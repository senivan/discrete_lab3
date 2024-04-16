import random
import math
class KeyGen:
    __PRIME_LIST = [2, 3, 5, 7, 11, 13, 17, 19, 23, 29,
                     31, 37, 41, 43, 47, 53, 59, 61, 67,
                     71, 73, 79, 83, 89, 97, 101, 103,
                     107, 109, 113, 127, 131, 137, 139,
                     149, 151, 157, 163, 167, 173, 179,
                     181, 191, 193, 197, 199, 211, 223,
                     227, 229, 233, 239, 241, 251, 257,
                     263, 269, 271, 277, 281, 283, 293,
                     307, 311, 313, 317, 331, 337, 347, 349]
    @staticmethod
    def __random_n_bit_number(n):
        return random.randrange(2**(n-1)+1, 2**n - 1)
    @staticmethod
    def miller_rabin_test(miller_rabin_candidate): 
        maxDivisionsByTwo = 0
        evenComponent = miller_rabin_candidate-1
    
        while evenComponent % 2 == 0: 
            evenComponent >>= 1
            maxDivisionsByTwo += 1
        assert(2**maxDivisionsByTwo * evenComponent == miller_rabin_candidate-1) 
    
        def trialComposite(round_tester): 
            if pow(round_tester, evenComponent,  
                miller_rabin_candidate) == 1: 
                return False
            for i in range(maxDivisionsByTwo): 
                if pow(round_tester, 2**i * evenComponent, 
                    miller_rabin_candidate)  == miller_rabin_candidate-1: 
                    return False
            return True
   
        # Set number of trials here 
        numberOfRabinTrials = 20
        for i in range(numberOfRabinTrials): 
            round_tester = random.randrange(2, 
                        miller_rabin_candidate) 
            if trialComposite(round_tester): 
                return False
        return True
    def get_pseudo_prime(n):
        while True:
            # Obtain a random number
            pc = KeyGen.__random_n_bit_number(n)
    
            # Test divisibility by pre-generated
            # primes
            for divisor in KeyGen.__PRIME_LIST:
                if pc % divisor == 0 and divisor**2 <= pc:
                    break
            else:
                return pc
    @staticmethod
    def get_big_prime(len_bits):
        prime_cand = KeyGen.get_pseudo_prime(len_bits)
        while not KeyGen.miller_rabin_test(prime_cand):
            prime_cand = KeyGen.get_pseudo_prime(len_bits)

        return prime_cand

def generateRSAkeys():
    E = 65537 # very common value for open exponent
    P = KeyGen.get_big_prime(1024)
    Q = KeyGen.get_big_prime(1024)
    while math.gcd((P-1)*(Q-1), E) != 1:
        P = KeyGen.get_big_prime(1024)
        Q = KeyGen.get_big_prime(1024)
        
    PHI = (P-1)*(Q-1)
    N = P*Q
    #d*e = 1 mod(λ(n))
    # λ(n) is Carmichael's function
    # λ(n) = lcm(p-1, q-1) = ((p-1)/gcd(p-1, q-1))(q-1);
    # Using the first equating we get:
    # e*d = 1 mod(((p-1)/gcd(p-1, q-1))(q-1))
    D = pow(E, -1, PHI)
    return ((N, E), D)

def encrypt(message, public_key):
    m = int.from_bytes(message.encode('utf-8'), byteorder="little")
    n, e = public_key
    return (m**e) % n

def decrypt(message:int, private_key:int, public_key):
    n, e = public_key
    m = (message ** private_key) % n
    return m.to_bytes(math.ceil(m.bit_length() / 8), byteorder="little")