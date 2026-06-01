# Runbook & Reproducibility Guide

Tài liệu này hướng dẫn cách chạy toàn bộ các thử nghiệm trong đồ án một cách hoàn toàn tự động, đảm bảo tính tái tạo (Reproducibility) cao nhất đúng chuẩn một nghiên cứu khoa học an toàn thông tin.

## 1. Yêu cầu hệ thống cơ bản
- Python 3.10+
- (Tùy chọn) Docker và Docker Compose (nếu muốn chạy trong môi trường Container cô lập).

## 2. Cách 1: Chạy Tự Động Bằng Python Script (Local)
Chúng tôi đã xây dựng các script tự động tại thư mục `scripts/` để chạy lần lượt toàn bộ 4 thử nghiệm (Experiment A -> D) và tổng hợp kết quả.

**Thao tác:**
1. Mở Terminal (PowerShell / Command Prompt) tại thư mục gốc của repository.
2. Cài đặt các thư viện phụ thuộc:
   ```bash
   pip install -r requirements.txt
   ```
3. Chạy lệnh tự động hóa 4 thử nghiệm:
   ```bash
   python scripts/run_all.py
   ```
4. Đọc báo cáo phân tích thống kê (tổng hợp từ log):
   ```bash
   python scripts/analyze_results.py
   ```

## 3. Cách 2: Chạy Tự Động Bằng Docker (Khuyến nghị)
Để đảm bảo môi trường thực thi của bạn giống hệt 100% với môi trường Lab của chúng tôi và không gây rác (conflict) hệ thống máy thật, bạn nên chạy toàn bộ suite thông qua Docker.

**Thao tác:**
1. Mở Terminal tại thư mục gốc của repository.
2. Build và Run Docker container bằng một lệnh duy nhất:
   ```bash
   docker-compose -f docker/docker-compose.yml up --build
   ```
3. Hệ thống sẽ tự động tải Python Image, cài đặt `pycryptodome`, chạy file `run_all.py` ngay bên trong Container.
4. **Kết quả Logs:** Dù chạy trong Container, toàn bộ kết quả vẫn sẽ được đồng bộ (mount volume) ra ngoài và lưu an toàn tại thư mục `data/` trên máy thật của bạn. Bạn hoàn toàn có thể chạy file `scripts/analyze_results.py` ở bên ngoài để đọc log.