# Cryptanalysis-on-Symmetric-Ciphers-DES-and-AES
```
project-root/
  ├─ docker/             # docker-compose files for vulnerable services + attacker tools
  ├── mini_des/
│ |   ├── mini_des.py (cipher implementation)
│ |   └── tests/
│ |   └── test_mini_des.py (unit tests)
  ├─ experiments/
  |   ├─ exp_des_bruteforce/
  |   ├─ exp_padding_oracle/
  |   ├─ exp_differential_cryptanalysis/        
  ├─ docs/               # report, slides, runbook
  ├─ scripts/            # automation scripts to run experiments and collect logs
  └─ data/               # non-sensitive raw outputs (timing logs, trace counts, csvs)
  ```