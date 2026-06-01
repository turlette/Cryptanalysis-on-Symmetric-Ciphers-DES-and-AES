"""
Task 3.2.6 [R] — DC Attack Part 3: Key Recovery
================================================
Từ bias tìm được ở Task 3.2.5, recover last-round subkey
bằng cách đếm right pairs, sau đó brute-force phần key còn lại.

MiniDES specs (từ mini_des/mini_des.py):
    Block  : 16 bits  (L=8bit | R=8bit)
    Key    : 24 bits
    Rounds : 8 (Feistel)
    Subkey : rotate_left(key, i) & 0xFF  — subkeys[i] là 8-bit
    F(R,K) : ((R ^ K) + 0x42) & 0xFF

Deliverable: experiments/dc/dc_key_recovery_results.json

Chạy từ root của repo:
    python experiments/dc/key_recovery.py
"""

import os
import sys
import json
import csv
from collections import Counter, defaultdict

sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))
from mini_des.mini_des import MiniDES

# ---------------------------------------------------------------------------
# Config — dùng cùng key với Task 3.1.5
# ---------------------------------------------------------------------------
INPUT_CSV   = os.path.join(os.path.dirname(__file__), "plaintext_pairs.csv")
OUTPUT_JSON = os.path.join(os.path.dirname(__file__), "dc_key_recovery_results.json")
TRUE_KEY    = 0b101000001011001100   # 24-bit — phải khớp với collect_plaintext_pairs.py


# ---------------------------------------------------------------------------
# Load pairs
# ---------------------------------------------------------------------------
def load_pairs(path: str) -> list[dict]:
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


# ---------------------------------------------------------------------------
# Step 1: Tìm top-bias từ delta_out
# ---------------------------------------------------------------------------
def find_top_bias(records: list[dict], top_n: int = 3):
    deltas = []
    for r in records:
        c1 = int(r["ciphertext1"], 16)
        c2 = int(r["ciphertext2"], 16)
        deltas.append(c1 ^ c2)

    freq  = Counter(deltas)
    total = len(deltas)
    top   = freq.most_common(top_n)

    # Bias có ý nghĩa nếu top-1 xuất hiện nhiều hơn 5x mức uniform
    uniform_expected = total / 0xFFFF
    bias_found = bool(top and top[0][1] > uniform_expected * 5)

    return freq, top, bias_found


# ---------------------------------------------------------------------------
# Step 2: Partial key recovery — recover subkey của vòng cuối (round 7)
#
# MiniDES Feistel round thuận:
#   L_new = R
#   R_new = L ^ F(R, subkeys[round])
#
# Để đảo vòng cuối (round 7) từ ciphertext:
#   ciphertext = (R_final << 8) | L_final  (sau final swap)
#   Trước final swap: L8 = R_final, R8 = L_final
#   R7 = L8 = R_final
#   L7 = R8 ^ F(R7, subkeys[7]) = L_final ^ F(R_final, k7)
#
# Với 2 ciphertext C và C', nếu pair là "right pair" cho characteristic:
#   delta(L7) ^ delta(L7') nên match với expected_delta_after_round7
# ---------------------------------------------------------------------------
def _f_function(R: int, subkey: int) -> int:
    """MiniDES F-function: ((R ^ subkey) + 0x42) & 0xFF"""
    return ((R ^ subkey) + 0x42) & 0xFF


def _undo_last_round(ciphertext: int, k7: int) -> tuple[int, int]:
    """
    Đảo ngược vòng cuối (round 7) của MiniDES với subkey candidate k7.

    MiniDES encrypt kết thúc bằng:
        result = (R << 8) | L   (final swap)
    Nên từ ciphertext:
        R_final = (ciphertext >> 8) & 0xFF  = R sau round 7
        L_final = ciphertext & 0xFF         = L sau round 7

    Feistel: L_new=R_old, R_new = L_old ^ F(R_old, key)
    Đảo:     R_old = L_new,  L_old = R_new ^ F(L_new, key)
    """
    R_final = (ciphertext >> 8) & 0xFF
    L_final = ciphertext & 0xFF

    # Undo round 7:
    R7 = R_final                            # R trước round 7
    L7 = L_final ^ _f_function(R_final, k7) # L trước round 7

    return L7, R7


def recover_last_subkey(
    records: list[dict],
    expected_delta_out: int,
) -> tuple[int, dict[int, int]]:
    """
    Với mỗi subkey candidate k7 (0..255):
      - Undo vòng cuối của mỗi ciphertext pair
      - Nếu XOR của kết quả == expected_delta_out → right pair → count[k7]++
    Trả về (best_k7, count_dict)
    """
    subkey_count: dict[int, int] = defaultdict(int)

    for r in records:
        c1 = int(r["ciphertext1"], 16)
        c2 = int(r["ciphertext2"], 16)

        for k7 in range(256):
            L7_a, R7_a = _undo_last_round(c1, k7)
            L7_b, R7_b = _undo_last_round(c2, k7)

            # XOR của state trước round 7
            delta_L = L7_a ^ L7_b
            delta_R = R7_a ^ R7_b
            recovered_delta = (delta_L << 8) | delta_R

            if recovered_delta == expected_delta_out:
                subkey_count[k7] += 1

    best_k7 = max(subkey_count, key=subkey_count.get) if subkey_count else 0
    return best_k7, dict(subkey_count)


