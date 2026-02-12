from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import binascii

# ---------- Helper Function ----------
def print_state(label, data):
    print(f"{label}: {binascii.hexlify(data).decode()}")
    
# ---------- Encryption ----------
def encrypt_aes(plaintext, key):
    print("\n========= AES ENCRYPTION =========")
    # Ensure 16-byte key
    key = key.encode()[:16].ljust(16, b'\0')
    plaintext = plaintext.encode()
    # Pad plaintext to 16 bytes
    padded_text = pad(plaintext, 16)
    cipher = AES.new(key, AES.MODE_ECB)
    print("\n---- ROUND 1 (Conceptual State) ----")
    print_state("Input Block", padded_text[:16])
    ciphertext = cipher.encrypt(padded_text)
    print("\n---- ROUND 10 (Final State) ----")
    print_state("Cipher Block", ciphertext[:16])
    print("\nCipher Text (hex):", binascii.hexlify(ciphertext).decode())
    return ciphertext, key

# ---------- Decryption ----------
def decrypt_aes(ciphertext, key):
    cipher = AES.new(key, AES.MODE_ECB)
    decrypted = cipher.decrypt(ciphertext)
    unpadded = unpad(decrypted, 16)
    print("\nDecrypted Text:", unpadded.decode())
    return unpadded

# ---------- Main ----------
plaintext = input("Enter Plaintext (any length): ")
key = input("Enter Key (max 16 characters): ")
ciphertext, key_used = encrypt_aes(plaintext, key)
print("\n==============================")
decrypt_aes(ciphertext, key_used)