#!/usr/bin/env python3
import sys, os, datetime
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '..')))
from crypto_utils import generate_totp_code

SEED_FILE_PATH = os.getenv("SEED_PATH", "/data/seed.txt")

def job():
    if not os.path.exists(SEED_FILE_PATH):
        return
    with open(SEED_FILE_PATH, "r") as f:
        hex_seed = f.read().strip()
    result = generate_totp_code(hex_seed)
    now_utc = datetime.datetime.now(datetime.timezone.utc).strftime("%Y-%m-%d %H:%M:%S")
    print(f"{now_utc} - 2FA Code: {result['code']}")

if __name__ == "__main__":
    job()