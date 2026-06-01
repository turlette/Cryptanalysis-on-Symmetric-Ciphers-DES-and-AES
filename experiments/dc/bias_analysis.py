"""
Task 3.2.5 [R] — DC Attack Part 2: Bias Analysis
=================================================
Load plaintext_pairs.csv, compute delta_out = c1 XOR c2,
count frequency histogram, identify top-3, save plot.

Deliverables:
    - plots/dc_bias_histogram.png
    - frequency table in stdout

Chạy từ root của repo:
    python experiments/dc/bias_analysis.py
"""

import os
import sys
import csv
from collections import Counter

import matplotlib
matplotlib.use("Agg")
import matplotlib.pyplot as plt
import matplotlib.ticker as ticker

# ---------------------------------------------------------------------------
# Config
# ---------------------------------------------------------------------------
ROOT_DIR   = os.path.join(os.path.dirname(__file__), "..", "..")
INPUT_CSV  = os.path.join(os.path.dirname(__file__), "plaintext_pairs.csv")
OUTPUT_PNG = os.path.join(ROOT_DIR, "plots", "dc_bias_histogram.png")
TOP_N      = 3


# ---------------------------------------------------------------------------
# Step 1: Load CSV
# ---------------------------------------------------------------------------
def load_pairs(path: str) -> list[dict]:
    with open(path, newline="") as f:
        return list(csv.DictReader(f))


# ---------------------------------------------------------------------------
# Step 2: Compute delta_out = c1 XOR c2
# (CSV đã có sẵn delta_out, nhưng tính lại để đảm bảo chính xác)
# ---------------------------------------------------------------------------
def compute_delta_out(records: list[dict]) -> list[int]:
    deltas = []
    for r in records:
        c1 = int(r["ciphertext1"], 16)
        c2 = int(r["ciphertext2"], 16)
        deltas.append(c1 ^ c2)
    return deltas


# ---------------------------------------------------------------------------
# Step 3 & 4: Count + print frequency table
# ---------------------------------------------------------------------------
def count_frequency(deltas: list[int]) -> Counter:
    return Counter(deltas)


def print_frequency_table(freq: Counter, total: int, top_n: int = 15) -> None:
    uniform_expected = total / 0xFFFF
    print(f"\n{'='*60}")
    print(f"  delta_out Frequency Table  (total pairs: {total})")
    print(f"  Uniform baseline: {uniform_expected:.2f} counts per delta_out")
    print(f"{'='*60}")
    print(f"  {'Rank':<5} {'delta_out':<12} {'count':<8} {'prob':<12} {'vs uniform'}")
    print(f"  {'-'*54}")
    for rank, (delta, count) in enumerate(freq.most_common(top_n), 1):
        prob  = count / total
        ratio = count / uniform_expected
        mark  = " ◀ BIAS" if rank <= TOP_N else ""
        print(f"  {rank:<5} 0x{delta:04X}       {count:<8} {prob:<12.6f} {ratio:.1f}x{mark}")
    print(f"{'='*60}\n")


# ---------------------------------------------------------------------------
# Step 5: Plot histogram
# ---------------------------------------------------------------------------
def plot_histogram(freq: Counter, total: int, top_n: int, output_path: str) -> None:
    os.makedirs(os.path.dirname(output_path), exist_ok=True)

    top_items  = freq.most_common(20)
    labels     = [f"0x{d:04X}" for d, _ in top_items]
    counts     = [c for _, c in top_items]
    colors     = ["#E63946" if i < top_n else "#457B9D"
                  for i in range(len(top_items))]

    fig, ax = plt.subplots(figsize=(14, 6))
    bars = ax.bar(range(len(top_items)), counts, color=colors,
                  edgecolor="white", linewidth=0.5)

    # Label on each bar
    for bar, count in zip(bars, counts):
        ax.text(bar.get_x() + bar.get_width() / 2,
                bar.get_height() + total * 0.0008,
                str(count), ha="center", va="bottom",
                fontsize=8, color="#222222")

    # Uniform baseline
    uniform = total / 0xFFFF
    ax.axhline(uniform, color="#2D6A4F", linestyle="--",
               linewidth=1.4, label=f"Uniform baseline ({uniform:.2f})")

    ax.set_xticks(range(len(top_items)))
    ax.set_xticklabels(labels, rotation=45, ha="right", fontsize=8)
    ax.set_xlabel("delta_out  (c1 XOR c2)", fontsize=11)
    ax.set_ylabel("Frequency", fontsize=11)
    ax.set_title(
        "Differential Cryptanalysis — Output Difference Histogram (MiniDES)\n"
        f"Top-20 delta_out  |  Total pairs: {total}  |  🔴 = Top-{top_n} biased",
        fontsize=12, pad=12,
    )
    ax.legend(fontsize=10)
    ax.set_facecolor("#F8F9FA")
    fig.patch.set_facecolor("#FFFFFF")
    plt.tight_layout()
    plt.savefig(output_path, dpi=150, bbox_inches="tight")
    plt.close()
    print(f"[OK] Histogram saved → {output_path}")


# ---------------------------------------------------------------------------
# Entry point
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print(f"Loading {INPUT_CSV} ...")
    records = load_pairs(INPUT_CSV)
    total   = len(records)
    print(f"  Loaded {total} pairs.")

    deltas = compute_delta_out(records)
    freq   = count_frequency(deltas)

    print_frequency_table(freq, total, top_n=15)

    print(f"Top-{TOP_N} most-frequent delta_out:")
    for rank, (delta, count) in enumerate(freq.most_common(TOP_N), 1):
        print(f"  [{rank}] 0x{delta:04X}  count={count}  "
              f"prob={count/total:.6f}  ({count/(total/0xFFFF):.1f}x uniform)")

    plot_histogram(freq, total, TOP_N, OUTPUT_PNG)