from flask import Flask, jsonify
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import os

app = Flask(__name__)

# Sinh khóa tĩnh ngẫu nhiên khi khởi động server
SECRET_KEY = os.urandom(16)
# Plaintext dài hơn 1 block để minh họa rõ khả năng giải mã tuần tự của attacker
SECRET_MESSAGE = "TopSecret: This is a highly confidential message for padding oracle lab!"

@app.route('/encrypt', methods=['GET'])
def encrypt_message():
    """Endpoint mô phỏng việc server cấp một encrypted token cho client."""
    iv = os.urandom(16)
    cipher = AES.new(SECRET_KEY, AES.MODE_CBC, iv)
    padded_msg = pad(SECRET_MESSAGE.encode('utf-8'), AES.block_size)
    ciphertext = cipher.encrypt(padded_msg)
    
    # Trả về chuỗi hex chứa cả IV và Ciphertext
    payload = iv + ciphertext
    return jsonify({"ciphertext": payload.hex()})

@app.route('/decrypt/<payload_hex>', methods=['GET'])
def decrypt_message(payload_hex):
    """Endpoint nhận token, giải mã và xử lý nghiệp vụ."""
    try:
        payload = bytes.fromhex(payload_hex)
        if len(payload) < 32 or len(payload) % 16 != 0:
            return jsonify({"error": "Invalid payload length"}), 400
            
        iv = payload[:16]
        ciphertext = payload[16:]
        
        cipher = AES.new(SECRET_KEY, AES.MODE_CBC, iv)
        decrypted_padded = cipher.decrypt(ciphertext)
        
        # LỖ HỔNG (VULNERABILITY): Hàm unpad ném ra ValueError nếu padding sai.
        decrypted = unpad(decrypted_padded, AES.block_size)
        
        # Xử lý nghiệp vụ giả lập (kiểm tra định dạng)
        text = decrypted.decode('utf-8')
        if not text.startswith("TopSecret"):
            return jsonify({"error": "Invalid token format"}), 400
            
        return jsonify({"message": "Token accepted!"}), 200
        
    except ValueError as e:
        # LỖ HỔNG LÀ ĐÂY: Trả về một mã lỗi và thông báo ĐẶC TRƯNG khi padding sai (HTTP 500).
        # Điều này cho phép Attacker biết chính xác khi nào họ đã đoán đúng 1 byte padding.
        if "padding is incorrect" in str(e).lower() or "padding" in str(e).lower():
            return jsonify({"error": "Invalid Padding"}), 500
        return jsonify({"error": "Decryption error"}), 500
    except Exception as e:
        return jsonify({"error": "Unknown error"}), 500

if __name__ == '__main__':
    print("[*] Starting VULNERABLE Server on port 5000")
    print("[!] Warning: This server is intentionally vulnerable to Padding Oracle attack.")
    app.run(port=5000)
