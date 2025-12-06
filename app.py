from flask import Flask, request, jsonify, render_template
import bcrypt, hashlib, os
from argon2 import PasswordHasher
import hashlib

app = Flask(__name__)
ph = PasswordHasher()

@app.route("/")
def home():
    return render_template("index.html")

@app.route("/generate", methods=["POST"])
def generate():
    data = request.get_json()
    password = data["password"].encode()

    # 1. bcrypt
    bcrypt_hash = bcrypt.hashpw(password, bcrypt.gensalt()).decode()

    # 2. Argon2id
    argon_hash = ph.hash(password.decode())

    # 3. PBKDF2-HMAC-SHA256
    salt_pbkdf2 = os.urandom(16)
    pbkdf2_hash = hashlib.pbkdf2_hmac("sha256", password, salt_pbkdf2, 100000).hex()

    # 4. scrypt
    salt_scrypt = os.urandom(16)
    scrypt_hash = hashlib.scrypt(password, salt=salt_scrypt, n=16384, r=8, p=1).hex()

    # 5. SHA-256
    sha256_hash = hashlib.sha256(password).hexdigest()

    return jsonify({
        "bcrypt": {
            "hash": bcrypt_hash
        },
        "argon2id": {
            "hash": argon_hash
        },
        "pbkdf2_sha256": {
            "hash": pbkdf2_hash,
            "salt": salt_pbkdf2.hex()
        },
        "scrypt": {
            "hash": scrypt_hash,
            "salt": salt_scrypt.hex()
        },
        "sha256": {
            "hash": sha256_hash
        }
    })

if __name__ == "__main__":
    app.run(debug=True)
