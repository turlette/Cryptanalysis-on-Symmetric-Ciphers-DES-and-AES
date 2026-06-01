# Experiment C: AES-GCM Nonce Reuse

Bài thực nghiệm này minh họa hậu quả thảm khốc của việc cấu hình sai chế độ AES-GCM (Galois/Counter Mode) bằng cách **tái sử dụng Nonce (Initialization Vector)** cho nhiều tin nhắn mã hóa cùng một khóa.

## Lỗ hổng (The Vulnerability)
GCM hoạt động dựa trên cơ chế Counter (CTR) mode ở phần lõi mã hóa (Confidentiality). Trong mode CTR, `Ciphertext = Plaintext XOR Keystream`. 
Nếu một cặp `(Key, Nonce)` được dùng lại, Keystream sinh ra sẽ giống hệt nhau cho cả hai tin nhắn.
Khi đó:
`Ciphertext1 XOR Ciphertext2 = Plaintext1 XOR Plaintext2`
Chỉ cần kẻ tấn công biết (hoặc đoán được) một phần Plaintext1 (như Header file, định dạng chuẩn), họ có thể dễ dàng dùng phép toán XOR để lật ngược lại toàn bộ nội dung bí mật của Plaintext2.

Ngoài ra, tái sử dụng Nonce trong GCM còn dẫn đến **"Forbidden Attack"**: cho phép kẻ tấn công giải được khóa nội bộ (GHASH key) để giả mạo (forge) chữ ký xác thực (Authentication Tag) cho mọi dữ liệu giả mạo gửi lên hệ thống.

## Cấu trúc thư mục
- `gcm_vulnerable.py`: Hàm mã hóa bị cấu hình sai (cố định Nonce).
- `gcm_attacker.py`: Script khai thác sự trùng lặp Nonce để lấy cắp thông tin tức thì.
- `gcm_secure.py`: Mã nguồn đã vá, sử dụng `os.urandom(12)` để sinh Nonce độc nhất.

## Hướng dẫn chạy thử nghiệm

**Bước 1:** Bật Terminal, di chuyển vào thư mục bài lab:
```bash
cd experiments/exp_gcm_nonce_reuse
```

**Bước 2:** Chạy mã khai thác tự động:
```bash
python gcm_attacker.py
```
*(Bạn sẽ thấy tốc độ lấy lại bản rõ là ngay lập tức - chỉ khoảng 0.000x giây so với hàng giờ/ngày nếu làm Brute-force).*

**Bước 3:** Chạy bản vá lỗ hổng:
```bash
python gcm_secure.py
```
*(Bản vá minh họa việc các Nonce sinh ngẫu nhiên sẽ khác nhau, từ đó đập tan mọi giả định XOR của kẻ tấn công).*