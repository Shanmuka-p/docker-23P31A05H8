from cryptography.hazmat.primitives.asymmetric import rsa
from cryptography.hazmat.primitives import serialization

def generate_rsa_keypair(key_size: int = 4096):
    print(f"Generating {key_size}-bit RSA key pair...")
    private_key = rsa.generate_private_key(public_exponent=65537, key_size=key_size)
    public_key = private_key.public_key()

    
    pem_private = private_key.private_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PrivateFormat.PKCS8,
        encryption_algorithm=serialization.NoEncryption()
    )
    with open("student_private.pem", "wb") as f:
        f.write(pem_private)

    
    pem_public = public_key.public_bytes(
        encoding=serialization.Encoding.PEM,
        format=serialization.PublicFormat.SubjectPublicKeyInfo
    )
    with open("student_public.pem", "wb") as f:
        f.write(pem_public)

    print("✅ Keys generated: student_private.pem, student_public.pem")

if __name__ == "__main__":
    generate_rsa_keypair()