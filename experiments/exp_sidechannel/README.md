# Experiment D: Side-channel Attack (Power / Timing Traces)

Bài thực nghiệm này minh họa sức mạnh tàn phá của các cuộc tấn công **Side-channel (Kênh kề)**. Cụ thể là phương pháp Phân tích năng lượng/thời gian thông qua sự tương quan **(Correlation Power Analysis - CPA)** trên các mô hình AES dạng tra bảng (Table-based AES) kém an toàn.

## Lỗ hổng là gì?
Thuật toán mã hóa dù an toàn về mặt toán học đến đâu cũng có thể bị phá vỡ thông qua **cách thức nó được lập trình và chạy trên phần cứng**. 
Trong các thư viện AES cũ hoặc cài đặt IoT yếu, phép thay thế S-Box (`SubBytes`) thường được thực thi bằng cách tra mảng (Lookup Table) trong bộ nhớ. 
Thời gian truy xuất bộ nhớ (Cache hit/miss) hoặc lượng điện năng tiêu thụ để tải byte dữ liệu đó lên thanh ghi tỷ lệ thuận với số bit `1` của giá trị đó (Hamming Weight). 
Kẻ tấn công có thể thu thập các mẫu (traces) tín hiệu vật lý này và dùng thống kê Pearson để xác định ra chính xác Khóa bí mật.

## Cấu trúc thư mục
- `aes_timing_vulnerable.py`: Module giả lập thiết bị IoT bị rò rỉ tín hiệu (trả về giá trị điện năng phụ thuộc vào dữ liệu S-Box).
- `sidechannel_attacker.py`: Script tự động sinh dữ liệu, thu thập 500 mẫu (traces) và dùng phân tích Pearson CPA để khôi phục toàn bộ 16 bytes Khóa AES trong tích tắc.
- `aes_timing_secure.py`: Bản vá mô phỏng AES Constant-Time (như AES-NI), nơi tín hiệu điện năng tiêu thụ luôn không đổi bất kể dữ liệu.

## Hướng dẫn chạy thử nghiệm

**Bước 1:** Khởi chạy cuộc tấn công để khôi phục khóa:
Mở Terminal, di chuyển vào thư mục bài lab:
```bash
cd experiments/exp_sidechannel
python sidechannel_attacker.py
```
*(Chờ trong giây lát, bạn sẽ thấy attacker đối chiếu tín hiệu từng byte và phá khóa với độ tin cậy được in ra chi tiết. Tốc độ thực hiện chỉ tính bằng giây, hoàn toàn bỏ qua sức mạnh toán học của AES-128!)*

**Bước 2:** Đọc source code bản vá tại `aes_timing_secure.py`
Nếu bạn thay thế hàm `simulate_encryption_with_leakage` bằng hàm ở `aes_timing_secure.py`, tín hiệu rò rỉ giờ chỉ còn là nhiễu ngẫu nhiên. Mọi thuật toán thống kê của Attacker sẽ lập tức bị vô hiệu hóa vì không còn tìm thấy sự tương quan (Correlation).