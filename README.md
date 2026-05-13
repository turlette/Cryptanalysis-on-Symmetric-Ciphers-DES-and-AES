# Cryptanalysis on Symmetric Ciphers: DES and AES
 
Dự án phân tích các thuật toán mã hóa đối xứng: **DES** (Data Encryption Standard) và **AES** (Advanced Encryption Standard).
 
---
 
## 📋 Yêu cầu hệ thống
 
- **Python:** 3.9 trở lên
- **OS:** Windows, macOS, Linux
- **Git:** Để clone repository
### Kiểm tra Python version:
 
```bash
python --version
```
 
✅ Phải hiện **Python 3.9+** (ví dụ: `Python 3.12.11`)
 
---
 
## 🚀 Hướng dẫn setup ban đầu (Lần đầu tiên)
 
### **Bước 1: Clone repository**
 
```bash
git clone <repository-url>
cd Cryptanalysis-on-Symmetric-Ciphers-DES-and-AES
```
 
### **Bước 2: Tạo Virtual Environment**
 
#### **Windows (Command Prompt):**
 
```bash
python -m venv venv
```
 
#### **macOS / Linux:**
 
```bash
python3 -m venv venv
```
 
### **Bước 3: Kích hoạt Virtual Environment**
 
#### **Windows (Command Prompt):**
 
```bash
venv\Scripts\activate
```
 
Sau khi kích hoạt, terminal sẽ hiện `(venv)` ở đầu dòng:
 
```
(venv) F:\Cryptanalysis-on-Symmetric-Ciphers-DES-and-AES>
```
 
#### **macOS / Linux:**
 
```bash
source venv/bin/activate
```
 
Sau khi kích hoạt, terminal sẽ hiện `(venv)`:
 
```
(venv) user@machine:~/Cryptanalysis$ 
```
 
#### **Git Bash (Windows):**
 
```bash
source venv/Scripts/activate
```
 
### **Bước 4: Cài đặt dependencies**
 
```bash
pip install -r requirements.txt
```
 
Chờ cho tất cả packages được cài xong. Output cuối cùng sẽ hiện:
 
```
Successfully installed pycryptodome numpy matplotlib pytest ...
```
 
### **Bước 5: Kiểm tra installation**
 
```bash
python -c "from Crypto.Cipher import DES, AES; import numpy; import matplotlib; print('✅ All packages imported successfully!')"
```
 
✅ Nếu không có lỗi → **Setup thành công!**
 
---
 
## 🔄 Lần tiếp theo (Mỗi lần sử dụng)
 
Mỗi lần muốn làm việc với dự án, chỉ cần kích hoạt venv:
 
### **Windows:**
 
```bash
venv\Scripts\activate
```
 
### **macOS / Linux:**
 
```bash
source venv/bin/activate
```
 
### **Git Bash:**
 
```bash
source venv/Scripts/activate
```
 
---
 
## 📁 Cấu trúc dự án
 
```
Cryptanalysis-on-Symmetric-Ciphers-DES-and-AES/
├── venv/
├── mini_des/              # Mini-DES implementation
├── experiments/           # 3 attack scenarios
│   ├── exp_des_bruteforce/
│   ├── exp_padding_oracle/
│   └── exp_differential_cryptanalysis/
├── docker/               # Lab environment
├── docs/                 # Reports & slides
├── scripts/              # Automation
├── data/                 # Results
└── README.md
```
 
---
 
## 🔧 Cài thêm Package
 
Nếu cần cài thêm package nào:
 
```bash
pip install <package-name>
```
 
**Sau đó, cập nhật `requirements.txt`:**
 
```bash
pip freeze > requirements.txt
```
 
**Commit lên Git:**
 
```bash
git add requirements.txt
git commit -m "Add new package: <package-name>"
git push
```
 
---
 
## 🧪 Chạy tests
 
Nếu có tests trong dự án:
 
```bash
pytest
```
 
Hoặc chạy test file cụ thể:
 
```bash
pytest mini_des/tests/test_mini_des.py -v
```
 
---
 
## ❌ Troubleshooting
 
### **Vấn đề 1: "python is not recognized"**
 
**Nguyên nhân:** Python chưa được thêm vào PATH
 
