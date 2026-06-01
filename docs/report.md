# Final Report: Cryptanalysis on Symmetric Ciphers (DES & AES)

## 1. Tóm tắt Đề tài
Đồ án tập trung nghiên cứu, triển khai thực nghiệm và phân tích mức độ rủi ro của các kỹ thuật tấn công mã hóa đối xứng trong kịch bản triển khai thực tế. Bốn thử nghiệm chính (từ Tuần 1 đến Tuần 10) đã được thực hiện nhằm chứng minh rằng: Dù thuật toán có an toàn tuyệt đối về mặt toán học (như AES), nhưng việc cấu hình sai (Misconfiguration) hoặc thiếu các biện pháp bảo vệ vật lý/phần mềm (Implementation Flaws) đều sẽ dẫn đến lộ lọt thông tin cực kỳ nghiêm trọng.

## 2. Kết quả Thực nghiệm & Phân tích Rủi ro

### 2.1. Experiment A: DES Brute-force
- **Nguyên lý:** Tấn công vét cạn không gian khóa hiệu dụng 56-bit của Data Encryption Standard (DES).
- **Kết quả đo lường:** Việc thử khóa diễn ra rất trơn tru. Với giới hạn không gian chỉ 2^56, các hệ thống GPU cluster hiện đại hoặc Cloud Computing hoàn toàn có thể bẻ gãy DES trong vòng vài giờ đồng hồ.
- **Phân tích:** DES đã chính thức "chết" và không còn an toàn cho bất kỳ ứng dụng hiện đại nào. Khuyến nghị loại bỏ hoàn toàn DES/3DES khỏi các hệ thống Legacy.

### 2.2. Experiment B: AES-CBC Padding Oracle
- **Nguyên lý:** Khai thác lỗ hổng xử lý lỗi (error handling) khi giải mã. Kẻ tấn công dùng phản hồi lỗi `Invalid Padding` của server (ví dụ mã HTTP 500) làm "Oracle" để giải mã ciphertext từng byte mà hoàn toàn không cần khóa bí mật.
- **Kết quả đo lường:** Khôi phục hoàn toàn bản rõ chỉ với khoảng 128 - 256 truy vấn (queries) mạng cho mỗi byte.
- **Biện pháp khắc phục (Mitigation):** Áp dụng kiến trúc *Uniform Error Handling* (trả về cùng một lỗi HTTP 400 chung chung cho mọi ngoại lệ). Giải pháp tốt nhất là chuyển hẳn sang sử dụng các chế độ mã hóa có xác thực (AEAD) như AES-GCM.

### 2.3. Experiment C: AES-GCM Nonce Reuse
- **Nguyên lý:** Lợi dụng việc lập trình viên tái sử dụng Nonce (Initialization Vector) trong mã hóa GCM. Khi Nonce trùng lặp giữa 2 bản tin, dòng khóa (Keystream) bị lộ qua phép toán XOR.
- **Kết quả đo lường:** Thời gian khôi phục bản rõ gần như tức thời ($O(1)$). Đặc biệt nguy hiểm, kẻ tấn công còn có thể thực hiện *Forbidden Attack* để khôi phục khóa xác thực (GHASH key) và tùy ý giả mạo nhãn xác thực (Tag Forgery) cho mọi dữ liệu sau này.
- **Biện pháp khắc phục:** Bắt buộc sử dụng hệ thống sinh số ngẫu nhiên an toàn (Cryptographically Secure Pseudo-Random) để sinh Nonce dài 96-bit, đảm bảo tính duy nhất tuyệt đối cho mỗi phiên.

### 2.4. Experiment D: AES Side-Channel (Cache Timing / CPA)
- **Nguyên lý:** Thu thập tín hiệu rò rỉ vật lý (thời gian truy cập bộ nhớ, hoặc điện năng tiêu thụ) khi CPU thực hiện tra cứu mảng S-Box (Table-based lookup) và sử dụng phân tích tương quan Pearson (CPA) để truy vết lại Khóa.
- **Kết quả đo lường:** Chỉ với khoảng 500 mẫu (traces) rò rỉ, thuật toán thống kê có thể phân tích và khôi phục toàn bộ 16-byte Khóa bí mật của AES-128 chỉ trong chưa tới 1 giây.
- **Biện pháp khắc phục:** Cấm sử dụng Table-based AES trong các môi trường có chia sẻ tài nguyên (Cloud/Multi-tenant) hoặc thiết bị IoT. Bắt buộc lập trình theo kiến trúc **Constant-Time** (thời gian thực thi không đổi, độc lập với dữ liệu) hoặc sử dụng tính năng phần cứng AES-NI.

## 3. Tổng kết Dự án
Qua 12 tuần thực hiện đồ án, chúng em rút ra kết luận cốt lõi: 
> **"Sự an toàn của một hệ thống mật mã không bao giờ chỉ nằm ở công thức toán học của nó, mà nằm ở toàn bộ quy trình cấu hình, lập trình và triển khai phần cứng."**

Mọi sơ suất nhỏ trong lập trình (báo lỗi sai, dùng lại biến ngẫu nhiên, không xử lý nhiễu điện năng) đều mở ra cánh cửa cho kẻ tấn công (Hackers) vượt qua bức tường thành AES tưởng chừng như bất khả xâm phạm.