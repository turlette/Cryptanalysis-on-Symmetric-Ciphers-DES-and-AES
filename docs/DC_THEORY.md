# Differential Cryptanalysis — Theory Deep-dive

## 1. Differential Characteristic

### Khái niệm cơ bản

**Differential cryptanalysis** khai thác cách *differences* (sự khác biệt) giữa 2 bản rõ lan truyền qua các vòng mã hóa.

- **Difference** được định nghĩa là XOR giữa 2 giá trị:
  ```
  ΔX = X ⊕ X'
  ```
  Với `X` và `X'` là cặp bản rõ (plaintext pair).

- **Mục tiêu:** Tìm một chuỗi differences `(ΔP → ΔC)` có xác suất xảy ra cao nhất qua tất cả các vòng → suy ra key bits.

### Differential Characteristic

Một **differential characteristic** là một chuỗi các differences qua từng vòng:

```
ΔP → Δα₁ → Δα₂ → ... → Δαᵣ₋₁ → ΔC
```

Trong đó:
- `ΔP` = input difference (XOR của 2 plaintext)
- `Δαᵢ` = difference sau vòng thứ i
- `ΔC` = output difference (XOR của 2 ciphertext)
- Mỗi bước có một xác suất xảy ra `pᵢ`

### Ví dụ minh họa (1-round characteristic)

```
Plaintext pair:  P  = 0x0000000000000000
                 P' = 0x0020000000000000
Input diff:      ΔP = P ⊕ P' = 0x0020000000000000

Sau vòng 1:
  ΔX₁ = ΔP xử lý qua expansion, S-box, permutation
  → Δα₁ = 0x0000008000000000  (xác suất p₁ = 1/4)

Sau vòng 2:
  → Δα₂ = 0x0000000000000000  (xác suất p₂ = 1/4)
```

### Differential Characteristics Table (Simplified — 1-round)

Bảng dưới đây mô tả một số differential đặc trưng của S1-box trong DES:

| Input Difference (ΔX_in) | Output Difference (ΔX_out) | Số lần xuất hiện | Xác suất |
|--------------------------|---------------------------|------------------|----------|
| `0x00`                   | `0x00`                    | 64               | 1.0      |
| `0x06`                   | `0x02`                    | 8                | 8/64 = 1/8 |
| `0x06`                   | `0x04`                    | 6                | 6/64     |
| `0x0E`                   | `0x06`                    | 6                | 6/64     |
| `0x34`                   | `0x04`                    | 4                | 4/64 = 1/16 |
| `0x22`                   | `0x00`                    | 0                | 0        |

> **Ghi chú:** Bảng đầy đủ cần xây dựng từ từng S-box của DES/Mini-DES bằng cách enumerate tất cả 64×64 cặp đầu vào.

### Cách xây dựng bảng (thuật toán):

```python
def build_difference_table(sbox):
    """
    Với mỗi S-box (64 entry), xây dựng bảng:
    diff_table[delta_in][delta_out] = số cặp (x, x') thỏa mãn
    """
    size = len(sbox)
    table = [[0] * size for _ in range(size)]

    for x in range(size):
        for x_prime in range(size):
            delta_in  = x ^ x_prime
            delta_out = sbox[x] ^ sbox[x_prime]
            table[delta_in][delta_out] += 1

    return table
```

---

## 2. Probability Calculation

### Xác suất của một characteristic

Xác suất của một r-round characteristic là **tích** xác suất tại từng vòng:

```
Pr(ΔP → ΔC) = p₁ × p₂ × ... × pᵣ
```

Mỗi `pᵢ` là xác suất difference `Δαᵢ₋₁ → Δαᵢ` qua S-box của vòng i.

### Ví dụ tính xác suất (13-round characteristic cho DES):

Biham & Shamir tìm được characteristic 13 vòng với xác suất:

```
p = 1/234 ≈ 2⁻⁴⁷·²
```

Điều này có nghĩa: cần ~2⁴⁷ chosen plaintext pairs để attack thành công.

### So sánh với brute-force:

| Phương pháp        | Độ phức tạp |
|--------------------|-------------|
| Brute-force (56-bit key) | 2⁵⁶ ≈ 7.2 × 10¹⁶ |
| Differential (13-round)  | 2⁴⁷ ≈ 1.4 × 10¹⁴ |
| **Cải thiện**            | **~512 lần nhanh hơn** |

### Signal-to-noise ratio (S/N):

