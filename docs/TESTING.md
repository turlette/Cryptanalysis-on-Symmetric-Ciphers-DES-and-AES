# Hướng dẫn Kiểm thử (Testing & PoC)

**Lưu ý:** Tất cả các lệnh dưới đây phải được thực thi bên trong shell của container attacker (`docker-compose exec attacker bash`).

## 1. Unit Tests (Mini-DES Core)
Kiểm tra tính chính xác của thuật toán mã hóa cốt lõi.
```bash
pytest mini_des/tests/ -v
```
## 2. Brute-force Attack (Offline)
Kiểm tra engine brute-force bằng C (được gọi qua Python).
```Bash
python experiments/exp_des_bruteforce/bf_engine.py --mode test
```
*Kết quả:* Chìa khóa được tìm thấy, log lưu tại data/timing_results.csv.

## 3. Padding Oracle Attack (Network)
Tấn công vào mục tiêu victim-web đang chạy trong mạng nội bộ Docker.

**Kiểm tra kết nối tới Victim:**

```Bash
curl http://victim-web:5000/
```
**Khởi chạy script tấn công:**

```Bash
python experiments/exp__padding_oracle/oracle_attack.py --target http://victim-web:5000
```
*Kết quả:* Plaintext được khôi phục block-by-block. Log truy vấn lưu tại data/attack_log.csv.

(Có thể mở thêm 1 terminal để xem log của server victim bị dội bom request: docker-compose logs -f victim-web)

## 4. Differential Cryptanalysis (Offline)
Kiểm tra bộ khung tấn công vi phân.

```Bash
python experiments/exp_differential_cryptanalysis/attack_framework.py --pairs 4096 --delta 0x0100
```
*Kết quả:* Trích xuất các bit khóa khả nghi. Log lưu tại data/dc_key_recovery_results.json.