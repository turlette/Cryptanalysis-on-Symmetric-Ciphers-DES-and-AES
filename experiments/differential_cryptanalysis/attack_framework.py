"""
Differential Cryptanalysis Attack Framework
============================================
Task 2.2.6 [R] — Mini-AES Reference & DC Framework

Reference: Biham & Shamir (1993)
         "Differential Cryptanalysis of the Data Encryption Standard"

Mini-AES Reference Implementation:
  - pycryptodome AES used as placeholder (full AES)
  - Replace self.cipher with Mini-AES once implemented

Usage:
    from Crypto.Cipher import AES
    import os

    key = os.urandom(16)
    cipher_func = lambda pt: AES.new(key, AES.MODE_ECB).encrypt(pt)

    attack = DifferentialAttack(cipher_func)
    pairs = attack.collect_pairs(n_pairs=1000, delta_in=b'\\x00' * 15 + b'\\x01')
    bias  = attack.analyze_bias(pairs, delta_in=b'\\x00' * 15 + b'\\x01')
"""

import os
import random
from collections import defaultdict
from typing import Callable, List, Tuple, Dict


# ---------------------------------------------------------------------------
# Type aliases
# ---------------------------------------------------------------------------
Plaintext  = bytes
Ciphertext = bytes
PairList   = List[Tuple[Ciphertext, Ciphertext]]  # list of (C, C') pairs


# ---------------------------------------------------------------------------
# Mini-AES placeholder (pycryptodome full AES — swap out later)
# ---------------------------------------------------------------------------
def _default_cipher_func(plaintext: bytes) -> bytes:
    """
    Placeholder cipher using pycryptodome AES-128 ECB.
    Replace with actual Mini-AES implementation when available.

    Args:
        plaintext: 16-byte block

    Returns:
        16-byte ciphertext block
    """
    try:
        from Crypto.Cipher import AES  # pycryptodome
        # NOTE: key is fixed here for demo — in real use, inject via __init__
        _KEY = bytes.fromhex("00112233445566778899aabbccddeeff")
        cipher = AES.new(_KEY, AES.MODE_ECB)
        return cipher.encrypt(plaintext)
    except ImportError:
        raise ImportError(
            "pycryptodome not installed. Run: pip install pycryptodome"
        )


