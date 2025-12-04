import sys, subprocess, base64
from cryptography.hazmat.primitives import hashes, serialization
from cryptography.hazmat.primitives.asymmetric import padding

def generate_proof():
    try:
        commit_hash = subprocess.check_output(['git', 'log', '-1', '--format=%H']).decode('utf-8').strip()
        print(f"✅ Commit Hash: {commit_hash}")
    except:
        print("❌ Git Error")
        return

    with open("student_private.pem", "rb") as f:
        private_key = serialization.load_pem_private_key(f.read(), password=None)

    signature = private_key.sign(
        commit_hash.encode('utf-8'),
        padding.PSS(mgf=padding.MGF1(hashes.SHA256()), salt_length=padding.PSS.MAX_LENGTH),
        hashes.SHA256()
    )

    with open("instructor_public.pem", "rb") as f:
        inst_key = serialization.load_pem_public_key(f.read())

    enc_sig = inst_key.encrypt(
        signature,
        padding.OAEP(mgf=padding.MGF1(hashes.SHA256()), algorithm=hashes.SHA256(), label=None)
    )
    print("\n⬇️ ENCRYPTED SIGNATURE ⬇️")
    print(base64.b64encode(enc_sig).decode('utf-8'))

if __name__ == "__main__":
    generate_proof()