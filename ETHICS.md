# Khuyến nghị Đạo đức & Miễn trừ Trách nhiệm (Ethics & Responsible Disclosure)

## 1. Tuyên bố Đạo đức (Ethics Statement)
Dự án **"Cryptanalysis on Symmetric Ciphers: DES & AES"** được thực hiện **DUY NHẤT** vì mục đích giáo dục, nghiên cứu học thuật và nâng cao nhận thức về an toàn thông tin theo chuẩn mực quốc tế.
Mọi thử nghiệm tấn công (như Padding Oracle, Brute-force, Nonce Reuse, Side-channel) đều được lập trình và chạy trên các **hệ thống giả lập (Isolated Lab Targets)** nội bộ do chính nhóm nghiên cứu xây dựng.

Chúng tôi **TUYỆT ĐỐI KHÔNG** sử dụng các công cụ, mã khai thác (Exploit/PoC) được phát triển trong đồ án này để nhắm vào bất kỳ hệ thống, dịch vụ, hay thiết bị IoT của bên thứ ba nào khi chưa có sự ủy quyền bằng văn bản.

## 2. Nguyên tắc Tiết lộ Trách nhiệm (Responsible Disclosure)
Trong trường hợp các kỹ thuật phân tích của dự án vô tình phát hiện ra lỗ hổng bảo mật zero-day trên các thư viện mật mã mã nguồn mở hiện hành (ví dụ: OpenSSL, PyCryptodome), chúng tôi cam kết sẽ tuân thủ nghiêm ngặt quy trình Tiết lộ Trách nhiệm (Responsible Disclosure):
1. Báo cáo riêng tư trực tiếp cho đội ngũ bảo mật của tổ chức (Vendor) kèm theo kịch bản tái tạo lỗ hổng.
2. Cho phép một khoảng thời gian tiêu chuẩn (thường là 90 ngày) để nhà phát hành tung ra bản vá trước khi công bố thông tin ra đại chúng.
3. Chống lại việc phát tán mã khai thác vũ khí hóa (weaponized exploit) gây nguy hiểm cho cộng đồng.

## 3. Cảnh báo (Dual-use Caution)
Mã nguồn tấn công (Attacker scripts) trong thư mục `experiments/` mang tính chất rủi ro cao (công nghệ lưỡng dụng - Dual-use technology). Người đọc và sử dụng mã nguồn trong kho lưu trữ này phải tự chịu trách nhiệm trước pháp luật về mọi hành vi của mình. Tác giả đồ án và cơ sở đào tạo từ chối mọi trách nhiệm liên đới đối với bất kỳ thiệt hại nào do việc lạm dụng hoặc sử dụng sai mục đích các thông tin từ dự án này gây ra.
