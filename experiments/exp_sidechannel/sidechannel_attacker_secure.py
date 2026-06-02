import random
import time
import math
import csv
import os
from aes_timing_secure import simulate_encryption_constant_time
from aes_timing_vulnerable import SBOX, hamming_weight

def pearson_correlation(x, y):
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
    print("="*75)
    print("   THỬ NGHIỆM SIDE-CHANNEL TRÊN BẢN VÁ AN TOÀN (CONSTANT-TIME)   ")
    print("="*75)
    
    num_traces = 500
    print(f"[*] Giai đoạn 1: Thu thập {num_traces} Traces (Mẫu rò rỉ) từ thiết bị An toàn...")
    
    start_time = time.time()
    
    plaintexts = []
    traces_per_byte = {i: [] for i in range(16)}
    
    # 1. Thu thập Trace từ hàm mã hóa an toàn
    for _ in range(num_traces):
        pt = [random.randint(0, 255) for _ in range(16)]
        plaintexts.append(pt)
        
        # BẢN VÁ: Yêu cầu thiết bị an toàn mã hóa. Lúc này, điện năng đo được chỉ là nhiễu trắng!
        leakages = simulate_encryption_constant_time(pt)
        for i in range(16):
            traces_per_byte[i].append(leakages[i])
            
    print("[+] Thu thập hoàn tất. Chuyển sang giai đoạn Phân tích thống kê (CPA)...")
    
    recovered_key = bytearray(16)
    
    # 2. Quá trình phân tích
    for byte_idx in range(16):
        max_corr = 0
        best_guess = 0
        
        actual_traces = traces_per_byte[byte_idx] 
        
        for guess in range(256):
            expected_leakages = []
            for pt in plaintexts:
                sbox_out = SBOX[pt[byte_idx] ^ guess]
                expected_leakages.append(hamming_weight(sbox_out))
                
            corr = abs(pearson_correlation(expected_leakages, actual_traces))
            if corr > max_corr:
                max_corr = corr
                best_guess = guess
                
        recovered_key[byte_idx] = best_guess
        
        char_rep = chr(best_guess) if 32 <= best_guess <= 126 else '?'
        print(f"    -> Đang đoán Byte {byte_idx:02d}: 0x{best_guess:02x} ('{char_rep}')  | Độ tin cậy cực thấp (Corr): {max_corr:.4f}")
        
    end_time = time.time()
    duration = end_time - start_time
    
    print("\n" + "="*75)
    print("[-] TẤN CÔNG THẤT BẠI (ATTACK FAILED)!")
    print(f"[-] Khóa rác thu được:   {recovered_key.hex()}")
    try:
        print(f"[-] Dạng ASCII: '{recovered_key.decode('utf-8', errors='replace')}'")
    except Exception:
        pass
    print("="*75)
    print("GIẢI THÍCH (Dùng để trình diễn):")
    print("Trên bản vá Constant-Time (như AES-NI), việc xử lý không còn phụ thuộc vào dữ liệu.")
    print("Do đó, sóng điện năng (Traces) đo được chỉ là một đường thẳng kèm nhiễu nền tĩnh.")
    print("Hệ số tương quan Pearson (Corr) cực kỳ thấp (~0.05). Thuật toán thống kê bị mù")
    print("hoàn toàn và không thể phân biệt đâu là khóa đúng, dẫn đến kết quả trả về là Rác!")

if __name__ == "__main__":
    main()
