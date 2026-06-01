"""
Task 3.1.5 [R] — DC Attack Part 1: Pair Collection
===================================================
Generate 2048 plaintext pairs, encrypt with Mini-DES,
compute delta_in = p1 XOR p2, save to CSV.

Output: experiments/dc/plaintext_pairs.csv

Chạy từ root của repo:
    python experiments/dc/collect_plaintext_pairs.py
"""

import os
import sys
import csv
import random

# Đảm bảo import được mini_des từ root repo
sys.path.insert(0, os.path.join(os.path.dirname(__file__), "..", ".."))

from mini_des.mini_des import MiniDES

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
N_PAIRS    = 2048
KEY        = 0b101000001011001100  # 24-bit key — thay đổi nếu cần
OUTPUT_DIR = os.path.join(os.path.dirname(__file__))
OUTPUT_CSV = os.path.join(OUTPUT_DIR, "plaintext_pairs.csv")


# ---------------------------------------------------------------------------
# Main: collect_plaintext_pairs
# ---------------------------------------------------------------------------
def collect_plaintext_pairs(n_pairs: int, key: int) -> list[dict]:
    """
    Generate n_pairs random 16-bit plaintext pairs,
    encrypt cả 2 bằng MiniDES, tính delta_in = p1 XOR p2.

    MiniDES specs:
        - Block size : 16 bits
        - Key size   : 24 bits
        - Rounds     : 8 (Feistel)
        - F-function : ((R ^ subkey) + 0x42) & 0xFF

    Returns:
        List of dicts:
        plaintext1, plaintext2, ciphertext1, ciphertext2, delta_in, delta_out
    """
    des     = MiniDES(key)
    records = []

    for _ in range(n_pairs):
        p1 = random.randint(0, 0xFFFF)   # random 16-bit plaintext
        p2 = random.randint(0, 0xFFFF)   # random independent plaintext

        c1 = des.encrypt(p1)
        c2 = des.encrypt(p2)

        delta_in  = p1 ^ p2
        delta_out = c1 ^ c2

        records.append({
            "plaintext1":  f"0x{p1:04X}",
            "plaintext2":  f"0x{p2:04X}",
            "ciphertext1": f"0x{c1:04X}",
            "ciphertext2": f"0x{c2:04X}",
            "delta_in":    f"0x{delta_in:04X}",
            "delta_out":   f"0x{delta_out:04X}",
        })

    return records


def save_to_csv(records: list[dict], path: str) -> None:
    os.makedirs(os.path.dirname(path), exist_ok=True)
    fieldnames = ["plaintext1", "plaintext2",
                  "ciphertext1", "ciphertext2",
                  "delta_in", "delta_out"]
    with open(path, "w", newline="") as f:
        writer = csv.DictWriter(f, fieldnames=fieldnames)
        writer.writeheader()
        writer.writerows(records)
    print(f"[OK] Saved {len(records)} pairs → {path}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print(f"MiniDES key: 0x{KEY:06X}  (24-bit)")
    print(f"Generating {N_PAIRS} plaintext pairs...")

    records = collect_plaintext_pairs(N_PAIRS, KEY)
    save_to_csv(records, OUTPUT_CSV)

    print("\nPreview (first 3 rows):")
    for r in records[:3]:
        print(f"  P1={r['plaintext1']}  P2={r['plaintext2']}"
              f"  C1={r['ciphertext1']}  C2={r['ciphertext2']}"
              f"  ΔIn={r['delta_in']}  ΔOut={r['delta_out']}")