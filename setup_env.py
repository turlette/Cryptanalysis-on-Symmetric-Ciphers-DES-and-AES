import os

def create_structure(base_dir):
    structure = {
        "docker": ["docker-compose.yml"],
        "experiments": {
            "exp_des_bruteforce": ["README.md", "des_bruteforce.py"],
            "exp_padding_oracle": ["README.md", "padding_oracle.py"],
            "exp_gcm_nonce_reuse": ["README.md", "gcm_nonce_reuse.py"],
            "exp_sidechannel": ["README.md", "sidechannel.py"],
        },
        "docs": ["report.md", "runbook.md"],
        "scripts": ["run_all.sh"],
        "data": [".gitkeep"],
    }

    print(f"Creating directory structure in {base_dir}...\n")

    for main_item, content in structure.items():
        main_path = os.path.join(base_dir, main_item)
        os.makedirs(main_path, exist_ok=True)
        print(f"[+] Directory: {main_path}")

        if isinstance(content, list):
            # Create files in main directory
            for file_name in content:
                file_path = os.path.join(main_path, file_name)
                if not os.path.exists(file_path):
                    with open(file_path, "w", encoding="utf-8") as f:
                        if file_name.endswith('.md'):
                            f.write(f"# {file_name}\n\nPlaceholder content.")
                        elif file_name.endswith('.py'):
                            f.write(f"# Python placeholder for {file_name}\n")
                        elif file_name.endswith('.sh'):
                            f.write(f"#!/bin/bash\n# Shell script placeholder for {file_name}\n")
                    print(f"  [-] Created file: {file_name}")
        elif isinstance(content, dict):
            # Create subdirectories and files
            for sub_dir, sub_files in content.items():
                sub_path = os.path.join(main_path, sub_dir)
                os.makedirs(sub_path, exist_ok=True)
                print(f"  [+] Sub-directory: {sub_path}")
                
                for file_name in sub_files:
                    file_path = os.path.join(sub_path, file_name)
                    if not os.path.exists(file_path):
                        with open(file_path, "w", encoding="utf-8") as f:
                            if file_name.endswith('.md'):
                                f.write(f"# {sub_dir}\n\nPlaceholder for {sub_dir} experiment.")
                            elif file_name.endswith('.py'):
                                f.write(f"# Implementation for {sub_dir}\n")
                        print(f"    [-] Created file: {file_name}")

    print("\nEnvironment setup complete!")

if __name__ == "__main__":
    current_dir = os.path.abspath(os.path.dirname(__file__))
    create_structure(current_dir)