# ---------------------------------------------------------------------------
# Main class
# ---------------------------------------------------------------------------
class DifferentialAttack:
    """
    Framework for performing differential cryptanalysis on a block cipher.

    Follows the methodology of Biham & Shamir (1993):
      1. Choose a differential characteristic (ΔP → ΔC*) with high probability
      2. Collect plaintext pairs with input difference = delta_in
      3. Analyze output difference bias across pairs
      4. Use bias to recover key bits (last-round subkey attack)

    Attributes:
        cipher      : Callable — encryption oracle, takes bytes → bytes
        block_size  : int      — block size in bytes (default: 16 for AES)
        _collected  : int      — number of pairs collected so far
    """

    def __init__(
        self,
        cipher_func: Callable[[bytes], bytes] = None,
        block_size: int = 16,
    ):
        """
        Initialize the differential attack framework.

        Args:
            cipher_func : Encryption oracle function (plaintext bytes → ciphertext bytes).
                          Defaults to pycryptodome AES placeholder if None.
            block_size  : Block size in bytes. Default 16 (AES-128).
        """
        self.cipher     = cipher_func if cipher_func is not None else _default_cipher_func
        self.block_size = block_size
        self._collected = 0

    # -----------------------------------------------------------------------
    # Phase 2: Collect plaintext pairs
    # -----------------------------------------------------------------------
    def collect_pairs(
        self,
        n_pairs: int,
        delta_in: bytes,
    ) -> PairList:
        """
        Collect plaintext pairs with input difference = delta_in,
        then encrypt both and return the ciphertext pairs.

        Differential input:
            P' = P ⊕ delta_in
            (C, C') = (cipher(P), cipher(P'))

        Args:
            n_pairs  : Number of plaintext pairs to generate and encrypt.
            delta_in : Input XOR difference (bytes, same length as block_size).

        Returns:
            List of (C, C') ciphertext pairs.

        Raises:
            ValueError: If delta_in length does not match block_size.
        """
        if len(delta_in) != self.block_size:
            raise ValueError(
                f"delta_in length {len(delta_in)} != block_size {self.block_size}"
            )

        pairs: PairList = []

        for _ in range(n_pairs):
            # Choose random plaintext P
            P = os.urandom(self.block_size)

            # Compute P' = P ⊕ delta_in
            P_prime = bytes(p ^ d for p, d in zip(P, delta_in))

            # Query cipher oracle
            C       = self.cipher(P)
            C_prime = self.cipher(P_prime)

            pairs.append((C, C_prime))

        self._collected += n_pairs
        print(f"[collect_pairs] Collected {n_pairs} pairs "
              f"(total so far: {self._collected})")
        return pairs

    # -----------------------------------------------------------------------
    # Phase 3: Analyze output difference bias
    # -----------------------------------------------------------------------
    def analyze_bias(
        self,
        pairs: PairList,
        delta_in: bytes,
    ) -> Dict[bytes, int]:
        """
        Count output differences across all ciphertext pairs to find bias.

        For each pair (C, C'), compute:
            delta_out = C ⊕ C'

        Then count frequency of each delta_out. A biased (non-uniform)
        distribution indicates a valid differential characteristic.

        Args:
            pairs    : List of (C, C') ciphertext pairs from collect_pairs().
            delta_in : The input difference used (for reporting only).

        Returns:
            Dict mapping delta_out (bytes) → count (int), sorted by frequency.
        """
        diff_count: Dict[bytes, int] = defaultdict(int)

        for C, C_prime in pairs:
            delta_out = bytes(c ^ cp for c, cp in zip(C, C_prime))
            diff_count[delta_out] += 1

        # Sort by count descending
        sorted_bias = dict(
            sorted(diff_count.items(), key=lambda x: x[1], reverse=True)
        )

        # Report top-5 most frequent output differences
        print(f"\n[analyze_bias] Input difference: {delta_in.hex()}")
        print(f"[analyze_bias] Total pairs analyzed: {len(pairs)}")
        print(f"[analyze_bias] Unique output differences found: {len(sorted_bias)}")
        print(f"\n  Top-5 output differences (possible characteristic signals):")
        for i, (delta_out, count) in enumerate(list(sorted_bias.items())[:5]):
            prob = count / len(pairs)
            print(f"  [{i+1}] ΔC = {delta_out.hex()}  count={count}  prob={prob:.6f}")

        return sorted_bias

    # -----------------------------------------------------------------------
    # Phase 4: Last-round subkey recovery (skeleton — to be implemented)
    # -----------------------------------------------------------------------
    def recover_subkey(
        self,
        pairs: PairList,
        expected_delta_out: bytes,
        subkey_space: int = 256,
    ) -> Dict[int, int]:
        """
        [SKELETON] Recover last-round subkey by counting right pairs.

        For each subkey candidate k:
          - Partially decrypt last round of each C and C' using k
          - Check if resulting difference matches expected_delta_out
          - Count "right pairs" for each k

        The k with highest count is the correct subkey.

        Args:
            pairs              : Ciphertext pairs from collect_pairs().
            expected_delta_out : The expected output difference from the characteristic.
            subkey_space       : Number of subkey candidates to test (default 256).

        Returns:
            Dict mapping subkey_candidate (int) → right_pair_count (int).

        TODO:
            - Implement decrypt_last_round() for Mini-DES / Mini-AES
            - Integrate with actual S-box inverse
        """
        # TODO: implement last-round partial decryption
        subkey_count: Dict[int, int] = defaultdict(int)

        for k in range(subkey_space):
            for C, C_prime in pairs:
                # T       = self._decrypt_last_round(C, k)
                # T_prime = self._decrypt_last_round(C_prime, k)
                # delta_t = bytes(a ^ b for a, b in zip(T, T_prime))
                # if delta_t == expected_delta_out:
                #     subkey_count[k] += 1
                pass  # placeholder

        print("[recover_subkey] TODO: implement last-round decryption")
        return subkey_count

    # -----------------------------------------------------------------------
    # Utility
    # -----------------------------------------------------------------------
    def xor_bytes(self, a: bytes, b: bytes) -> bytes:
        """XOR two byte strings of equal length."""
        return bytes(x ^ y for x, y in zip(a, b))

    def __repr__(self) -> str:
        return (
            f"DifferentialAttack("
            f"block_size={self.block_size}, "
            f"pairs_collected={self._collected})"
        )


# ---------------------------------------------------------------------------
# Quick smoke test
# ---------------------------------------------------------------------------
if __name__ == "__main__":
    print("=" * 60)
    print("Differential Attack Framework — Smoke Test")
    print("Using pycryptodome AES as placeholder cipher")
    print("=" * 60)

    # Init attack with default AES placeholder
    attack = DifferentialAttack()
    print(f"\nInitialized: {attack}\n")

    # Define input difference (single bit flip in last byte)
    delta_in = b"\x00" * 15 + b"\x01"

    # Phase 2: collect pairs
    pairs = attack.collect_pairs(n_pairs=500, delta_in=delta_in)

    # Phase 3: analyze bias
    bias = attack.analyze_bias(pairs, delta_in=delta_in)

    print("\n[OK] Framework running. Replace cipher_func with Mini-AES when ready.")