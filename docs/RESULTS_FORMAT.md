# Results Format

Các file dữ liệu sinh ra từ thư mục `experiments/` phải tuân thủ schema dưới đây và lưu tại `data/` để phục vụ phân tích.

## 1. Brute-force (`timing_results.csv`)

| Cột | Kiểu dữ liệu | Mô tả | 
|---|---|---|
| `run_id` | Int | ID lần chạy |
| `key_size_bits` | Int | Kích thước khóa |
| `keys_searched` | Int | Số key đã quét |
| `time_seconds` | Float | Thời gian thực thi |

## 2. Padding Oracle (`attack_log.csv`)

| Cột | Kiểu dữ liệu | Mô tả |
|---|---|---|
| `block_index` | Int | Vị trí block |
| `byte_index` | Int | Vị trí byte trong block |
| `queries_made` | Int | Số request HTTP đã gửi |
| `recovered_byte` | String (Hex) | Byte tìm được (VD: `0x4A`) |

## 3. Differential Cryptanalysis

### a. `plaintext_pairs.csv`
| Cột | Kiểu dữ liệu | Mô tả |
|---|---|---|
| `p1` | String (Hex) | Plaintext 1 |
| `p2` | String (Hex) | Plaintext 2 |
| `c1` | String (Hex) | Ciphertext 1 |
| `c2` | String (Hex) | Ciphertext 2 |
| `delta_out` | String (Hex) | `c1 ⊕ c2` |

### b. `dc_key_recovery_results.json`
```json
{
  "attack_params": {
    "num_pairs": 4096,
    "delta_in": "0x0100"
  },
  "key_candidates": [
    {"subkey": "0xA4", "hits": 156, "probability": 0.038},
    {"subkey": "0x12", "hits": 12, "probability": 0.002}
  ]
}