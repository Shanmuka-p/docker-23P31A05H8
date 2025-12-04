import base64
import time
import pyotp
import hashlib
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

def decrypt_seed(encrypted_seed_b64: str, private_key_path: str = "student_private.pem") -> str:
    try:
        with open(private_key_path, "rb") as key_file:
            private_key = serialization.load_pem_private_key(key_file.read(), password=None)

        encrypted_bytes = base64.b64decode(encrypted_seed_b64)
        decrypted_bytes = private_key.decrypt(
            encrypted_bytes,
            padding.OAEP(mgf=padding.MGF1(algorithm=hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
        )
        return decrypted_bytes.decode('utf-8')
    except Exception as e:
        print(f"Decryption failed: {str(e)}")
        raise e

def generate_totp_code(hex_seed: str):
    seed_bytes = bytes.fromhex(hex_seed)
    base32_seed = base64.b32encode(seed_bytes).decode('utf-8')
    totp = pyotp.TOTP(base32_seed, digits=6, interval=30, digest=hashlib.sha1)
    time_remaining = int(totp.interval - (time.time() % totp.interval))
    return {"code": totp.now(), "valid_for": time_remaining}

def verify_totp_code(hex_seed: str, code: str) -> bool:
    seed_bytes = bytes.fromhex(hex_seed)
    base32_seed = base64.b32encode(seed_bytes).decode('utf-8')
    totp = pyotp.TOTP(base32_seed, digits=6, interval=30, digest=hashlib.sha1)
    return totp.verify(code, valid_window=1)