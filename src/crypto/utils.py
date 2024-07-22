from cryptography.hazmat.primitives.asymmetric import rsa, padding
from cryptography.hazmat.primitives import hashes
from cryptography.hazmat.backends import default_backend
from cryptography.hazmat.primitives.asymmetric.rsa import RSAPublicKey, RSAPrivateKey
from cryptography.hazmat.primitives import serialization

class CryptoUtils:
    @staticmethod
    def generate_rsa_keys():
        private_key = rsa.generate_private_key(
            public_exponent=65537,
            key_size=2048,
            backend=default_backend()
        )
        public_key = private_key.public_key()
        
        private_pem = private_key.private_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PrivateFormat.PKCS8,
            encryption_algorithm=serialization.NoEncryption()
        )
        public_pem = public_key.public_bytes(
            encoding=serialization.Encoding.PEM,
            format=serialization.PublicFormat.SubjectPublicKeyInfo
        )
        
        return {
            "private_key": private_pem.decode(),
            "public_key": public_pem.decode()
        }
    
    @staticmethod
    def encrypt_message(message: str, recipient_public_key: RSAPublicKey) -> bytes:
        encrypted_message = recipient_public_key.encrypt(
            message.encode(),
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        )
        return encrypted_message
    
    @staticmethod
    def load_private_key(private_key_str: str) -> RSAPrivateKey:
        private_key = serialization.load_pem_private_key(
            private_key_str.encode('utf-8'),
            password=None,
            backend=default_backend()
        )
        return private_key
    
    @staticmethod
    def decrypt_message(encrypted_message: bytes, recipient_private_key: RSAPrivateKey) -> str:
        decrypted_message = recipient_private_key.decrypt(
            encrypted_message,
            padding.OAEP(
                mgf=padding.MGF1(algorithm=hashes.SHA256()),
                algorithm=hashes.SHA256(),
                label=None
            )
        ).decode()
        return decrypted_message

    
    @staticmethod
    def load_public_key(public_key_str: str) -> RSAPublicKey:
        public_key = serialization.load_pem_public_key(
            public_key_str.encode('utf-8'),
            backend=default_backend()
        )
        return public_key