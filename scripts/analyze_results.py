import os
import csv

def analyze_logs():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    data_dir = os.path.join(base_dir, 'data')
    
    print("="*70)
    print("       BÁO CÁO TỔNG HỢP & PHÂN TÍCH THỐNG KÊ (WEEK 11 - 12)     ")
    print("="*70)
    
    # 1. DES Brute-force
    f_des = os.path.join(data_dir, 'des_bruteforce_log.csv')
    if os.path.exists(f_des):
        with open(f_des, 'r', encoding='utf-8') as f:
            lines = list(csv.reader(f))
            if len(lines) > 1:
                times = [float(row[6]) for row in lines[1:]]
                print(f"[+] Experiment A: DES Brute-force")
                print(f"    - Tổng số lần chạy (Runs): {len(times)}")
                print(f"    - Thời gian bẻ khóa trung bình: {sum(times)/len(times):.4f} giây")
    
    # 2. Padding Oracle
    f_pad = os.path.join(data_dir, 'aes_padding_oracle_log.csv')
    if os.path.exists(f_pad):
        with open(f_pad, 'r', encoding='utf-8') as f:
            lines = list(csv.reader(f))
            if len(lines) > 1:
                times = [float(row[3]) for row in lines[1:]]
                reqs = [int(row[2]) for row in lines[1:]]
                print(f"\n[+] Experiment B: AES-CBC Padding Oracle")
                print(f"    - Tổng số lần chạy (Runs): {len(times)}")
                print(f"    - Số lượng Requests trung bình gửi tới Server: {sum(reqs)/len(reqs):.0f} queries")
                print(f"    - Thời gian giải mã trung bình: {sum(times)/len(times):.4f} giây")
                
    # 3. GCM Nonce Reuse
    f_gcm = os.path.join(data_dir, 'aes_gcm_nonce_reuse_log.csv')
    if os.path.exists(f_gcm):
        with open(f_gcm, 'r', encoding='utf-8') as f:
            lines = list(csv.reader(f))
            if len(lines) > 1:
                times = [float(row[3]) for row in lines[1:]]
                print(f"\n[+] Experiment C: AES-GCM Nonce Reuse")
                print(f"    - Tổng số lần chạy (Runs): {len(times)}")
                print(f"    - Thời gian bẻ khóa trung bình: {sum(times)/len(times):.6f} giây (Độ phức tạp O(1))")

    # 4. Side-channel
    f_sc = os.path.join(data_dir, 'aes_sidechannel_log.csv')
    if os.path.exists(f_sc):
        with open(f_sc, 'r', encoding='utf-8') as f:
            lines = list(csv.reader(f))
            if len(lines) > 1:
                times = [float(row[3]) for row in lines[1:]]
                print(f"\n[+] Experiment D: AES Side-Channel (CPA)")
                print(f"    - Tổng số lần chạy (Runs): {len(times)}")
                print(f"    - Số lượng mẫu (Traces) sử dụng: 500 mẫu vật lý")
                print(f"    - Thời gian phân tích trung bình: {sum(times)/len(times):.4f} giây")

    print("\n" + "="*70)
    print("KẾT LUẬN RÚT RA TỪ KẾT QUẢ THỰC NGHIỆM (MITIGATION ANALYSIS):")
    print("1. Độ an toàn Toán học là CHƯA ĐỦ: Dù AES-128 không thể bị bẻ gãy bằng Brute-force")
    print("   như DES, nhưng nó dễ dàng sụp đổ trước các cuộc tấn công cấu hình (Experiment B, C)")
    print("   và tấn công kênh kề phần cứng (Experiment D).")
    print("2. Lỗ hổng Triển khai (Implementation Bugs): Việc rò rỉ phản hồi lỗi (Error Handling)")
    print("   hoặc rò rỉ điện năng tiêu thụ khiến hàng tỷ USD đầu tư bảo mật trở nên vô nghĩa.")
    print("3. Khuyến nghị Bắt buộc: Cần chuyển dịch sang dùng Mã hóa Xác thực (AEAD - GCM/ChaCha20),")
    print("   kiểm soát chặt chẽ việc sinh Nonce bằng hệ RNG an toàn, và sử dụng thư viện")
    print("   chuyên dụng chạy Constant-Time (như AES-NI) để triệt tiêu lỗ hổng Kênh Kề.")
    print("="*70)

if __name__ == "__main__":
    analyze_logs()
