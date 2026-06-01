# Hướng dẫn Cài đặt & Khởi chạy

Dự án sử dụng kiến trúc 2 Docker container để mô phỏng môi trường tấn công thực tế (Attacker và Victim).

## 1. Yêu cầu hệ thống
* Docker & Docker Compose
* Git

## 2. Khởi chạy Môi trường

**Bước 1:** Clone repository
```bash
git clone <repository_url>
cd cryptanalysis-on-symmetric-ciphers-des-and-aes-victim-web
```
Bước 2: Build và khởi chạy các container ở chế độ background

```bash
docker-compose up -d --build
```
Bước 3: Kiểm tra trạng thái container

```bash
docker-compose ps
```
*Expected output:* Cả crypto_victim (port 5000) và crypto_attacker đều đang ở trạng thái Up.
## 3. Truy cập Môi trường Tấn công (Attacker Workspace)

Mọi thao tác chạy script, compile code (C/C++), hoặc test đều được thực hiện bên trong container **Attacker**.

```bash
docker-compose exec attacker bash
```

**Kiểm tra kết nối tới máy Victim (từ bên trong Attacker):**
```bash
curl http://victim-web:5000/
```

## 4. Các lệnh thường dùng

* **Dừng hệ thống:** `docker-compose down`
* **Xem log của máy Victim:** `docker-compose logs -f victim-web`
* **Khởi động lại toàn bộ:** `docker-compose restart`