**Giải pháp:**
1. Gỡ cài Python cũ
2. Cài Python từ https://www.python.org/downloads/
3. ✅ **QUAN TRỌNG:** Tick "Add Python to PATH" khi cài
4. Restart máy
5. Mở Command Prompt mới và thử lại
### **Vấn đề 2: "No module named 'venv'"**
 
**Nguyên nhân:** Python chưa cài venv module
 
**Giải pháp:**
- **Ubuntu/Debian:**
  ```bash
  sudo apt-get install python3-venv
  ```
- **Fedora:**
  ```bash
  sudo dnf install python3-venv
  ```
- **macOS:** Cài lại Python từ python.org
### **Vấn đề 3: Lỗi khi cài pycryptodome / numpy**
 
**Nguyên nhân:** Compiler hoặc dependency bị thiếu
 
**Giải pháp:**
```bash
# Cập nhật pip trước
python -m pip install --upgrade pip
 
# Rồi cài lại
pip install -r requirements.txt
```
 
### **Vấn đề 4: "ModuleNotFoundError" khi chạy code**
 
**Nguyên nhân:** Chưa kích hoạt virtual environment
 
**Giải pháp:** Chắc chắn terminal hiện `(venv)` ở đầu dòng. Nếu không, chạy:
 
**Windows:**
```bash
venv\Scripts\activate
```
 
**macOS/Linux:**
```bash
source venv/bin/activate
```
 
### **Vấn đề 5: Xóa venv và reset lại**
 
Nếu muốn xóa venv hoàn toàn và tạo lại từ đầu:
 
```bash
# Windows
rmdir /s venv
 
# macOS / Linux
rm -rf venv
 
# Rồi tạo lại từ bước 2
python -m venv venv
venv\Scripts\activate  # hoặc source venv/bin/activate
pip install -r requirements.txt
```
 
---
 
## 📚 Tài liệu tham khảo
 
### Feistel Network & DES
 
- **FIPS 46-3 (Chính thức):** https://csrc.nist.gov/files/pubs/fips/46-3/final/docs/fips46-3.pdf
- **Purdue Lecture 3:** https://engineering.purdue.edu/kak/compsec/NewLectures/Lecture3.pdf
- **Simplified DES:** https://www.brainkart.com/article/Simplified-Data-Encryption-Standard-(S-DES)_8343/
### Open-source Reference
 
- **Simplified DES (C++):** https://github.com/kevinoconnor7/Simplified-DES
- **Mini-DES (Python):** https://github.com/RodoVerduzco/Mini-DES
### Online Resources
 
- **Wikipedia Feistel Cipher:** https://en.wikipedia.org/wiki/Feistel_cipher
- **Medium: Feistel & DES:** https://medium.com/@ajeetskbp9843/day-04-quantum-cryptography-feistel-cipher-structure-data-encryption-standard-des-and-advanced-fb2a7cb75433
---
 
## ❓ Câu hỏi thường gặp
 
### Q: Tại sao phải dùng Virtual Environment?
 
**A:** Virtual environment giúp:
- ✅ Tách biệt packages của dự án này với dự án khác
- ✅ Tránh xung đột version (Project A dùng numpy 1.24, Project B dùng numpy 1.26)
- ✅ Dễ chia sẻ (`requirements.txt` là đủ)
- ✅ Dễ dọn dẹp (xóa folder `venv` là xong)
### Q: Có cần commit `venv/` folder lên Git không?
 
**A:** **KHÔNG!** Lý do:
- `venv/` quá nặng (~100-200 MB)
- Mỗi máy/OS (Windows/Mac/Linux) có cấu trúc venv khác nhau
- Người khác sẽ tạo venv riêng trên máy họ
Nó đã được thêm vào `.gitignore` rồi.
 
### Q: Làm sao để người mới join team cài được?
 
**A:** Họ chỉ cần làm theo 5 bước trong "Hướng dẫn setup ban đầu" ở trên.
 
### Q: Nếu tôi cài thêm package mới, team khác làm sao biết?
 
**A:** Cập nhật `requirements.txt`:
 
```bash
pip freeze > requirements.txt
git add requirements.txt
git commit -m "Add new package: <package-name>"
git push
```
 
Mọi người pull repo → chạy `pip install -r requirements.txt` → cập nhật được.
 
### Q: Làm sao thoát khỏi venv?
 
**A:** Gõ:
 
```bash
deactivate
```
 
Terminal sẽ không còn hiện `(venv)` nữa.
 
---