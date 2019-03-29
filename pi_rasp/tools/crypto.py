from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives import serialization, hashes, padding, hmac
from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
from cryptography.hazmat.primitives.asymmetric import rsa, ec, padding as padd
from cryptography.hazmat.primitives.serialization import load_pem_private_key, load_pem_public_key
from cryptography.exceptions import InvalidSignature
import base64
import os


class Asymmetric(object):
    def create_rsa_keys(self, password, name):
        private_key = rsa.generate_private_key(public_exponent=65537, key_size=4096, backend=default_backend())
        private_pem = private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                                format=serialization.PrivateFormat.PKCS8,
                                                encryption_algorithm=serialization.BestAvailableEncryption(
                                                    str.encode(password)))
        with open(name+'_rsa', 'wb') as f:
            f.write(private_pem)

        public_key = private_key.public_key()
        public_pem = public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                             format=serialization.PublicFormat.SubjectPublicKeyInfo)
        with open(name+'_rsa.pub', 'wb') as f:
            f.write(public_pem)

    def create_ecc_keys(self, password, name):
        private_key = ec.generate_private_key(ec.SECP384R1(), default_backend())
        private_pem = private_key.private_bytes(encoding=serialization.Encoding.PEM,
                                                format=serialization.PrivateFormat.PKCS8,
                                                encryption_algorithm=serialization.BestAvailableEncryption(
                                                    str.encode(password)))
        with open(name+'_ecc', 'wb') as f:
            f.write(private_pem)

            public_key = private_key.public_key()
            public_pem = public_key.public_bytes(encoding=serialization.Encoding.PEM,
                                                 format=serialization.PublicFormat.SubjectPublicKeyInfo)
            with open(name+'_ecc.pub', 'wb') as f:
                f.write(public_pem)

    def load_private_key(self, filename, password):
        with open(filename, 'rb') as f:
            return load_pem_private_key(f.read(), password=str.encode(password), backend=default_backend())

    def load_public_key(self, filename):
        with open(filename, 'rb') as f:
            return load_pem_public_key(f.read(), backend=default_backend())

    def encrypt_msg(self, public_key, msg):
        return base64.b64encode(public_key.encrypt(msg.encode(), padd.OAEP(mgf=padd.MGF1(algorithm=hashes.SHA512()),
                                                                           algorithm=hashes.SHA512(),
                                                                           label=None))).decode()

    def decrypt_msg(self, private_key, msg):
        return private_key.decrypt(base64.b64decode(msg), padd.OAEP(mgf=padd.MGF1(algorithm=hashes.SHA512()),
                                                                            algorithm=hashes.SHA512(), label=None))

    def sign_msg(self, private_key, msg):
        return base64.b64encode(private_key.sign(msg.encode(), ec.ECDSA(hashes.SHA512()))).decode()

    def verify_sign(self, public_key, msg, signature):
        try:
            public_key.verify(base64.b64decode(signature), msg, ec.ECDSA(hashes.SHA512()))
        except InvalidSignature:
            return True
        return False


class Symmetric(object):
    def create_key(self, password=None, iv=None, salt=None):
        if password is None:
            password = os.urandom(32)
        else:
            password = base64.b64decode(password)
        if iv is None:
            iv = os.urandom(16)
        else:
            iv = base64.b64decode(iv)
        if salt is None:
            salt = os.urandom(16)
        else:
            salt = base64.b64decode(salt)
        kdf = PBKDF2HMAC(algorithm=hashes.SHA512(), length=32, salt=salt, iterations=100000, backend=default_backend())
        key = kdf.derive(password)
        return [base64.b64encode(password).decode('utf-8'), base64.b64encode(iv).decode('utf-8'),
                base64.b64encode(salt).decode('utf-8')], Cipher(algorithms.AES(key), modes.CBC(iv),
                                                                backend=default_backend())

    def encrypt_data(self, cipher, data):
        padder = padding.PKCS7(128).padder()
        padded_data = padder.update(data.encode())
        padded_data += padder.finalize()
        encryptor = cipher.encryptor()
        enc_data = encryptor.update(padded_data) + encryptor.finalize()
        return base64.b64encode(enc_data).decode()

    def decrypt_data(self, cipher, data):
        unpadder = padding.PKCS7(128).unpadder()
        decryptor = cipher.decryptor()
        dec_data = decryptor.update(base64.b64decode(data)) + decryptor.finalize()
        final_data = unpadder.update(dec_data)
        return (final_data + unpadder.finalize()).decode()


class HMAC(object):
    def message_digest(self, msg):
        key = os.urandom(32)
        h = hmac.HMAC(key, hashes.SHA512(), backend=default_backend())
        h.update(msg.encode())
        return base64.b64encode(key).decode(), base64.b64encode(h.finalize()).decode()

    def verify_digest(self, key, msg, digest):
        h = hmac.HMAC(base64.b64decode(key), hashes.SHA512(), backend=default_backend())
        h.update(msg.encode())
        try:
            h.verify(base64.b64decode(digest))
        except InvalidSignature:
            return False
        return True
