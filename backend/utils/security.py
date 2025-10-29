from cryptography.fernet import Fernet
import os

# É crucial que esta chave seja carregada de uma variável de ambiente em produção
ENCRYPTION_KEY = os.environ.get("ENCRYPTION_KEY", Fernet.generate_key().decode())

fernet = Fernet(ENCRYPTION_KEY.encode())

def encrypt_data(data):
    """Criptografa os dados (de string para bytes)."""
    if not isinstance(data, str):
        raise TypeError("Apenas strings podem ser criptografadas.")
    return fernet.encrypt(data.encode())

def decrypt_data(encrypted_data):
    """Descriptografa os dados (de bytes para string)."""
    if not isinstance(encrypted_data, bytes):
        raise TypeError("Apenas bytes podem ser descriptografados.")
    return fernet.decrypt(encrypted_data).decode()

