
import sys
import random
import socket

# Uncomment to run on VMs
# import Crypto
# from Crypto.Cipher import AES

# Comment to run on VMs
import crypto
sys.modules['Crypto'] = crypto
from crypto.Cipher import AES


class Connection:
    _buffer_size = 128
    _socket = None
    key = None

    # Stablish Connection

    def wait_connection_on_port(self, port:int) -> None:
        bindsocket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        bindsocket.bind(('', port))
        bindsocket.listen()
        print(f'Listening on port {port}')
        self._socket, fromaddr = bindsocket.accept()
        bindsocket.close()

    def connect_to(self, ip:str, port:int):
        self._socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
        self._socket.connect((ip, port))
        print(f'Connected to {ip}:{port}')

    def resolve_domain(domain):
        return socket.gethostbyname(domain)

    # Socket IO

    def write_bytes(self, bytes_to_write:bytes) -> None:
        print(f'Writing >> {bytes_to_write}')
        bytes_to_write += b'|'
        while len(bytes_to_write)<self._buffer_size:
            bytes_to_write += b'\\'
        self._socket.sendall(bytes_to_write)

    def read_bytes(self) -> bytes:
        bytes_read = None
        while bytes_read is None:
            bytes_read = self._socket.recv(self._buffer_size)
        bytes_read = bytes_read.split(b'|')[:-1]
        bytes_read = b'|'.join(bytes_read)
        print(f'Reading << {bytes_read}')
        return bytes_read

    def write_string(self, msg:str) -> None:
        self.write_bytes(msg.encode('ASCII'))

    def close_socket(self) -> None:
        self._socket.close()

    def remove_header(self, all_bytes:bytes) -> bytes:
        msg_bytes = all_bytes.split(b'|')[1:]
        msg_bytes = b'|'.join(msg_bytes)
        return msg_bytes


    # Encryption

    def write_encrypted_msg(self, msg:str) -> None:
        msg_bytes = msg.encode('ASCII')
        msg_bytes = self.encrypt(msg_bytes)
        bytes_to_write = b'EncryptedMsg|' + msg_bytes
        self.write_bytes(bytes_to_write)

    def read_encrypted_msg(self) -> str:
        msg_bytes = self.read_bytes()
        msg_bytes = self.remove_header(msg_bytes)
        msg_bytes = self.decrypt(msg_bytes)
        return msg_bytes.decode('ASCII')

    def encrypt(self, msg_bytes:bytes) -> bytes:
        cipher = AES.new(self.key, AES.MODE_CFB, iv=(0).to_bytes(16, 'big'))
        encrypted_bytes = cipher.encrypt(msg_bytes)
        return encrypted_bytes

    def decrypt(self, msg_bytes:bytes) -> bytes:
        cipher = AES.new(self.key, AES.MODE_CFB, iv=(0).to_bytes(16, 'big'))
        encrypted_bytes = cipher.decrypt(msg_bytes)
        return encrypted_bytes


    # Diffie - Hellman

    # Prime number q: 7727
    # Primitive root a: 1222

    # A -> B: Prime|q
    # A -> B: Root|a

    # A: XA = random.randint(1, q)
    # A: YA = pow(a,XA,q)
    # A -> B: PKA|YA

    # B: XB = random.randint(1, q)
    # B: YB = pow(a,XB,q)
    # B -> A: PKB|YB

    # A: K = pow(YB,XA,q)
    # B: K = pow(YA,XB,q)

    def start_diffie_hellman(self):
        # Prime number
        q = 7727
        # Primitive root
        a = 1222
        self.write_string(f'Prime|{q}')
        self.write_string(f'Root|{a}')
        # Public and private Key of A
        XA = random.randint(1, q-1)
        YA = pow(a,XA,q)
        self.write_string(f'PKA|{YA}')
        # Public Key of B
        key_msg = self.read_bytes()
        YB = int(self.remove_header(key_msg))
        # Simmetric Key
        K = pow(YB,XA,q)
        self.set_key(K)


    def accept_diffie_hellman(self):
        # Prime number
        prime_msg = self.read_bytes()
        q = int(self.remove_header(prime_msg))
        # Primitive root
        root_msg = self.read_bytes()
        a = int(self.remove_header(root_msg))
        # Public and private Key of B
        XB = random.randint(1, q-1)
        YB = pow(a,XB,q)
        # Public Key of A
        key_msg = self.read_bytes()
        YA = int(self.remove_header(key_msg))
        self.write_string(f'PKB|{YB}')
        # Simmetric Key
        K = pow(YA,XB,q)
        self.set_key(K)


    def set_key(self, K:int):
        self.key = K.to_bytes(16, 'big')


