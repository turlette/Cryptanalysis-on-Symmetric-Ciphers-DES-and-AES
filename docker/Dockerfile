FROM python:3.10-slim

# Thiết lập thư mục làm việc trong container
WORKDIR /app

# Copy file requirements trước để tận dụng cache
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy toàn bộ mã nguồn của dự án vào container
COPY . .

# Chạy kịch bản tự động mô phỏng toàn bộ 4 thử nghiệm
CMD ["python", "scripts/run_all.py"]
