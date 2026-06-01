import os
import subprocess
import time
import sys

def main():
    base_dir = os.path.abspath(os.path.join(os.path.dirname(__file__), '..'))
    exp_dir = os.path.join(base_dir, 'experiments')
    
    print("="*65)
    print("      AUTOMATED EXPERIMENT RUNNER (WEEK 11-12 AUTOMATION)      ")
    print("="*65)
    
    # 1. Experiment A
    print("\n[1] Running Experiment A: DES Brute-force")
    exp_a_dir = os.path.join(exp_dir, 'exp_des_bruteforce')
    subprocess.run([sys.executable, 'bruteforce_simulator.py'], cwd=exp_a_dir)
    
    # 2. Experiment B
    print("\n[2] Running Experiment B: AES Padding Oracle")
    exp_b_dir = os.path.join(exp_dir, 'exp_padding_oracle')
    print("    -> Khởi động Server mục tiêu (Vulnerable)...")
    server_proc = subprocess.Popen([sys.executable, 'server.py'], cwd=exp_b_dir, 
                                   stdout=subprocess.DEVNULL, stderr=subprocess.DEVNULL)
    time.sleep(2) # Chờ server khởi động
    print("    -> Khởi chạy kịch bản Tấn công (Attacker)...")
    subprocess.run([sys.executable, 'attacker.py'], cwd=exp_b_dir)
    print("    -> Đóng Server mục tiêu...")
    server_proc.terminate()
    server_proc.wait()

    # 3. Experiment C
    print("\n[3] Running Experiment C: AES-GCM Nonce Reuse")
    exp_c_dir = os.path.join(exp_dir, 'exp_gcm_nonce_reuse')
    subprocess.run([sys.executable, 'gcm_attacker.py'], cwd=exp_c_dir)
    
    # 4. Experiment D
    print("\n[4] Running Experiment D: AES Side-channel (CPA)")
    exp_d_dir = os.path.join(exp_dir, 'exp_sidechannel')
    subprocess.run([sys.executable, 'sidechannel_attacker.py'], cwd=exp_d_dir)
    
    print("\n" + "="*65)
    print("[+] TẤT CẢ THỬ NGHIỆM ĐÃ HOÀN TẤT THÀNH CÔNG.")
    print("[+] Vui lòng chạy lệnh: `python scripts/analyze_results.py` để xem báo cáo thống kê.")
    print("="*65)

if __name__ == "__main__":
    main()
