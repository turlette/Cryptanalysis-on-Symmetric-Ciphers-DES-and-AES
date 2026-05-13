# Literature Summary

## 1. Differential Cryptanalysis (Biham & Shamir, 1993)

- **Key idea**: Phương pháp thám mã sai phân (differential cryptanalysis) phân tích cặp bản rõ và bản mã với các "difference" (sự khác biệt) được kiểm soát. Bằng cách theo dõi sự lan truyền của difference qua các vòng mã hóa, có thể xác định key với xác suất cao hơn brute-force [citation:1].

- **Contribution**: 
  - Là attack thành công đầu tiên phá vỡ DES 16 vòng nhanh hơn exhaustive search
  - Giới thiệu khái niệm characteristic, signal-to-noise ratio, và structures
  - Được áp dụng thành công cho FEAL, Khafre, REDOC-II, LOKI, Lucifer và nhiều hash functions [citation:7]

- **Relevance to our work**: Nền tảng cho nhiều side-channel attacks hiện đại. Hiểu differential cryptanalysis giúp phân tích điểm yếu của các cipher khác.

- **Notes**: 
  - Book chính thức: "Differential Cryptanalysis of the Data Encryption Standard" (Springer, 1993)
  - DOI: 10.1007/978-1-4613-9314-6 [citation:7]


## 2. Linear Cryptanalysis (Matsui, 1994)

- **Key idea**: Phương pháp thám mã tuyến tính (linear cryptanalysis) tìm xấp xỉ tuyến tính giữa bản rõ, bản mã và key. Sử dụng các linear approximation của S-boxes để khôi phục key bits [citation:2].

- **Contribution**: 
  - Attack DES 16 vòng thành công với 2^43 known plaintexts (trong thực nghiệm)
  - Thực hiện trên 12 máy tính trong 50 ngày: 40 ngày sinh plaintexts + 10 ngày tìm key [citation:8]
  - Đạt toàn bộ 56 bits key

- **Relevance to our work**: Song song với differential cryptanalysis ở cấp độ cấu trúc [citation:6]. Cả hai đều là nền tảng cho modern cryptanalysis.

- **Notes**: 
  - Paper gốc: "The First Experimental Cryptanalysis of the Data Encryption Standard" (Crypto 1994)
  - Có thể tìm phiên bản conference từ Eurocrypt'93: "Linear Cryptanalysis Method for DES Cipher"


## 3. Padding Oracle Attack (Vaudenay, 2002)

- **Key idea**: Tấn công dựa trên padding oracle - một hệ thống cho biết padding của ciphertext có hợp lệ hay không. Từ thông tin này (side channel), attacker có thể decrypt dữ liệu mà không cần key [citation:3].

- **Contribution**:
  - Phát hiện vulnerability trong CBC-mode encryption với PKCS#5 padding
  - Chỉ ra rằng chỉ cần oracle trả lời "padding correct/incorrect" là đủ để phá vỡ bảo mật
  - Được mở rộng thành POODLE attack trên SSL 3.0 (2014) [citation:9]

- **Relevance to our work**: Là ví dụ kinh điển về side-channel attack từ error messages. Cho thấy thông tin tưởng chừng vô hại (padding error) có thể bị khai thác.

- **Notes**: 
  - Paper gốc: "Security of Padding Schemes in CBC-Mode Encryption" (Eurocrypt 2002)
  - Ứng dụng thực tế: tấn công TLS/SSL, web frameworks [citation:3]
  - Xem thêm: Rizzo & Duong (2010) - "Practical padding oracle attacks" (WOOT)


## 4. Cache Timing Attack (Bernstein, 2005)

- **Key idea**: Tận dụng sự khác biệt thời gian truy cập cache (cache hit ~ vài chu kỳ, cache miss ~ hàng trăm chu kỳ). Khi AES implementation truy cập S-box, cache misses sẽ leak thông tin về key [citation:4].

- **Contribution**:
  - Chứng minh có thể khôi phục AES key từ timing measurements
  - Chỉ ra NIST đã bỏ qua vấn đề này trong quá trình chọn AES
  - Đề xuất hướng giải quyết cho CPU designers [citation:10]

- **Relevance to our work**: Ví dụ quan trọng về hardware side-channel attack. Khác với các attack toán học (differential/linear), attack này khai thác implementation thực tế.

- **Notes**: 
  - PDF trực tiếp: http://cr.yp.to/antiforgery/cachetiming-20050414.pdf [citation:4]
  - Có thể thực thi từ xa qua network (remote timing attack)
  - Đặt ra yêu cầu về constant-time implementations cho cryptographic code


## Next steps
- [x] Tìm kiếm 4 key papers
- [ ] Đọc chi tiết từng paper (ưu tiên abstract + introduction + kết luận trước)
- [ ] Điền nội dung chi tiết hơn vào các mục trên
- [ ] So sánh chéo 4 phương pháp: điểm mạnh, điểm yếu, điều kiện tấn công
- [ ] Bổ sung các paper liên quan (mở rộng từ mỗi hướng)