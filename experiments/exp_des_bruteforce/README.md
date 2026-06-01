# Experiment A: DES Brute-force Simulator

Bài thực nghiệm này minh hoạ quá trình tấn công brute-force để tìm khóa mã hóa DES (với độ dài hiệu dụng là 56-bit).

## Tại sao DES không còn an toàn?

Thuật toán DES (Data Encryption Standard) sử dụng không gian khóa là 56-bit, tương đương với $2^{56}$ (khoảng 72 triệu tỉ) trường hợp khóa có thể có. Vào thời điểm mới được ban hành vào những năm 1970, đây là một con số an toàn trước khả năng tính toán của máy tính thời bấy giờ. 

Tuy nhiên, với sự phát triển của công nghệ và sức mạnh tính toán hiện đại (đặc biệt là sự ra đời của GPU, FPGA, ASICs và điện toán đám mây), việc vét cạn toàn bộ $2^{56}$ khóa đã trở nên khả thi về mặt thực tiễn. Thực tế vào năm 1998, tổ chức Electronic Frontier Foundation (EFF) đã chế tạo một cỗ máy (Deep Crack) phá được mã DES trong chưa đầy 3 ngày. Hiện tại, với một hệ thống GPU cluster thông thường, thời gian này có thể chỉ còn vài giờ hoặc vài phút. Do giới hạn về không gian khóa quá nhỏ, DES hiện bị coi là không an toàn và đã được NIST loại bỏ, thay thế bởi tiêu chuẩn AES mạnh mẽ hơn.

## Cách chạy thử nghiệm

**Bước 1:** Đảm bảo bạn đã cài đặt thư viện `pycryptodome` (được sử dụng cho các thao tác mã hóa):
```bash
pip install pycryptodome
```

**Bước 2:** Di chuyển vào thư mục chứa experiment và chạy script mô phỏng:
```bash
cd experiments/exp_des_bruteforce
python bruteforce_simulator.py
```

**Lưu ý:** Script mô phỏng này mặc định đã được thiết lập giả lập brute-force 2 bytes cuối của khóa (Difficulty: 2 bytes tương đương $2^{16}$ tổ hợp) nhằm mục đích có thể hoàn thành trong chưa tới 1 giây trên máy tính cá nhân. Bạn có thể thay đổi biến `difficulty_bytes` trong file `bruteforce_simulator.py` thành `3` (tốn vài giây) hoặc lớn hơn để tự trải nghiệm.

**Bước 3:** Kiểm tra log kết quả:
Toàn bộ thông số đo lường bao gồm: Khóa gốc, Khóa tìm được, Thời gian chạy, Tốc độ thử khóa (keys/second) được tự động xuất ra file `data/des_bruteforce_log.csv` nằm ở thư mục gốc. Mở file để xem.