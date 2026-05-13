import time
import sys
import os

sys.path.append(
    os.path.abspath(
        os.path.join(os.path.dirname(__file__), "../..")
    )
)

from mini_des.mini_des import MiniDES

def brute_force_attack(known_plaintext, known_ciphertext):
    """
    Try all possible 24-bit keys until the ciphertext matches.
    """

    start_time = time.time()

    for key in range(2**24):

        cipher = MiniDES(key)

        encrypted = cipher.encrypt(known_plaintext)

        if encrypted == known_ciphertext:

            end_time = time.time()

            return {
                "found_key": key,
                "time_taken": end_time - start_time,
                "attempts": key + 1
            }

    return None


def main():

    # Secret key used by victim
    secret_key = 0x123456

    # Known plaintext
    plaintext = 0xABCD

    # Victim encrypts plaintext
    victim_cipher = MiniDES(secret_key)
    ciphertext = victim_cipher.encrypt(plaintext)

    print("=" * 50)
    print("MINI-DES BRUTE FORCE DEMO")
    print("=" * 50)

    print(f"Known plaintext : {hex(plaintext)}")
    print(f"Known ciphertext: {hex(ciphertext)}")

    print("\nStarting brute-force attack...")
    print("Searching all possible 24-bit keys...\n")

    result = brute_force_attack(plaintext, ciphertext)

    if result:

        print("=" * 50)
        print("KEY FOUND")
        print("=" * 50)

        print(f"Recovered key : {hex(result['found_key'])}")
        print(f"Attempts       : {result['attempts']}")
        print(f"Time taken     : {result['time_taken']:.4f} seconds")

    else:
        print("Key not found.")


if __name__ == "__main__":
    main()