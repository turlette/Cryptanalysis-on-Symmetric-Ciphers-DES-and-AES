# Experiment B: AES-CBC Padding Oracle

Bài thực nghiệm này minh họa lỗ hổng Padding Oracle rất phổ biến trong các hệ thống sử dụng AES chế độ CBC mà không thực hiện xác thực thông điệp (ví dụ không sử dụng MAC).

## Lỗ hổng là gì?
Khi giải mã AES-CBC, hệ thống sẽ thực hiện quá trình gỡ bỏ padding (unpad). Nếu cấu trúc padding không hợp lệ, ứng dụng thường sẽ ném ra lỗi (exception). Nếu server phản hồi lại lỗi này cho người dùng (ví dụ: HTTP 500 "Invalid Padding"), kẻ tấn công (attacker) có thể dựa vào đó để đóng vai trò như một "Oracle" (máy tiên tri). Bằng cách gửi liên tục các ciphertext bị thay đổi (bit-flipping) và quan sát phản hồi lỗi của server, attacker có thể khôi phục lại hoàn toàn Plaintext mà **KHÔNG CẦN** biết khóa bí mật (Secret Key).

## Cấu trúc thư mục
- `server.py`: API Server chứa lỗ hổng rò rỉ lỗi Padding.
- `attacker.py`: Script tự động khai thác lỗ hổng để giải mã ciphertext từng byte một.
- `server_patched.py`: API Server đã được vá lỗi bằng kỹ thuật *Uniform Error Handling* (Xử lý lỗi đồng nhất).

## Cách chạy thử nghiệm

**Bước 1: Cài đặt thư viện (nếu chưa có)**
Đảm bảo bạn đã cài `Flask` để dựng server và `requests` để gửi request.
```bash
pip install pycryptodome flask requests
```

**Bước 2: Bật Server có lỗ hổng (Mở Terminal 1)**
Tại thư mục gốc, chuyển vào thư mục bài lab và chạy server:
```bash
cd experiments/exp_padding_oracle
python server.py
```
*(Server sẽ bắt đầu lắng nghe ở cổng 5000)*

**Bước 3: Chạy Script Tấn Công (Mở Terminal 2)**
Mở một cửa sổ Terminal mới, chuyển vào thư mục bài lab và chạy attacker:
```bash
cd experiments/exp_padding_oracle
python attacker.py
```
*(Bạn sẽ thấy attacker gửi hàng nghìn request, từ từ giải mã từng block. Sau khi thành công, kết quả sẽ tự động lưu vào file `../../data/aes_padding_oracle_log.csv`)*

**Bước 4: Kiểm chứng Bản vá (Mitigation)**
Trở lại Terminal 1, bấm `Ctrl+C` để tắt `server.py`. Sau đó khởi động server đã vá lỗi:
```bash
python server_patched.py
```
Quay lại Terminal 2 và chạy lại lệnh `python attacker.py`. Lúc này cuộc tấn công sẽ lập tức thất bại (bị Abort), bởi vì server đã xử lý lỗi đồng nhất (trả về HTTP 400 cho mọi tình huống bất thường), triệt tiêu hoàn toàn khả năng đóng vai trò Oracle.