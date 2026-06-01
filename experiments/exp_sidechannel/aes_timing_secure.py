import random

SECRET_KEY = b"SideChannel_123!" # Khóa thực tế

def simulate_encryption_constant_time(plaintext_bytes):
    """
    Giả lập một thiết bị mã hóa AES An Toàn với kiến trúc Constant-Time (ví dụ: AES-NI).
    Trong kiến trúc này, việc xử lý không dùng bảng tra (Look-up Table) phụ thuộc vào dữ liệu.
    Mọi chỉ lệnh tiêu tốn thời gian và điện năng không đổi.
    """
    assert len(plaintext_bytes) == 16
    traces = []
    
    for i in range(16):
        # BẢN VÁ (MITIGATION):
        # Tín hiệu rò rỉ giờ đây chỉ là một nhiễu nền tĩnh (baseline noise)
        # Hoàn toàn KHÔNG TƯƠNG QUAN (Uncorrelated) với Plaintext hay Secret Key.
        noise = random.uniform(3.0, 4.0) 
        traces.append(noise)
        
    return traces

if __name__ == "__main__":
    print("[*] SECURE Constant-Time AES Simulator Loaded.")
    print("[!] Side-channel leakage is completely decoupled from the data being processed.")
    print("[!] Correlation Power Analysis (CPA) / Cache Timing attacks will fail.")
