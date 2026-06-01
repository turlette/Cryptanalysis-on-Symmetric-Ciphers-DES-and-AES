from Crypto.Cipher import DES
from Crypto.Util.Padding import pad, unpad
import os

def generate_key() -> bytes:
    """Generate a random 8-byte key for DES.
    Note: DES uses 56 bits of the 64-bit key (every 8th bit is parity).
    """
    return os.urandom(8)

def encrypt_message(plaintext: str, key: bytes) -> bytes:
    """Encrypt a string using DES in ECB mode."""
    cipher = DES.new(key, DES.MODE_ECB)
    padded_text = pad(plaintext.encode('utf-8'), DES.block_size)
    return cipher.encrypt(padded_text)

def decrypt_message(ciphertext: bytes, key: bytes) -> str:
    """Decrypt a ciphertext using DES in ECB mode."""
    cipher = DES.new(key, DES.MODE_ECB)
    decrypted_padded = cipher.decrypt(ciphertext)
    decrypted = unpad(decrypted_padded, DES.block_size)
    return decrypted.decode('utf-8')

if __name__ == "__main__":
    # Test the harness
    test_key = generate_key()
    test_pt = "Hello DES!"
    test_ct = encrypt_message(test_pt, test_key)
    test_decrypted = decrypt_message(test_ct, test_key)
    
    print(f"Plaintext: {test_pt}")
    print(f"Key (hex): {test_key.hex()}")
    print(f"Ciphertext (hex): {test_ct.hex()}")
    print(f"Decrypted: {test_decrypted}")
