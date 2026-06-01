import random
import time
import math
import csv
import os
from aes_timing_vulnerable import simulate_encryption_with_leakage, SBOX, hamming_weight

def pearson_correlation(x, y):
    """
    Tính hệ số tương quan Pearson giữa 2 tập dữ liệu.
    Hệ số càng gần 1 (hoặc -1) thì x và y càng có quan hệ tuyến tính mạnh.
    """
    n = len(x)
    sum_x = sum(x)
    sum_y = sum(y)
    sum_x_sq = sum(xi*xi for xi in x)
    sum_y_sq = sum(yi*yi for yi in y)
    psum = sum(xi*yi for xi, yi in zip(x, y))
    
    num = psum - (sum_x * sum_y / n)
    den = math.sqrt((sum_x_sq - sum_x**2 / n) * (sum_y_sq - sum_y**2 / n))
    if den == 0:
        return 0
    return num / den

def main():
    print("="*70)
    print("     SIDE-CHANNEL: CORRELATION POWER ANALYSIS (CPA) ATTACK    ")
    print("="*70)
    
    num_traces = 500 # Số lượng mẫu (traces) thu thập từ thiết bị
    print(f"[*] Giai đoạn 1: Thu thập {num_traces} Traces (Mẫu rò rỉ) từ thiết bị...")
    
    start_time = time.time()
    
    plaintexts = []
    # Lưu trữ trace (tín hiệu điện/timing) cho từng byte vị trí (0-15)
    traces_per_byte = {i: [] for i in range(16)}
    
    # 1. Quá trình thu thập Trace (Data Acquisition)
    for _ in range(num_traces):
        # Sinh 1 khối plaintext ngẫu nhiên
        pt = [random.randint(0, 255) for _ in range(16)]
        plaintexts.append(pt)
        
        # Yêu cầu thiết bị mã hóa và đo đạc tín hiệu rò rỉ (bằng oscilloscope giả lập)
        leakages = simulate_encryption_with_leakage(pt)
        for i in range(16):
            traces_per_byte[i].append(leakages[i])
            
    print("[+] Thu thập hoàn tất. Chuyển sang giai đoạn Phân tích thống kê (CPA)...")
    print("[*] Giai đoạn 2: Phân tích tương quan Pearson để tìm Khóa...")
    
    recovered_key = bytearray(16)
    
    # 2. Quá trình phân tích (Data Analysis) - Xử lý độc lập từng byte của khóa
    for byte_idx in range(16):
        max_corr = 0
        best_guess = 0
        
        actual_traces = traces_per_byte[byte_idx] # Dữ liệu điện năng thực tế thu được
        
        # Duyệt qua 256 trường hợp có thể có của 1 byte Khóa
        for guess in range(256):
            expected_leakages = []
            # Với giả định 'guess' là khóa đúng, tính toán xem điện năng lý thuyết sẽ là bao nhiêu
            for pt in plaintexts:
                sbox_out = SBOX[pt[byte_idx] ^ guess]
                expected_leakages.append(hamming_weight(sbox_out))
                
            # So sánh mức độ tương đồng giữa "Điện năng lý thuyết" và "Điện năng đo được thực tế"
            corr = abs(pearson_correlation(expected_leakages, actual_traces))
            if corr > max_corr:
                max_corr = corr
                best_guess = guess
                
        recovered_key[byte_idx] = best_guess
        
        # In kết quả từng byte
        char_rep = chr(best_guess) if 32 <= best_guess <= 126 else '?'
        print(f"    -> Khôi phục Byte {byte_idx:02d}: 0x{best_guess:02x} ('{char_rep}')  | Độ tin cậy (Corr): {max_corr:.4f}")
        
    end_time = time.time()
    duration = end_time - start_time
    
    print("\n" + "="*70)
    print("[+] ATTACK SUCCESSFUL! (Without Brute-forcing all 2^128 keys)")
    print(f"[+] Toàn bộ Khóa AES được khôi phục (Hex):   {recovered_key.hex()}")
    try:
        print(f"[+] Toàn bộ Khóa AES được khôi phục (ASCII): '{recovered_key.decode('utf-8')}'")
    except Exception:
        pass
    print(f"[*] Thời gian thực hiện: {duration:.2f} giây")
    print("="*70 + "\n")
    
    # Ghi log kết quả
    log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data'))
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'aes_sidechannel_log.csv')
    
    file_exists = os.path.isfile(log_file)
    with open(log_file, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['Timestamp', 'Recovered Key (hex)', 'Traces Used', 'Time (s)'])
        writer.writerow([
            time.strftime("%Y-%m-%d %H:%M:%S"),
            recovered_key.hex(),
            num_traces,
            round(duration, 4)
        ])
    print(f"[+] Kết quả đã lưu vào: {os.path.relpath(log_file, os.path.dirname(__file__))}")

if __name__ == "__main__":
    main()
