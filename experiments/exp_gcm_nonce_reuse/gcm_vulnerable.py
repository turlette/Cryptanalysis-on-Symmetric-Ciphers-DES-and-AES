from Crypto.Cipher import AES
import os

# Khóa bí mật tĩnh (Chỉ Server biết)
SECRET_KEY = os.urandom(16)

# LỖ HỔNG: Nonce bị hardcode hoặc tái sử dụng (Static Nonce)
# Trong GCM, Nonce (IV) yêu cầu bắt buộc là duy nhất (unique) cho mỗi lần mã hóa với cùng một khóa.
STATIC_NONCE = b"BadNonce1234" # 12 bytes (96 bits)

def encrypt_message(plaintext: str):
    """Mã hóa bản rõ bằng AES-GCM với Nonce bị tái sử dụng."""
    # Khởi tạo cipher với chế độ GCM và Nonce cố định
    cipher = AES.new(SECRET_KEY, AES.MODE_GCM, nonce=STATIC_NONCE)
    ciphertext, tag = cipher.encrypt_and_digest(plaintext.encode('utf-8'))
    return ciphertext, tag

def get_vulnerable_samples():
    """Giả lập việc server mã hóa 2 thông điệp khác nhau nhưng dùng chung cặp (Key, Nonce)."""
    # Plaintext 1 (Giả sử attacker biết trước được một phần nội dung, ví dụ như Header HTTP, Format file chuẩn)
    pt1 = "CONFIDENTIAL_REPORT_ID_9921: We have successfully secured the perimeter."
    
    # Plaintext 2 (Thông điệp mà attacker muốn đánh cắp)
    pt2 = "CONFIDENTIAL_REPORT_ID_9922: The main target coordinates are 45.1N, 9.2E."
    
    ct1, tag1 = encrypt_message(pt1)
    ct2, tag2 = encrypt_message(pt2)
    
    return {
        "pt1": pt1, # Kẻ tấn công biết (Known-plaintext)
        "ct1": ct1.hex(),
        "tag1": tag1.hex(),
        "ct2": ct2.hex(),
        "tag2": tag2.hex()
    }

if __name__ == "__main__":
    print("[*] VULNERABLE AES-GCM ENCRYPTION")
    samples = get_vulnerable_samples()
    print(f"[+] Ciphertext 1: {samples['ct1']}")
    print(f"[+] Ciphertext 2: {samples['ct2']}")
    print("[!] Warning: Both ciphertexts were encrypted with the exact same Nonce!")
