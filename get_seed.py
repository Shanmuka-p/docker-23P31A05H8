import requests
import json
import sys


STUDENT_ID = "23P31A05H8" 
GITHUB_REPO_URL = "https://github.com/Shanmuka-p/docker-23P31A05H8" 

API_URL = "https://eajeyq4r3zljoq4rpovy2nthda0vtjqf.lambda-url.ap-south-1.on.aws"

def get_encrypted_seed():
    try:
        with open("student_public.pem", "r") as f:
            public_key_content = f.read()
    except FileNotFoundError:
        print("❌ student_public.pem not found")
        return

    payload = {
        "student_id": STUDENT_ID,
        "github_repo_url": GITHUB_REPO_URL,
        "public_key": public_key_content
    }

    try:
        response = requests.post(API_URL, json=payload, timeout=10)
        if response.status_code == 200:
            data = response.json()
            if "encrypted_seed" in data:
                with open("encrypted_seed.txt", "w") as f:
                    f.write(data["encrypted_seed"])
                print("✅ Encrypted seed saved to encrypted_seed.txt")
            else:
                print("❌ Error:", data)
        else:
            print(f"❌ API Error {response.status_code}: {response.text}")
    except Exception as e:
        print(f"❌ Connection Error: {e}")

if __name__ == "__main__":
    get_encrypted_seed()