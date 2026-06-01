from Crypto.Cipher import AES
import os

SECRET_KEY = os.urandom(16)

def encrypt_message_secure(plaintext: str):
    """Mã hóa bản rõ bằng AES-GCM với cơ chế sinh Nonce ngẫu nhiên cho mỗi lần."""
    # BẢN VÁ: Sinh Nonce ngẫu nhiên mã hóa an toàn (Cryptographically secure) độ dài 12 bytes.
    # Đảm bảo xác suất trùng lặp Nonce (Collision) gần như bằng 0.
    nonce = os.urandom(12)
    
    cipher = AES.new(SECRET_KEY, AES.MODE_GCM, nonce=nonce)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode('utf-8'))
    return nonce.hex(), ciphertext.hex(), tag.hex()

def demo_secure_encryption():
    pt1 = "CONFIDENTIAL_REPORT_ID_9921: We have successfully secured the perimeter."
    pt2 = "CONFIDENTIAL_REPORT_ID_9922: The main target coordinates are 45.1N, 9.2E."
    
    nonce1, ct1, tag1 = encrypt_message_secure(pt1)
    nonce2, ct2, tag2 = encrypt_message_secure(pt2)
    
    print("[*] SECURE AES-GCM ENCRYPTION")
    print(f"[+] Message 1 -> Nonce: {nonce1}")
    print(f"                 Ciphertext: {ct1[:32]}...")
    print(f"                 Tag: {tag1}")
    print("-" * 50)
    print(f"[+] Message 2 -> Nonce: {nonce2}")
    print(f"                 Ciphertext: {ct2[:32]}...")
    print(f"                 Tag: {tag2}")
    print("-" * 50)
    
    if nonce1 != nonce2:
        print("[!] MITIGATION SUCCESSFUL:")
        print("    Mỗi thông điệp đều sử dụng một Nonce hoàn toàn khác biệt.")
        print("    Keystream XOR Attack và Tag Forgery (Forbidden Attack) LÀ BẤT KHẢ THI!")

if __name__ == "__main__":
    demo_secure_encryption()
