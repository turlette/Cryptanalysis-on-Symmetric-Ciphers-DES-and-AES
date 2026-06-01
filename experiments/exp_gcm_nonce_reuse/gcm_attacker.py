import time
import csv
import os
from gcm_vulnerable import get_vulnerable_samples

def xor_bytes(b1: bytes, b2: bytes) -> bytes:
    """Hàm phụ trợ để thực hiện phép XOR trên từng byte của 2 mảng bytes."""
    return bytes(x ^ y for x, y in zip(b1, b2))

def main():
    print("="*70)
    print("        AES-GCM NONCE REUSE ATTACK (KEYSTREAM RECOVERY)        ")
    print("="*70)
    
    # Lấy dữ liệu mô phỏng từ server
    samples = get_vulnerable_samples()
    ct1 = bytes.fromhex(samples['ct1'])
    ct2 = bytes.fromhex(samples['ct2'])
    known_pt1 = samples['pt1'].encode('utf-8')
    
    print(f"[*] Intercepted Ciphertext 1 (len: {len(ct1)}): {ct1.hex()[:32]}...")
    print(f"[*] Intercepted Ciphertext 2 (len: {len(ct2)}): {ct2.hex()[:32]}...")
    print(f"[*] Known Plaintext 1 (e.g., File Header): '{samples['pt1']}'")
    
    print("\n[*] Commencing Attack...")
    start_time = time.time()
    
    # BƯỚC 1: Khôi phục Keystream
    # Trong mã hóa luồng (GCM hoạt động như luồng mã thông qua mode CTR ở lõi):
    # C1 = P1 XOR Keystream  =>  Keystream = C1 XOR P1
    # Số byte keystream khôi phục được sẽ bằng độ dài của phần Plaintext đã biết.
    min_len_1 = min(len(ct1), len(known_pt1))
    keystream = xor_bytes(ct1[:min_len_1], known_pt1[:min_len_1])
    
    print(f"[+] Recovered Keystream (first {min_len_1} bytes): {keystream.hex()[:32]}...")
    
    # BƯỚC 2: Dùng Keystream khôi phục Plaintext 2
    # C2 = P2 XOR Keystream  =>  P2 = C2 XOR Keystream
    min_len_2 = min(len(ct2), len(keystream))
    pt2_recovered_bytes = xor_bytes(ct2[:min_len_2], keystream[:min_len_2])
    
    end_time = time.time()
    duration = end_time - start_time
    
    try:
        pt2_recovered_str = pt2_recovered_bytes.decode('utf-8')
    except Exception:
        pt2_recovered_str = pt2_recovered_bytes.decode('utf-8', errors='ignore')
        
    print("\n" + "="*70)
    print(f"[+] ATTACK SUCCESSFUL IN {duration:.6f} SECONDS!")
    print(f"[+] Secret Plaintext 2 Recovered: '{pt2_recovered_str}'")
    print("="*70 + "\n")
    
    # BƯỚC 3: Giải thích về Tag Forgery (Forbidden Attack)
    print("--- BEYOND CONFIDENTIALITY: THE FORBIDDEN ATTACK (TAG FORGERY) ---")
    print("Việc dùng lại Nonce trong GCM không chỉ làm lộ Keystream (mất Confidentiality),")
    print("mà còn làm sụp đổ hoàn toàn cơ chế xác thực (Authenticity).")
    print("Auth Tag trong GCM được tính bằng một đa thức trên trường Galois GF(2^128).")
    print("Nếu 2 thông điệp dùng chung Nonce, ta có 2 phương trình với Auth Tag T1, T2.")
    print("Kẻ tấn công có thể XOR (T1 XOR T2) để triệt tiêu thành phần mặt nạ (Auth Mask).")
    print("Kết quả để lại một đa thức mà chỉ có MỘT ẨN SỐ DUY NHẤT là khóa xác thực (GHASH key 'H').")
    print("Bằng cách tìm nghiệm của đa thức này, kẻ tấn công sẽ lấy được H.")
    print("Khi có H, kẻ tấn công có thể dễ dàng TẠO RA (FORGE) các Tag hợp lệ cho BẤT KỲ")
    print("ciphertext giả mạo nào gửi lên server, đánh lừa server tin đó là dữ liệu chuẩn!\n")
    
    # Ghi Log
    log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data'))
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'aes_gcm_nonce_reuse_log.csv')
    
    file_exists = os.path.isfile(log_file)
    with open(log_file, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['Timestamp', 'Recovered Plaintext', 'Attack Type', 'Time (s)'])
        writer.writerow([
            time.strftime("%Y-%m-%d %H:%M:%S"),
            pt2_recovered_str,
            "Keystream Recovery",
            f"{duration:.6f}"
        ])
    print(f"[+] Results logged to: {os.path.relpath(log_file, os.path.dirname(__file__))}")

if __name__ == "__main__":
    main()
