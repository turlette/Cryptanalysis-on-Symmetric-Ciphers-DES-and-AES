# Literature Summary — Cryptanalysis on Symmetric Ciphers (DES & AES)

## Paper 1: Differential Cryptanalysis of DES

- **Title:** Differential Cryptanalysis of the Data Encryption Standard
- **Authors:** Eli Biham, Adi Shamir
- **Year:** 1993
- **Source:** Springer, DOI: 10.1007/978-1-4613-9314-6
- **Link:** https://www.semanticscholar.org/paper/Differential-Cryptanalysis-of-the-Data-Encryption-Biham-Shamir/0cfd5a7c6610e0eff2d277b419808edb32d93b78

### Key Contributions
- Giới thiệu **differential cryptanalysis** — phân tích cặp bản rõ có XOR difference được kiểm soát, theo dõi cách difference lan truyền qua các vòng S-box để suy ra key bits với xác suất cao hơn brute-force
- Là attack đầu tiên phá vỡ **full 16-round DES** nhanh hơn exhaustive search (~2⁴⁷ chosen plaintexts), đồng thời giới thiệu các khái niệm nền tảng: *characteristic*, *signal-to-noise ratio*, *structures*
- Được áp dụng thành công cho nhiều cipher khác: FEAL, Khafre, REDOC-II, LOKI, Lucifer, và một số hash functions — chứng minh đây là phương pháp tổng quát, không chỉ dành riêng cho DES

### Relevance to Project
Là nền tảng lý thuyết trực tiếp cho `experiments/exp_differential_cryptanalysis/`. Project implement lại đúng attack này trên Mini-DES, nên hiểu rõ paper là bắt buộc. Differential cryptanalysis cũng là tiền đề để hiểu các side-channel attacks hiện đại.

---

## Paper 2: Linear Cryptanalysis of DES

- **Title:** The First Experimental Cryptanalysis of the Data Encryption Standard
- **Authors:** Mitsuru Matsui
- **Year:** 1994
- **Source:** CRYPTO 1994 (version lý thuyết: "Linear Cryptanalysis Method for DES Cipher", EUROCRYPT 1993)
- **Link:** https://www.semanticscholar.org/paper/The-First-Experimental-Cryptanalysis-of-the-Data-Matsui/56606d725cb6d553862c98311765dd2d77e9603b

### Key Contributions
- Giới thiệu **linear cryptanalysis** — tìm xấp xỉ tuyến tính (linear approximation) giữa bản rõ, bản mã và key thông qua bias của S-boxes, cho phép khôi phục key bits bằng thống kê
- Là known-plaintext attack đầu tiên phá thực nghiệm DES đầy đủ 56-bit key (~2⁴³ known plaintexts), thực hiện trên 12 máy tính trong 50 ngày (40 ngày sinh data + 10 ngày phân tích)
- Đặt nền tảng cho tiêu chí thiết kế S-box: **non-linearity cao** là yêu cầu bắt buộc — AES S-box được thiết kế với non-linearity tối ưu để chống lại attack này

### Relevance to Project
Song song với differential cryptanalysis ở cấp độ cấu trúc. Cả hai cùng nhau tạo nên nền tảng của *classical cryptanalysis* và là lý do DES bị coi là không an toàn. Hiểu paper này giúp phân tích điểm yếu của S-box trong Mini-DES và so sánh với AES.

---

## Paper 3: Padding Oracle Attack (CBC Mode)

- **Title:** Security Flaws Induced by CBC Padding — Applications to SSL, IPSEC, WTLS...
- **Authors:** Serge Vaudenay
- **Year:** 2002
- **Source:** EUROCRYPT 2002
- **Link:** https://www.usenix.org/legacy/event/woot10/tech/full_papers/Rizzo.pdf *(practical extension: Rizzo & Duong, WOOT 2010)*

### Key Contributions
- Phát hiện **padding oracle vulnerability** trong CBC mode với PKCS#5 padding: nếu server tiết lộ thông tin "padding đúng/sai" (dù chỉ qua error message hoặc timing), attacker có thể decrypt hoàn toàn ciphertext mà không cần key
- Chỉ ra rằng thông tin tưởng chừng vô hại (padding error) tạo thành **adaptive chosen-ciphertext oracle**, đủ để phá vỡ confidentiality của toàn bộ session
- Được mở rộng thành các attack thực tế trên TLS/SSL, IPSEC, WTLS; sau đó là **POODLE attack** (2014) trên SSL 3.0 — ảnh hưởng trực tiếp đến hàng triệu web server

### Relevance to Project
Là attack được implement trực tiếp trong `experiments/exp_padding_oracle/`. Đây là ví dụ kinh điển về **side-channel attack từ error messages** — cho thấy implementation-level flaws nguy hiểm không kém mathematical weaknesses.

---

## Paper 4: Cache Timing Attack on AES

- **Title:** Cache-timing attacks on AES
- **Authors:** Daniel J. Bernstein
- **Year:** 2005
- **Source:** Technical Report, cr.yp.to
- **Link:** http://cr.yp.to/antiforgery/cachetiming-20050414.pdf

### Key Contributions
- Chứng minh AES implementation tiêu chuẩn (dùng T-table lookup) bị rò rỉ thông tin key qua **CPU cache timing**: cache hit (~4 cycles) vs cache miss (~200 cycles) tạo ra timing signature phụ thuộc vào key
- Thực hiện remote key recovery chỉ từ timing measurements qua network (~2²⁸ measurements) — không cần physical access, chứng minh đây là **practical remote attack**
- Chỉ ra NIST đã bỏ qua vấn đề này khi chọn AES, và đề xuất yêu cầu **constant-time implementation** như tiêu chuẩn cho cryptographic code

### Relevance to Project
Minh họa quan trọng rằng ngay cả cipher toán học mạnh như AES cũng có thể bị phá qua implementation. Khác với differential/linear (tấn công toán học), cache timing tấn công hardware layer — mở rộng threat model của project sang side-channel attacks thực tế.

---

## So sánh 4 Phương pháp

| Tiêu chí | Differential (1993) | Linear (1994) | Padding Oracle (2002) | Cache Timing (2005) |
|----------|--------------------|--------------|-----------------------|---------------------|
| **Loại attack** | Chosen-plaintext | Known-plaintext | Chosen-ciphertext | Side-channel (timing) |
| **Target** | DES S-box math | DES S-box bias | CBC padding impl | AES T-table impl |
| **Điều kiện** | Cần chosen plaintexts | Cần lượng lớn data | Cần padding oracle | Cần timing measurements |
| **Độ phức tạp** | ~2⁴⁷ | ~2⁴³ | O(n·256) queries | ~2²⁸ measurements |
| **Layer tấn công** | Mathematical | Mathematical | Protocol/Impl | Hardware/Impl |

---

## Reference Implementations

| # | Project | Link | Liên quan đến |
|---|---------|------|--------------|
| 1 | GurbSingh/Differential-Cryptanalysis | https://github.com/GurbSingh/Differential-Cryptanalysis | Paper 1 — Differential |
| 2 | mpgn/Padding-oracle-attack | https://github.com/mpgn/Padding-oracle-attack | Paper 3 — Padding Oracle |
| 3 | RodoVerduzco/Mini-DES | https://github.com/RodoVerduzco/Mini-DES | Base implementation cho Mini-DES |
| 4 | bozhu/AES-Python | https://github.com/bozhu/AES-Python | Paper 4 — AES impl reference |

---