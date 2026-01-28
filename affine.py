"""
Affine Cipher Module
Implements encryption and decryption using Affine cipher
"""

def mod_inverse(a, m):
    """Find modular inverse of a under modulo m"""
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    return None

def encrypt(text, a, b):
    """Encrypt text using Affine cipher"""
    result = ""
    for ch in text:
        if ch.isupper():
            p = ord(ch) - ord('A')
            c = (a * p + b) % 26
            result += chr(c + ord('A'))
        elif ch.islower():
            p = ord(ch) - ord('a')
            c = (a * p + b) % 26
            result += chr(c + ord('a'))
        else:
            result += ch
    return result

def decrypt(text, a, b):
    """Decrypt text using Affine cipher"""
    result = ""
    a_inv = mod_inverse(a, 26)
    if a_inv is None:
        return "Invalid value of 'a'"
    for ch in text:
        if ch.isupper():
            c = ord(ch) - ord('A')
            p = (a_inv * (c - b)) % 26
            result += chr(p + ord('A'))
        elif ch.islower():
            c = ord(ch) - ord('a')
            p = (a_inv * (c - b)) % 26
            result += chr(p + ord('a'))
        else:
            result += ch
    return result

def validate_key_a(a):
    """Validate that key 'a' is coprime with 26"""
    return mod_inverse(a, 26) is not None