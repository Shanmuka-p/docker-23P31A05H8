import os
from fastapi import FastAPI, HTTPException, Response
from pydantic import BaseModel
from crypto_utils import decrypt_seed, generate_totp_code, verify_totp_code

app = FastAPI()
SEED_FILE_PATH = os.getenv("SEED_PATH", "seed.txt")

class EncryptedSeedRequest(BaseModel):
    encrypted_seed: str

class VerifyCodeRequest(BaseModel):
    code: str

def get_stored_seed():
    if not os.path.exists(SEED_FILE_PATH):
        raise HTTPException(status_code=500, detail="Seed not decrypted yet")
    with open(SEED_FILE_PATH, "r") as f:
        return f.read().strip()

@app.post("/decrypt-seed")
def api_decrypt_seed(payload: EncryptedSeedRequest):
    try:
        hex_seed = decrypt_seed(payload.encrypted_seed, "student_private.pem")
        directory = os.path.dirname(SEED_FILE_PATH)
        if directory and not os.path.exists(directory):
            os.makedirs(directory)
        with open(SEED_FILE_PATH, "w") as f:
            f.write(hex_seed)
        return {"status": "ok"}
    except Exception:
        return Response(content='{"error": "Decryption failed"}', media_type="application/json", status_code=500)

@app.get("/generate-2fa")
def api_generate_2fa():
    hex_seed = get_stored_seed()
    return generate_totp_code(hex_seed)

@app.post("/verify-2fa")
def api_verify_2fa(payload: VerifyCodeRequest):
    hex_seed = get_stored_seed()
    return {"valid": verify_totp_code(hex_seed, payload.code)}