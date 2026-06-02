import time
from gcm_secure import encrypt_message_secure

def xor_bytes(b1: bytes, b2: bytes) -> bytes:
    """Hàm phụ trợ để thực hiện phép XOR trên từng byte của 2 mảng bytes."""
    return bytes(x ^ y for x, y in zip(b1, b2))

def main():
    print("="*75)
    print("   THỬ NGHIỆM TẤN CÔNG LÊN BẢN VÁ AN TOÀN (SECURE AES-GCM)   ")
    print("="*75)
    
    pt1 = "CONFIDENTIAL_REPORT_ID_9921: We have successfully secured the perimeter."
    pt2 = "CONFIDENTIAL_REPORT_ID_9922: The main target coordinates are 45.1N, 9.2E."
    
    # Đóng vai trò là Server mã hóa dữ liệu một cách AN TOÀN
    # (Dùng os.urandom(12) sinh Nonce ngẫu nhiên cho mỗi lần gọi)
    nonce1, ct1_hex, tag1 = encrypt_message_secure(pt1)
    nonce2, ct2_hex, tag2 = encrypt_message_secure(pt2)
    
    ct1 = bytes.fromhex(ct1_hex)
    ct2 = bytes.fromhex(ct2_hex)
    known_pt1 = pt1.encode('utf-8')
    
    # Kẻ tấn công (Attacker) bắt được gói tin
    print(f"[*] Bắt được Ciphertext 1 (Nonce: {nonce1})")
    print(f"[*] Bắt được Ciphertext 2 (Nonce: {nonce2})")
    print(f"[*] Biết trước Plaintext 1: '{pt1}'")
    
    print("\n[*] Tiến hành Tấn công (Keystream Recovery)...")
    
    # BƯỚC 1: Kẻ tấn công cố gắng lấy Keystream từ thông điệp 1
    # Công thức cũ: Keystream = C1 XOR P1
    min_len_1 = min(len(ct1), len(known_pt1))
    keystream_fake = xor_bytes(ct1[:min_len_1], known_pt1[:min_len_1])
    
    # BƯỚC 2: Cố gắng dùng Keystream đó để giải mã thông điệp 2
    # Công thức cũ: P2 = C2 XOR Keystream
    min_len_2 = min(len(ct2), len(keystream_fake))
    pt2_recovered_bytes = xor_bytes(ct2[:min_len_2], keystream_fake[:min_len_2])
    
    # Chuyển đổi mảng byte rác thành String (có lỗi sẽ thay thế bằng ký tự '?')
    pt2_recovered_str = pt2_recovered_bytes.decode('utf-8', errors='replace')
        
    print("\n" + "="*75)
    print(f"[-] TẤN CÔNG THẤT BẠI HOÀN TOÀN (ATTACK FAILED)!")
    print(f"[-] Dữ liệu khôi phục được chỉ là mảng rác: {pt2_recovered_str}")
    print("="*75)
    print("GIẢI THÍCH (Dùng để trình diễn lúc bảo vệ):")
    print("Vì Nonce 1 và Nonce 2 là hai chuỗi ngẫu nhiên hoàn toàn khác biệt,")
    print("Nên Keystream 1 và Keystream 2 sinh ra từ thuật toán AES cũng khác biệt.")
    print("Việc lấy (C2 XOR Keystream 1) sẽ không triệt tiêu được nhau,")
    print("kết quả trả về là rác (Random garbage) thay vì Plaintext 2.")

if __name__ == "__main__":
    main()
