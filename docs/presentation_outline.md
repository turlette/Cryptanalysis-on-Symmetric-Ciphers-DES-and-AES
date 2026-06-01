# Cấu trúc Bài thuyết trình (PowerPoint Outline)
**Đề tài:** Cryptanalysis on Symmetric Ciphers: DES & AES (Thực nghiệm & Phân tích)

Để có một buổi bảo vệ đồ án chỉn chu, thuyết phục và thể hiện được khối lượng công việc khổng lồ bạn đã làm trong 12 tuần, slide báo cáo (khoảng 15-20 slides) nên được cấu trúc theo mạch logic: **Vấn đề -> Cơ sở lý thuyết -> Thực nghiệm -> Giải pháp**.

Dưới đây là cấu trúc chi tiết từng Slide:

---

### Phần 1: Giới thiệu & Đặt vấn đề (3 Slides)

**Slide 1: Tiêu đề (Title Slide)**
- Tên đề tài: Cryptanalysis on Symmetric Ciphers — Thực nghiệm & Phân tích DES và AES trong kịch bản triển khai thực tế.
- Tên sinh viên thực hiện, MSSV.
- Tên Giảng viên hướng dẫn.

**Slide 2: Động lực nghiên cứu (Motivation)**
- Đặt vấn đề: AES là chuẩn mã hóa bất khả chiến bại về mặt toán học, nhưng tại sao các hệ thống dùng AES vẫn liên tục bị hack?
- Điểm nhấn: Lỗ hổng hiếm khi nằm ở thuật toán, mà nằm ở **Cách triển khai (Implementation)** và **Cấu hình (Misconfiguration)**.
- Trình bày tính cấp thiết: 3DES vẫn còn tồn tại ở hệ thống legacy; AES-GCM dễ bị dùng sai nonce; thiết bị IoT dễ bị tấn công vật lý.

**Slide 3: Mục tiêu đồ án (Objectives)**
- Triển khai thành công 4 kịch bản tấn công thực tế vào các hệ thống mã hóa đối xứng.
- Đo lường và đánh giá thời gian/nguồn lực cần thiết để bẻ khóa.
- Đề xuất và kiểm chứng các bản vá (Mitigations) chuẩn công nghiệp.

---

### Phần 2: Thực nghiệm & Phân tích (8 - 10 Slides)
*(Đây là phần "ăn điểm" nhất, hãy dùng ảnh chụp màn hình terminal lúc chạy tool hoặc chèn video demo ngắn vào slide)*

**Slide 4: Tổng quan Lab Setup**
- Giới thiệu môi trường: Python (PyCryptodome), Flask Server (mô phỏng Web API), Docker (môi trường cô lập), Tool phân tích (Pearson CPA).
- (Chèn một sơ đồ minh họa quy trình từ Attacker -> Server).

**Slide 5-6: Experiment A - DES Brute-force**
- **Lý thuyết ngắn:** Không gian khóa DES chỉ có 56-bit.
- **Thực nghiệm:** Mô phỏng bẻ khóa trên môi trường máy tính cá nhân.
- **Kết quả:** Vét cạn thành công. Kết luận DES đã "chết", cần loại bỏ hoàn toàn (thay bằng AES).

**Slide 7-8: Experiment B - Padding Oracle trên AES-CBC**
- **Lý thuyết ngắn:** Giải thích cách Server rò rỉ lỗi `Invalid Padding` (Mã HTTP 500) biến thành "máy tiên tri" (Oracle) giúp Attacker lật bit (Bit-flipping).
- **Thực nghiệm:** Chèn hình ảnh Attacker gửi hàng ngàn truy vấn mạng và dần dần giải mã được chuỗi bí mật mà KHÔNG cần khóa.
- **Bản vá (Mitigation):** Trình bày kỹ thuật *Uniform Error Handling* (trả về lỗi HTTP 400 đồng nhất).

**Slide 9-10: Experiment C - AES-GCM Nonce Reuse**
- **Lý thuyết ngắn:** GCM hoạt động theo cơ chế Stream Cipher. Nếu trùng Nonce -> trùng Keystream -> Attacker dùng phép XOR để giải mã ($C_1 \oplus C_2 = P_1 \oplus P_2$).
- **Thực nghiệm:** Nhấn mạnh thời gian bẻ khóa gần như tức thời ($O(1)$) và lỗ hổng "Forbidden Attack" giả mạo chữ ký (Tag Forgery).
- **Bản vá (Mitigation):** Sinh Nonce hoàn toàn ngẫu nhiên bằng `os.urandom(12)`.

**Slide 11-12: Experiment D - Tấn công Kênh Kề (Side-channel CPA)**
- **Lý thuyết ngắn:** Khi CPU thực hiện tra bảng (S-Box), thời gian và điện năng tiêu thụ bị rò rỉ tỷ lệ với dữ liệu (Hamming Weight).
- **Thực nghiệm:** Attacker thu thập 500 mẫu vật lý (traces) và dùng phân tích tương quan Pearson để tìm ra trọn vẹn Khóa 16-bytes.
- **Bản vá (Mitigation):** Giới thiệu khái niệm **Constant-Time Cryptography** (Thời gian thực thi không đổi).

---

### Phần 3: Kết luận & Khuyến nghị (3 Slides)

**Slide 13: Bảng Tổng hợp Kết quả (Mitigation Comparison)**
- Kẻ 1 bảng so sánh 4 phương pháp tấn công: Tên tấn công | Nguyên nhân | Tốc độ phá mã | Cách phòng chống.

**Slide 14: Bài học rút ra (Conclusion)**
- Thuật toán mạnh (AES-256) không cứu được một lập trình viên ẩu.
- Khuyến nghị 3 nguyên tắc vàng:
  1. Dùng mã hóa có xác thực (AEAD - GCM/ChaCha20) thay cho CBC.
  2. Quản lý Nonce/IV chặt chẽ.
  3. Dùng thư viện chuẩn (đã có Constant-time) thay vì tự viết lại thuật toán.

**Slide 15: Q&A và Tài liệu tham khảo**
- Ghi ngắn gọn 3-4 paper nổi bật nhất (Biham & Shamir, Vaudenay, Lucky13).
- Cảm ơn hội đồng và chuyển sang phần chạy Video Demo thực tế.

---

### Mẹo thiết kế (Design Tips)
1. **Không nhiều chữ:** Slide chỉ gạch đầu dòng từ khóa. Các giải thích phức tạp (như toán học của GHASH hay Pearson) hãy **nói bằng miệng**, dùng sơ đồ hình khối trên Slide để minh họa.
2. **Demo là vua:** Khảo sát sinh viên cho thấy hội đồng rất thích xem Demo. Chắc chắn bạn phải có Video quay lại cảnh chạy script `run_all.py` hoặc quay màn hình song song giữa Server và Attacker.
3. **Màu sắc & Theme:** Chọn một theme có thiên hướng "Cybersecurity" (nền tối, chữ trắng/xanh lá cây code mờ, font chữ monospaced như Consolas cho các đoạn code/log).
