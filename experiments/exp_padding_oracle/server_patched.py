from flask import Flask, jsonify
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os
import time

app = Flask(__name__)

SECRET_KEY = os.urandom(16)
SECRET_MESSAGE = "TopSecret: This is a patched confidential message!"

@app.route('/encrypt', methods=['GET'])
def encrypt_message():
    iv = os.urandom(16)
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, iv)
    padded_msg = pad(SECRET_MESSAGE.encode('utf-8'), AES.block_size)
    ciphertext = cipher.encrypt(padded_msg)
    payload = iv + ciphertext
    return jsonify({"ciphertext": payload.hex()})

@app.route('/decrypt/<payload_hex>', methods=['GET'])
def decrypt_message(payload_hex):
    # Sử dụng delay giả lập để giảm thiểu khác biệt thời gian xử lý (Timing attack mitigation)
    # Tuy nhiên, cách tốt nhất trong thực tế vẫn là dùng Authenticated Encryption (như AES-GCM)
    start_time = time.time()
    try:
        payload = bytes.fromhex(payload_hex)
        if len(payload) < 32 or len(payload) % 16 != 0:
            return jsonify({"error": "Invalid request"}), 400
            
        iv = payload[:16]
        ciphertext = payload[16:]
        
        cipher = AES.new(SECRET_KEY, AES.MODE_CBC, iv)
        decrypted_padded = cipher.decrypt(ciphertext)
        
        # Thử unpad và parse logic
        decrypted = unpad(decrypted_padded, AES.block_size)
        text = decrypted.decode('utf-8')
        
        if not text.startswith("TopSecret"):
            raise ValueError("Business logic failed")
            
        return jsonify({"message": "Token accepted!"}), 200
        
    except Exception as e:
        # BẢN VÁ (MITIGATION): Uniform error handling.
        # Bất kể lỗi là do Padding sai, Decode sai, hay Business logic sai, 
        # Server luôn trả về cùng một mã lỗi HTTP 400 và cùng một thông báo.
        # Từ đó, Attacker không thể dùng phản hồi server để làm "Oracle" nữa.
        return jsonify({"error": "Invalid request"}), 400
        
    finally:
        # Cân bằng thời gian phản hồi (Constant-time-ish delay)
        elapsed = time.time() - start_time
        if elapsed < 0.05:
            time.sleep(0.05 - elapsed)

if __name__ == '__main__':
    print("[*] Starting PATCHED Server on port 5000")
    print("[!] Uniform error handling enabled. Attacker cannot distinguish padding errors.")
    app.run(port=5000)