```
S/N = (2^k × p) / α
```

Trong đó:
- `k` = số key bits cần tìm
- `p` = xác suất characteristic
- `α` = tỷ lệ "wrong pairs" qua mỗi key candidate

S/N > 1 → attack khả thi (đúng key nổi bật hơn các key sai).

---

## 3. Attack Flow (High-level Pseudocode)

### Tổng quan

Differential cryptanalysis là **chosen-plaintext attack**: attacker chọn plaintext pairs, lấy ciphertext tương ứng, rồi dùng differential characteristic để suy ngược key của vòng cuối.

### Pseudocode

```
ALGORITHM: Differential_Cryptanalysis(cipher, target_rounds)

INPUT:
  - cipher: hàm mã hóa cần tấn công
  - r: số vòng (ví dụ: 16 với DES)
  - (ΔP → ΔC*): (r-1)-round characteristic đã biết

OUTPUT:
  - subkey của vòng cuối (round r)

─────────────────────────────────────────────────

PHASE 1: Chọn characteristic
  1. Tìm (r-1)-round characteristic (ΔP → ΔC*) với xác suất p cao nhất
     (Biham & Shamir đã tính sẵn cho DES)

PHASE 2: Thu thập data
  2. FOR i = 1 TO N (N ≈ c/p, với c là hằng số):
       a. Chọn ngẫu nhiên plaintext P
       b. Tính P' = P ⊕ ΔP
       c. Lấy ciphertext: C  = cipher(P)
                          C' = cipher(P')
       d. Lưu pair (C, C') vào dataset

PHASE 3: Phân tích key
  3. Tạo bảng đếm: count[k] = 0 với mọi subkey candidate k

  4. FOR mỗi ciphertext pair (C, C') trong dataset:
       FOR mỗi subkey candidate k:
         a. Giải mã vòng cuối: T  = decrypt_last_round(C,  k)
                                T' = decrypt_last_round(C', k)
         b. Tính output difference: ΔT = T ⊕ T'
         c. IF ΔT == ΔC*:           ← "right pair" signal
              count[k] += 1

PHASE 4: Tìm key
  5. Chọn k* = argmax(count[k])
     → k* là subkey của vòng cuối với xác suất cao

  6. (Optional) Lặp lại để tìm các subkey khác hoặc
     bruteforce phần key còn lại

─────────────────────────────────────────────────

COMPLEXITY:
  - Số plaintext pairs cần: N = O(1/p)
  - Với DES 16-round: p ≈ 2⁻⁴⁷ → cần ~2⁴⁷ pairs
```

### Sơ đồ luồng attack:

```
┌─────────────────────────────────────────────────────────┐
│                   ATTACKER                              │
│                                                         │
│  Chọn ΔP                                                │
│      │                                                  │
│      ▼                                                  │
│  Generate N plaintext pairs (P, P' = P ⊕ ΔP)           │
│      │                                                  │
│      ▼                                                  │
│  Query cipher oracle → nhận (C, C') pairs               │
│      │                                                  │
│      ▼                                                  │
│  FOR each subkey candidate k:                           │
│    Decrypt last round with k                            │
│    Check if ΔOutput == ΔC* (expected)                   │
│    Count "right pairs"                                  │
│      │                                                  │
│      ▼                                                  │
│  Subkey với count cao nhất = KEY ✓                      │
└─────────────────────────────────────────────────────────┘
```

---

## 4. Key Takeaways

| Khái niệm | Ý nghĩa |
|-----------|---------|
| **Difference (ΔX)** | XOR giữa 2 plaintexts: `ΔX = X ⊕ X'` |
| **Characteristic** | Chuỗi differences qua các vòng với xác suất p |
| **Right pair** | Pair thực sự tuân theo characteristic |
| **Wrong pair** | Pair ngẫu nhiên, gây nhiễu |
| **Signal-to-noise** | Tỷ lệ right/wrong pairs — quyết định số data cần thiết |
| **Chosen-plaintext** | Attacker cần quyền chọn plaintext và query cipher |

---

## 5. References

- Biham, E., & Shamir, A. (1993). *Differential Cryptanalysis of the Data Encryption Standard*. Springer. DOI: 10.1007/978-1-4613-9314-6
- Semantic Scholar: https://www.semanticscholar.org/paper/Differential-Cryptanalysis-of-the-Data-Encryption-Biham-Shamir/0cfd5a7c6610e0eff2d277b419808edb32d93b78