# ---------------------------------------------------------------------------
# Step 3: Verify recovered subkey vs true subkey
# ---------------------------------------------------------------------------
def get_true_subkey7(key: int) -> int:
    """Tính subkeys[7] giống _key_schedule trong MiniDES."""
    i       = 7
    rotated = ((key << i) | (key >> (24 - i))) & 0xFFFFFF
    return rotated & 0xFF


# ---------------------------------------------------------------------------
# Step 4: Brute-force full 24-bit key với hint từ subkey recovered
# ---------------------------------------------------------------------------
def brute_force_with_subkey_hint(
    records: list[dict],
    recovered_k7: int,
    sample_size: int = 64,
) -> tuple[int | None, int]:
    """
    Brute-force toàn bộ 24-bit key space (2^24 ≈ 16M),
    nhưng chỉ xét các key có subkeys[7] == recovered_k7.

    Với mỗi candidate, kiểm tra trên sample_size pairs.
    Key đúng sẽ decrypt đúng tất cả.

    Returns: (best_key, correct_count)
    """
    sample = records[:sample_size]

    best_key   = None
    best_score = 0

    for candidate in range(2**24):
        # Chỉ xét key có subkeys[7] khớp
        i       = 7
        rotated = ((candidate << i) | (candidate >> (24 - i))) & 0xFFFFFF
        if (rotated & 0xFF) != recovered_k7:
            continue

        des   = MiniDES(candidate)
        score = 0
        for r in sample:
            p1 = int(r["plaintext1"], 16)
            c1 = int(r["ciphertext1"], 16)
            if des.encrypt(p1) == c1:
                score += 1

        if score > best_score:
            best_score = score
            best_key   = candidate
            if score == sample_size:
                break   # perfect match — stop early

    return best_key, best_score


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print(f"Loading {INPUT_CSV} ...")
    records = load_pairs(INPUT_CSV)
    n_pairs = len(records)
    print(f"  Loaded {n_pairs} pairs.\n")

    # --- Step 1: Find bias ---
    freq, top3, bias_found = find_top_bias(records)
    most_likely_delta = top3[0][0] if top3 else 0
    top_frequency     = top3[0][1] if top3 else 0
    uniform_expected  = n_pairs / 0xFFFF

    print(f"bias_found        : {bias_found}")
    print(f"most_likely_delta : 0x{most_likely_delta:04X}")
    print(f"frequency         : {top_frequency}  "
          f"({top_frequency/uniform_expected:.1f}x uniform)")

    # --- Step 2: Recover last subkey (k7) ---
    print(f"\nRecovering last-round subkey (k7) against delta=0x{most_likely_delta:04X}...")
    best_k7, subkey_counts = recover_last_subkey(records, most_likely_delta)
    true_k7                = get_true_subkey7(TRUE_KEY)

    print(f"  Recovered k7 : 0x{best_k7:02X}  (count={subkey_counts.get(best_k7,0)})")
    print(f"  True k7      : 0x{true_k7:02X}")
    print(f"  k7 correct   : {best_k7 == true_k7}")

    key_bits_identified = 8 if best_k7 == true_k7 else 0

    # --- Step 3: Brute-force remaining bits ---
    print(f"\nBrute-forcing full 24-bit key with k7=0x{best_k7:02X} hint...")
    print("  (scanning ~2^24 / 256 = 65536 candidates — may take a moment)")
    recovered_key, score = brute_force_with_subkey_hint(records, best_k7)

    full_key_recovered = (recovered_key == TRUE_KEY)
    print(f"  Recovered key : 0x{recovered_key:06X}" if recovered_key else "  Recovered key : None")
    print(f"  True key      : 0x{TRUE_KEY:06X}")
    print(f"  Correct       : {full_key_recovered}  (score={score}/64)")

    # --- Step 4: Build JSON result ---
    result = {
        "n_pairs":             n_pairs,
        "bias_found":          bias_found,
        "most_likely_delta":   f"0x{most_likely_delta:04X}",
        "frequency":           top_frequency,
        "top3_delta_out": [
            {
                "delta": f"0x{d:04X}",
                "count": c,
                "prob":  round(c / n_pairs, 6),
                "vs_uniform": round(c / uniform_expected, 2),
            }
            for d, c in top3
        ],
        "recovered_subkey_k7":    f"0x{best_k7:02X}",
        "true_subkey_k7":         f"0x{true_k7:02X}",
        "subkey_correct":         best_k7 == true_k7,
        "key_bits_identified":    key_bits_identified,
        "full_key_recovered":     full_key_recovered,
        "recovered_key":          (f"0x{recovered_key:06X}"
                                   if recovered_key is not None else None),
        "effort_to_full_recovery": "brute_force_remaining_bits_with_k7_hint",
    }

    os.makedirs(os.path.dirname(OUTPUT_JSON), exist_ok=True)
    with open(OUTPUT_JSON, "w") as f:
        json.dump(result, f, indent=2)

    print(f"\n[OK] Results saved → {OUTPUT_JSON}")
    print(json.dumps(result, indent=2))