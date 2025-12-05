# Secure PKI-Based 2FA Microservice

A production-ready, containerized microservice that implements Two-Factor Authentication (2FA) using Time-based One-Time Passwords (TOTP). The system features enterprise-grade security practices including RSA 4096-bit asymmetric encryption, digital signatures, and persistent storage management.

## 🚀 Features

* **Asymmetric Cryptography:** Uses RSA 4096-bit keys for secure seed transmission.
* **Secure Decryption:** Implements RSA-OAEP with SHA-256 and MGF1 padding.
* **Standardized TOTP:** Generates 6-digit codes (RFC 6238) compatible with standard authenticator apps.
* **Dockerized Architecture:** Multi-stage Docker build with optimized image size.
* **Background Logging:** Integrated Cron job for auditing 2FA codes every minute.
* **Data Persistence:** Docker volumes ensure user seeds survive container restarts.
* **Time Synchronization:** Enforces UTC timezone for accurate TOTP generation.

---

## 🛠️ Technology Stack

* **Language:** Python 3.11
* **Framework:** FastAPI (High-performance web framework)
* **Server:** Uvicorn (ASGI server)
* **Containerization:** Docker & Docker Compose
* **Cryptography:** `cryptography` (OpenSSL wrapper) & `pyotp`
* **OS:** Debian-based Linux (via Python Slim image)

---

## 📋 Prerequisites

* Docker and Docker Compose installed.
* Git installed.
* **Security Keys:**
    * `student_private.pem`: Your generated 4096-bit private key.
    * `instructor_public.pem`: The instructor's public key (for proof verification).
* **Encrypted Seed:** The `encrypted_seed.txt` file obtained from the instructor API.

---

## ⚙️ Setup & Installation

1.  **Clone the Repository**
    ```bash
    git clone https://github.com/Shanmuka-p/docker-23P31A05H8.git
    cd docker-23P31A05H8
    ```

2.  **Verify Key Files**
    Ensure the following files are present in the project root:
    * `student_private.pem`
    * `instructor_public.pem`
    * `encrypted_seed.txt`

3.  **Build and Run with Docker**
    ```bash
    docker-compose up --build -d
    ```

4.  **Verify Container Status**
    ```bash
    docker ps
    # Status should be 'Up' for docker-23P31A05H8
    ```

---

## 🔌 API Documentation

The service exposes the following REST endpoints on **Port 8080**.

### 1. Decrypt Seed
Decrypts the encrypted seed and stores it persistently.
* **Endpoint:** `POST /decrypt-seed`
* **Example Request:**
    ```bash
    curl -X POST http://localhost:8080/decrypt-seed \
      -H "Content-Type: application/json" \
      -d "{\"encrypted_seed\": \"$(cat encrypted_seed.txt)\"}"
    ```
* **Success Response:** `{"status": "ok"}`

### 2. Generate 2FA Code
Generates a current TOTP code based on the stored seed.
* **Endpoint:** `GET /generate-2fa`
* **Example Request:**
    ```bash
    curl http://localhost:8080/generate-2fa
    ```
* **Success Response:** `{"code": "123456", "valid_for": 28}`

### 3. Verify 2FA Code
Verifies a user-provided code with a tolerance of ±30 seconds (1 period).
* **Endpoint:** `POST /verify-2fa`
* **Example Request:**
    ```bash
    curl -X POST http://localhost:8080/verify-2fa \
      -H "Content-Type: application/json" \
      -d '{"code": "123456"}'
    ```
* **Success Response:** `{"valid": true}`

---

## 🧪 Testing & Verification

### 1. Cron Job Verification
The system runs a cron job every minute to log the current 2FA code. To verify this works (wait at least 1-2 minutes after starting):

```bash
# Note: Use double slash // for Git Bash on Windows
docker exec docker-23P31A05H8 cat //cron/last_code.txt
