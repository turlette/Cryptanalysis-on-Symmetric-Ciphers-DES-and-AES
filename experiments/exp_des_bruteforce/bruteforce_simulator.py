import time
import csv
import os
import itertools
from Crypto.Cipher import DES
from Crypto.Util.Padding import unpad
from des_harness import encrypt_message, generate_key

def brute_force(ciphertext, known_prefix, difficulty_bytes, expected_plaintext):
    """
    Simulates a brute-force attack by guessing the missing bytes of the key.
    """
    print(f"[*] Starting brute-force...")
    print(f"[*] Known key prefix (hex): {known_prefix.hex()}")
    print(f"[*] Missing bytes: {difficulty_bytes}")
    
    start_time = time.time()
    attempts = 0
    found_key = None
    
    # Generate all possible combinations for the missing bytes
    # e.g., if difficulty_bytes=2, it generates (0,0) to (255,255)
    combinations = itertools.product(range(256), repeat=difficulty_bytes)
    
    for guess in combinations:
        attempts += 1
        guess_bytes = bytes(guess)
        full_key_guess = known_prefix + guess_bytes
        
        try:
            cipher = DES.new(full_key_guess, DES.MODE_ECB)
            decrypted_padded = cipher.decrypt(ciphertext)
            # Try to unpad
            decrypted = unpad(decrypted_padded, DES.block_size)
            # Verify if the decrypted text matches our expected plaintext
            # (In a real attack, we'd check for printable characters or known formats)
            if decrypted.decode('utf-8') == expected_plaintext:
                found_key = full_key_guess
                break
        except (ValueError, KeyError, UnicodeDecodeError):
            # ValueError/KeyError if unpad fails, UnicodeDecodeError if decode fails
            continue

    end_time = time.time()
    duration = end_time - start_time
    keys_per_second = attempts / duration if duration > 0 else 0
    
    return found_key, attempts, duration, keys_per_second

def main():
    # 1. Configuration
    difficulty_bytes = 3 # Number of bytes to brute-force (3 bytes = 2^(3*8) combinations)
    plaintext = "Top Secret 2026!"
    
    # 2. Setup targets
    original_key = generate_key()
    ciphertext = encrypt_message(plaintext, original_key)
    
    # Split key into known part and missing part
    known_prefix = original_key[:-difficulty_bytes]
    missing_part = original_key[-difficulty_bytes:]
    
    print(f"--- DES Brute-Force Simulator ---")
    print(f"Plaintext: {plaintext}")
    print(f"Original Key (hex): {original_key.hex()}")
    print(f"Ciphertext (hex): {ciphertext.hex()}")
    print(f"Difficulty: Guessing the last {difficulty_bytes} bytes ({8 * difficulty_bytes} bits)")
    print(f"Total possible combinations: {2**(8 * difficulty_bytes)}")
    print("-" * 35)
    
    # 3. Execute Brute-force Attack
    found_key, attempts, duration, kps = brute_force(ciphertext, known_prefix, difficulty_bytes, plaintext)
    
    if found_key:
        print(f"\n[+] SUCCESS! Key found: {found_key.hex()}")
    else:
        print(f"\n[-] FAILURE. Key not found after {attempts} attempts.")
        
    print(f"[*] Time taken: {duration:.4f} seconds")
    print(f"[*] Speed: {kps:,.2f} keys/second")
    print(f"[*] Total attempts: {attempts}")
    
    # 4. Log results to CSV
    log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data'))
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'des_bruteforce_log.csv')
    
    file_exists = os.path.isfile(log_file)
    with open(log_file, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['Timestamp', 'Plaintext', 'Original Key (hex)', 'Found Key (hex)', 'Difficulty (bytes)', 'Attempts', 'Time (s)', 'Speed (keys/s)'])
        
        writer.writerow([
            time.strftime("%Y-%m-%d %H:%M:%S"),
            plaintext,
            original_key.hex(),
            found_key.hex() if found_key else "NOT_FOUND",
            difficulty_bytes,
            attempts,
            round(duration, 4),
            round(kps, 2)
        ])
    print(f"\n[+] Results automatically logged to: {os.path.relpath(log_file, os.path.dirname(__file__))}")

if __name__ == "__main__":
    main()
