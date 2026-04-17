from flask import Flask, render_template, request, jsonify
import os
import math
import number_theory
from Crypto.Cipher import AES
from Crypto.Util.Padding import pad, unpad
import binascii

app = Flask(__name__)

# ==================== VIGENERE CIPHER ====================
def vigenere_encrypt(plaintext, key):
    """Encrypt plaintext using Vigenere cipher"""
    plaintext = plaintext.upper().replace(' ', '')
    key = key.upper().replace(' ', '')
    
    if not key:
        raise ValueError("Key cannot be empty")
    
    result = []
    key_index = 0
    
    for char in plaintext:
        if char.isalpha():
            # Shift character by key
            shift = ord(key[key_index % len(key)]) - ord('A')
            encrypted_char = chr((ord(char) - ord('A') + shift) % 26 + ord('A'))
            result.append(encrypted_char)
            key_index += 1
        else:
            result.append(char)
    
    return ''.join(result)

def vigenere_decrypt(ciphertext, key):
    """Decrypt ciphertext using Vigenere cipher"""
    ciphertext = ciphertext.upper().replace(' ', '')
    key = key.upper().replace(' ', '')
    
    if not key:
        raise ValueError("Key cannot be empty")
    
    result = []
    key_index = 0
    
    for char in ciphertext:
        if char.isalpha():
            # Reverse shift character by key
            shift = ord(key[key_index % len(key)]) - ord('A')
            decrypted_char = chr((ord(char) - ord('A') - shift) % 26 + ord('A'))
            result.append(decrypted_char)
            key_index += 1
        else:
            result.append(char)
    
    return ''.join(result)

# ==================== AFFINE CIPHER ====================
def gcd(a, b):
    """Calculate greatest common divisor"""
    while b:
        a, b = b, a % b
    return a

def mod_inverse(a, m):
    """Calculate modular multiplicative inverse"""
    if gcd(a, m) != 1:
        return None
    
    # Extended Euclidean Algorithm
    for i in range(1, m):
        if (a * i) % m == 1:
            return i
    return None

def affine_encrypt(plaintext, a, b):
    """Encrypt plaintext using Affine cipher"""
    plaintext = plaintext.upper().replace(' ', '')
    
    if gcd(a, 26) != 1:
        raise ValueError("Key 'a' must be coprime with 26")
    
    result = []
    for char in plaintext:
        if char.isalpha():
            # Apply affine transformation: E(x) = (ax + b) mod 26
            x = ord(char) - ord('A')
            encrypted = (a * x + b) % 26
            result.append(chr(encrypted + ord('A')))
        else:
            result.append(char)
    
    return ''.join(result)

def affine_decrypt(ciphertext, a, b):
    """Decrypt ciphertext using Affine cipher"""
    ciphertext = ciphertext.upper().replace(' ', '')
    
    if gcd(a, 26) != 1:
        raise ValueError("Key 'a' must be coprime with 26")
    
    a_inv = mod_inverse(a, 26)
    if a_inv is None:
        raise ValueError("Modular inverse of 'a' does not exist")
    
    result = []
    for char in ciphertext:
        if char.isalpha():
            # Apply inverse affine transformation: D(y) = a^(-1)(y - b) mod 26
            y = ord(char) - ord('A')
            decrypted = (a_inv * (y - b)) % 26
            result.append(chr(decrypted + ord('A')))
        else:
            result.append(char)
    
    return ''.join(result)

# ==================== PLAYFAIR CIPHER ====================
def generate_playfair_matrix(key):
    """Generate 5x5 Playfair matrix from key"""
    key = key.upper().replace('J', 'I').replace(' ', '')
    
    # Create matrix with unique letters from key
    matrix = []
    used = set()
    
    # Add key letters
    for char in key:
        if char.isalpha() and char not in used:
            matrix.append(char)
            used.add(char)
    
    # Add remaining letters (excluding J)
    for char in 'ABCDEFGHIKLMNOPQRSTUVWXYZ':
        if char not in used:
            matrix.append(char)
            used.add(char)
    
    # Convert to 5x5 grid
    grid = []
    for i in range(0, 25, 5):
        grid.append(matrix[i:i+5])
    
    return grid

def format_matrix_display(matrix):
    """Format matrix for display"""
    lines = []
    for row in matrix:
        lines.append('  '.join(row))
    return '\n'.join(lines)

def find_position(matrix, char):
    """Find position of character in matrix"""
    for i, row in enumerate(matrix):
        for j, letter in enumerate(row):
            if letter == char:
                return i, j
    return None, None

def prepare_playfair_text(text):
    """Prepare text for Playfair cipher (handle pairs, I/J substitution, X padding)"""
    text = text.upper().replace('J', 'I').replace(' ', '')
    text = ''.join([c for c in text if c.isalpha()])
    
    # Create pairs and insert X between duplicates
    prepared = []
    i = 0
    while i < len(text):
        char1 = text[i]
        
        if i + 1 < len(text):
            char2 = text[i + 1]
            if char1 == char2:
                prepared.append(char1)
                prepared.append('X')
                i += 1
            else:
                prepared.append(char1)
                prepared.append(char2)
                i += 2
        else:
            prepared.append(char1)
            prepared.append('X')
            i += 1
    
    return ''.join(prepared)

def playfair_encrypt(plaintext, key):
    """Encrypt plaintext using Playfair cipher"""
    matrix = generate_playfair_matrix(key)
    plaintext = prepare_playfair_text(plaintext)
    
    result = []
    for i in range(0, len(plaintext), 2):
        char1 = plaintext[i]
        char2 = plaintext[i + 1] if i + 1 < len(plaintext) else 'X'
        
        row1, col1 = find_position(matrix, char1)
        row2, col2 = find_position(matrix, char2)
        
        if row1 == row2:  # Same row
            result.append(matrix[row1][(col1 + 1) % 5])
            result.append(matrix[row2][(col2 + 1) % 5])
        elif col1 == col2:  # Same column
            result.append(matrix[(row1 + 1) % 5][col1])
            result.append(matrix[(row2 + 1) % 5][col2])
        else:  # Rectangle
            result.append(matrix[row1][col2])
            result.append(matrix[row2][col1])
    
    return ''.join(result)

def playfair_decrypt(ciphertext, key):
    """Decrypt ciphertext using Playfair cipher"""
    matrix = generate_playfair_matrix(key)
    ciphertext = ciphertext.upper().replace('J', 'I').replace(' ', '')
    ciphertext = ''.join([c for c in ciphertext if c.isalpha()])
    
    result = []
    for i in range(0, len(ciphertext), 2):
        char1 = ciphertext[i]
        char2 = ciphertext[i + 1] if i + 1 < len(ciphertext) else 'X'
        
        row1, col1 = find_position(matrix, char1)
        row2, col2 = find_position(matrix, char2)
        
        if row1 == row2:  # Same row
            result.append(matrix[row1][(col1 - 1) % 5])
            result.append(matrix[row2][(col2 - 1) % 5])
        elif col1 == col2:  # Same column
            result.append(matrix[(row1 - 1) % 5][col1])
            result.append(matrix[(row2 - 1) % 5][col2])
        else:  # Rectangle
            result.append(matrix[row1][col2])
            result.append(matrix[row2][col1])
    
    return ''.join(result)

# ==================== DES CIPHER ====================
DES_IP = [58,50,42,34,26,18,10,2,
      60,52,44,36,28,20,12,4,
      62,54,46,38,30,22,14,6,
      64,56,48,40,32,24,16,8,
      57,49,41,33,25,17,9,1,
      59,51,43,35,27,19,11,3,
      61,53,45,37,29,21,13,5,
      63,55,47,39,31,23,15,7]

DES_FP = [40,8,48,16,56,24,64,32,
      39,7,47,15,55,23,63,31,
      38,6,46,14,54,22,62,30,
      37,5,45,13,53,21,61,29,
      36,4,44,12,52,20,60,28,
      35,3,43,11,51,19,59,27,
      34,2,42,10,50,18,58,26,
      33,1,41,9,49,17,57,25]

DES_E = [32,1,2,3,4,5,4,5,
     6,7,8,9,8,9,10,11,
     12,13,12,13,14,15,16,17,
     16,17,18,19,20,21,20,21,
     22,23,24,25,24,25,26,27,
     28,29,28,29,30,31,32,1]

DES_P = [16,7,20,21,
     29,12,28,17,
     1,15,23,26,
     5,18,31,10,
     2,8,24,14,
     32,27,3,9,
     19,13,30,6,
     22,11,4,25]

DES_PC1 = [57,49,41,33,25,17,9,
       1,58,50,42,34,26,18,
       10,2,59,51,43,35,27,
       19,11,3,60,52,44,36,
       63,55,47,39,31,23,15,
       7,62,54,46,38,30,22,
       14,6,61,53,45,37,29,
       21,13,5,28,20,12,4]

DES_PC2 = [14,17,11,24,1,5,
       3,28,15,6,21,10,
       23,19,12,4,26,8,
       16,7,27,20,13,2,
       41,52,31,37,47,55,
       30,40,51,45,33,48,
       44,49,39,56,34,53,
       46,42,50,36,29,32]

DES_SHIFT = [1,1,2,2,2,2,2,2,1,2,2,2,2,2,2,1]

DES_S_BOX = [
# S1
[[14,4,13,1,2,15,11,8,3,10,6,12,5,9,0,7],
 [0,15,7,4,14,2,13,1,10,6,12,11,9,5,3,8],
 [4,1,14,8,13,6,2,11,15,12,9,7,3,10,5,0],
 [15,12,8,2,4,9,1,7,5,11,3,14,10,0,6,13]],
# S2
[[15,1,8,14,6,11,3,4,9,7,2,13,12,0,5,10],
 [3,13,4,7,15,2,8,14,12,0,1,10,6,9,11,5],
 [0,14,7,11,10,4,13,1,5,8,12,6,9,3,2,15],
 [13,8,10,1,3,15,4,2,11,6,7,12,0,5,14,9]],
# S3
[[10,0,9,14,6,3,15,5,1,13,12,7,11,4,2,8],
 [13,7,0,9,3,4,6,10,2,8,5,14,12,11,15,1],
 [13,6,4,9,8,15,3,0,11,1,2,12,5,10,14,7],
 [1,10,13,0,6,9,8,7,4,15,14,3,11,5,2,12]],
# S4
[[7,13,14,3,0,6,9,10,1,2,8,5,11,12,4,15],
 [13,8,11,5,6,15,0,3,4,7,2,12,1,10,14,9],
 [10,6,9,0,12,11,7,13,15,1,3,14,5,2,8,4],
 [3,15,0,6,10,1,13,8,9,4,5,11,12,7,2,14]],
# S5
[[2,12,4,1,7,10,11,6,8,5,3,15,13,0,14,9],
 [14,11,2,12,4,7,13,1,5,0,15,10,3,9,8,6],
 [4,2,1,11,10,13,7,8,15,9,12,5,6,3,0,14],
 [11,8,12,7,1,14,2,13,6,15,0,9,10,4,5,3]],
# S6
[[12,1,10,15,9,2,6,8,0,13,3,4,14,7,5,11],
 [10,15,4,2,7,12,9,5,6,1,13,14,0,11,3,8],
 [9,14,15,5,2,8,12,3,7,0,4,10,1,13,11,6],
 [4,3,2,12,9,5,15,10,11,14,1,7,6,0,8,13]],
# S7
[[4,11,2,14,15,0,8,13,3,12,9,7,5,10,6,1],
 [13,0,11,7,4,9,1,10,14,3,5,12,2,15,8,6],
 [1,4,11,13,12,3,7,14,10,15,6,8,0,5,9,2],
 [6,11,13,8,1,4,10,7,9,5,0,15,14,2,3,12]],
# S8
[[13,2,8,4,6,15,11,1,10,9,3,14,5,0,12,7],
 [1,15,13,8,10,3,7,4,12,5,6,11,0,14,9,2],
 [7,11,4,1,9,12,14,2,0,6,10,13,15,3,5,8],
 [2,1,14,7,4,10,8,13,15,12,9,0,3,5,6,11]]
]

def des_text_to_bin(text):
    return ''.join(format(ord(c), '08b') for c in text)

def des_bin_to_text(binary):
    return ''.join(chr(int(binary[i:i+8],2)) for i in range(0,64,8))

def des_permute(block, table):
    return ''.join(block[i-1] for i in table)

def des_shift_left(bits, n):
    return bits[n:] + bits[:n]

def des_xor(a, b):
    return ''.join('0' if i == j else '1' for i,j in zip(a,b))

def des_generate_keys(key_bin, logs=None):
    key_bin = des_permute(key_bin, DES_PC1)
    left, right = key_bin[:28], key_bin[28:]
    keys = []
    if logs is not None: logs.append("\n========= KEY GENERATION =========")
    for i in range(16):
        left = des_shift_left(left, DES_SHIFT[i])
        right = des_shift_left(right, DES_SHIFT[i])
        round_key = des_permute(left + right, DES_PC2)
        keys.append(round_key)
        if logs is not None: logs.append(f"Round {i+1} Key: {round_key}")
    return keys

def des_sbox_substitution(bits48, logs=None):
    result = ""
    for i in range(8):
        block = bits48[i*6:(i+1)*6]
        row = int(block[0]+block[5],2)
        col = int(block[1:5],2)
        val = DES_S_BOX[i][row][col]
        binary = format(val,'04b')
        if logs is not None: logs.append(f"S{i+1}: {block} -> {binary}")
        result += binary
    return result

def des_core(block_bin, keys, mode, logs=None):
    block_bin = des_permute(block_bin, DES_IP)
    left, right = block_bin[:32], block_bin[32:]
    if mode == "ENCRYPT" and logs is not None:
        logs.append("\n========= DES ENCRYPTION =========")
    for i in range(16):
        expanded = des_permute(right, DES_E)
        xored = des_xor(expanded, keys[i])
        sbox_out = des_sbox_substitution(xored, logs)
        pbox_out = des_permute(sbox_out, DES_P)
        new_right = des_xor(left, pbox_out)
        if mode == "ENCRYPT" and (i == 0 or i == 15) and logs is not None:
            logs.append(f"\n---- ROUND {i+1} ----")
            logs.append(f"Left : {left}")
            logs.append(f"Right: {right}")
            logs.append(f"Expanded: {expanded}")
            logs.append(f"After XOR: {xored}")
            logs.append(f"After S-Box: {sbox_out}")
            logs.append(f"After P-Box: {pbox_out}")
            logs.append(f"New Right: {new_right}")
        left = right
        right = new_right
    combined = right + left
    final_block = des_permute(combined, DES_FP)
    return final_block

def des_encrypt(plaintext, key):
    logs = []
    if len(plaintext) != 8 or len(key) != 8:
        raise ValueError("Plaintext and Key must be exactly 8 characters.")
    plain_bin = des_text_to_bin(plaintext)
    key_bin = des_text_to_bin(key)
    keys = des_generate_keys(key_bin, logs)
    cipher_bin = des_core(plain_bin, keys, "ENCRYPT", logs)
    cipher_text = des_bin_to_text(cipher_bin)
    return cipher_text, logs

def des_decrypt(ciphertext, key):
    logs = []
    if len(ciphertext) != 8 or len(key) != 8:
        raise ValueError("Ciphertext and Key must be exactly 8 characters.")
    cipher_bin = des_text_to_bin(ciphertext)
    key_bin = des_text_to_bin(key)
    keys = des_generate_keys(key_bin, logs)
    keys = keys[::-1]   # reverse order
    plain_bin = des_core(cipher_bin, keys, "DECRYPT", logs)
    return des_bin_to_text(plain_bin), logs

# ==================== AES CIPHER ====================
def aes_print_state(label, data, logs=None):
    if logs is not None:
        logs.append(f"{label}: {binascii.hexlify(data).decode()}")

def aes_encrypt(plaintext, key):
    """Encrypt plaintext using AES (ECB mode)"""
    logs = []
    logs.append("\n========= AES ENCRYPTION =========")
    # Ensure 16-byte key
    key_bytes = key.encode('utf-8')[:16].ljust(16, b'\0')
    plaintext_bytes = plaintext.encode('utf-8')
    
    # Pad plaintext to block size (16 bytes)
    padded_text = pad(plaintext_bytes, 16)
    
    cipher = AES.new(key_bytes, AES.MODE_ECB)
    
    logs.append("\n---- ROUND 1 (Conceptual State) ----")
    aes_print_state("Input Block", padded_text[:16], logs)
    
    ciphertext = cipher.encrypt(padded_text)
    
    logs.append("\n---- ROUND 10 (Final State) ----")
    aes_print_state("Cipher Block", ciphertext[:16], logs)
    logs.append(f"\nCipher Text (hex): {binascii.hexlify(ciphertext).decode('utf-8')}")
    
    # Return hex string
    return binascii.hexlify(ciphertext).decode('utf-8'), logs

def aes_decrypt(ciphertext_hex, key):
    """Decrypt ciphertext (hex string) using AES (ECB mode)"""
    logs = []
    logs.append("\n========= AES DECRYPTION =========")
    # Ensure 16-byte key
    key_bytes = key.encode('utf-8')[:16].ljust(16, b'\0')
    
    # Convert hex string back to bytes
    ciphertext = binascii.unhexlify(ciphertext_hex)
    
    logs.append("\n---- ROUND 1 (Input Ciphertext) ----")
    aes_print_state("Cipher Block", ciphertext[:16], logs)
    
    cipher = AES.new(key_bytes, AES.MODE_ECB)
    decrypted = cipher.decrypt(ciphertext)
    
    logs.append("\n---- ROUND 10 (Decrypted Block) ----")
    aes_print_state("Decrypted Block", decrypted[:16], logs)
    
    # Unpad and decode
    unpadded = unpad(decrypted, 16)
    logs.append(f"\nDecrypted Text: {unpadded.decode('utf-8')}")
    return unpadded.decode('utf-8'), logs

# ==================== RSA CIPHER ====================
def rsa_generate_keys(p, q):
    """Generate RSA keys from primes p and q"""
    # Check primality using number_theory module
    if not number_theory.rabin_miller(p, k=10) or not number_theory.rabin_miller(q, k=10):
        raise ValueError("Both numbers must be prime")
    
    n = p * q
    phi = (p - 1) * (q - 1)
    
    # Choose e (1 < e < phi) such that gcd(e, phi) = 1
    e = 2
    while e < phi:
        if gcd(e, phi) == 1:
            break
        e += 1
    
    d = mod_inverse(e, phi)
    if d is None:
        raise ValueError("Could not generate private key (d)")
        
    return {'e': e, 'n': n}, {'d': d, 'n': n}

# ==================== FLASK ROUTES ====================
@app.route('/')
def index():
    """Serve the main page"""
    return render_template('index.html')

@app.route('/api/vigenere', methods=['POST'])
def api_vigenere():
    """Handle Vigenere cipher requests"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        key = data.get('key', '')
        operation = data.get('operation', 'encrypt')
        
        if not message or not key:
            return jsonify({'success': False, 'error': 'Message and key are required'})
        
        if operation == 'encrypt':
            result = vigenere_encrypt(message, key)
            return jsonify({'success': True, 'result': result, 'operation': 'Encrypted'})
        else:
            result = vigenere_decrypt(message, key)
            return jsonify({'success': True, 'result': result, 'operation': 'Decrypted'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/affine', methods=['POST'])
def api_affine():
    """Handle Affine cipher requests"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        a = data.get('a')
        b = data.get('b')
        operation = data.get('operation', 'encrypt')
        
        if not message or a is None or b is None:
            return jsonify({'success': False, 'error': 'Message and keys (a, b) are required'})
        
        a = int(a)
        b = int(b)
        
        if operation == 'encrypt':
            result = affine_encrypt(message, a, b)
            return jsonify({'success': True, 'result': result, 'operation': 'Encrypted'})
        else:
            result = affine_decrypt(message, a, b)
            return jsonify({'success': True, 'result': result, 'operation': 'Decrypted'})
    
    except ValueError as e:
        return jsonify({'success': False, 'error': str(e)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/playfair', methods=['POST'])
def api_playfair():
    """Handle Playfair cipher requests"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        key = data.get('key', '')
        operation = data.get('operation', 'encrypt')
        
        if not message or not key:
            return jsonify({'success': False, 'error': 'Message and key are required'})
        
        matrix = generate_playfair_matrix(key)
        matrix_display = format_matrix_display(matrix)
        
        if operation == 'encrypt':
            result = playfair_encrypt(message, key)
            return jsonify({
                'success': True, 
                'result': result, 
                'matrix': matrix_display,
                'operation': 'Encrypted'
            })
        else:
            result = playfair_decrypt(message, key)
            return jsonify({
                'success': True, 
                'result': result, 
                'matrix': matrix_display,
                'operation': 'Decrypted'
            })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/des', methods=['POST'])
def api_des():
    """Handle DES cipher requests"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        key = data.get('key', '')
        operation = data.get('operation', 'encrypt')
        
        if not message or not key:
            return jsonify({'success': False, 'error': 'Message and key are required'})
        
        if operation == 'encrypt':
            result, logs = des_encrypt(message, key)
            return jsonify({'success': True, 'result': result, 'logs': logs, 'operation': 'Encrypted'})
        else:
            result, logs = des_decrypt(message, key)
            return jsonify({'success': True, 'result': result, 'logs': logs, 'operation': 'Decrypted'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/aes', methods=['POST'])
def api_aes():
    """Handle AES cipher requests"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        key = data.get('key', '')
        operation = data.get('operation', 'encrypt')
        
        if not message or not key:
            return jsonify({'success': False, 'error': 'Message and key are required'})
        
        if operation == 'encrypt':
            result, logs = aes_encrypt(message, key)
            return jsonify({'success': True, 'result': result, 'logs': logs, 'operation': 'Encrypted'})
        else:
            result, logs = aes_decrypt(message, key)
            return jsonify({'success': True, 'result': result, 'logs': logs, 'operation': 'Decrypted'})
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/rsa', methods=['POST'])
def api_rsa():
    """Handle RSA cipher requests"""
    try:
        data = request.get_json()
        operation = data.get('operation')
        
        if operation == 'generate':
            p = data.get('p')
            q = data.get('q')
            if not p or not q:
                return jsonify({'success': False, 'error': 'Primes p and q are required'})
            
            pub, priv = rsa_generate_keys(int(p), int(q))
            return jsonify({
                'success': True, 
                'public_key': pub, 
                'private_key': priv,
                'operation': 'Generated Keys'
            })
            
        # Encrypt/Decrypt
        message = data.get('message')
        key_part1 = data.get('key_part1') # e or d
        key_part2 = data.get('key_part2') # n
        
        if message is None or key_part1 is None or key_part2 is None:
             return jsonify({'success': False, 'error': 'Message, Key Exponent, and Modulus n are required'})
        
        # RSA operates on integers
        msg_int = int(message)
        exp = int(key_part1)
        mod = int(key_part2)
        
        if msg_int >= mod:
            return jsonify({'success': False, 'error': f'Message ({msg_int}) must be smaller than modulus n ({mod})'})

        result = pow(msg_int, exp, mod)
        
        return jsonify({
            'success': True, 
            'result': str(result), 
            'operation': 'Encrypted' if operation == 'encrypt' else 'Decrypted'
        })

    except ValueError as e:
        return jsonify({'success': False, 'error': 'Invalid input: ' + str(e)})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/diffie-hellman', methods=['POST'])
def api_diffie_hellman():
    """Handle Diffie-Hellman Key Exchange requests"""
    try:
        data = request.get_json()
        p = data.get('p')
        g = data.get('g')
        a = data.get('a')
        b = data.get('b')
        
        if not all([p, g, a, b]):
            return jsonify({'success': False, 'error': 'All fields (p, g, a, b) are required'})
            
        p, g, a, b = int(p), int(g), int(a), int(b)
        
        # Check if p is prime
        if not number_theory.rabin_miller(p, k=10):
            return jsonify({'success': False, 'error': f'The number p ({p}) must be a prime number.'})
        
        # Calculate Public Keys
        # A = g^a mod p
        A = pow(g, a, p)
        # B = g^b mod p
        B = pow(g, b, p)
        
        # Calculate Shared Secrets
        # Alice computes secret = B^a mod p
        secret_a = pow(B, a, p)
        # Bob computes secret = A^b mod p
        secret_b = pow(A, b, p)
        
        return jsonify({
            'success': True,
            'p': p, 'g': g, 'a': a, 'b': b,
            'A': A, 'B': B,
            'secret_a': secret_a,
            'secret_b': secret_b
        })
        
    except ValueError:
        return jsonify({'success': False, 'error': 'Invalid input: numbers required'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# ==================== NUMBER THEORY API ====================

@app.route('/api/primality-test', methods=['POST'])
def api_primality_test():
    """Rabin-Miller primality test"""
    try:
        data = request.get_json()
        number = data.get('number', '')
        
        if not number:
            return jsonify({'success': False, 'error': 'Number is required'})
        
        num = int(number)
        if num < 0:
            return jsonify({'success': False, 'error': 'Please enter a non-negative number'})
        
        is_prime = number_theory.rabin_miller(num, k=10)
        
        return jsonify({
            'success': True,
            'number': num,
            'is_prime': is_prime,
            'result': f"{num} is {'PRIME' if is_prime else 'COMPOSITE'}"
        })
    
    except ValueError:
        return jsonify({'success': False, 'error': 'Invalid number format'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/primitive-root', methods=['POST'])
def api_primitive_root():
    """Find primitive root modulo n"""
    try:
        data = request.get_json()
        number = data.get('number', '')
        
        if not number:
            return jsonify({'success': False, 'error': 'Number is required'})
        
        num = int(number)
        if num < 2:
            return jsonify({'success': False, 'error': 'Number must be greater than 1'})
        
        # Check if prime first
        is_prime = number_theory.rabin_miller(num, k=10)
        if not is_prime:
            return jsonify({
                'success': False,
                'error': f'{num} is not prime. Primitive roots are typically found for prime numbers.'
            })
        
        proot = number_theory.find_primitive_root(num)
        
        if proot is None:
            return jsonify({
                'success': False,
                'error': f'No primitive root found for {num}'
            })
        
        return jsonify({
            'success': True,
            'number': num,
            'primitive_root': proot,
            'result': f'Primitive root of {num} is {proot}'
        })
    
    except ValueError:
        return jsonify({'success': False, 'error': 'Invalid number format'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

@app.route('/api/euclid', methods=['POST'])
def api_euclid():
    """Euclid's algorithm for GCD"""
    try:
        data = request.get_json()
        num1 = data.get('number1', '')
        num2 = data.get('number2', '')
        
        if not num1 or not num2:
            return jsonify({'success': False, 'error': 'Both numbers are required'})
        
        a, b = int(num1), int(num2)
        if a < 0 or b < 0:
            return jsonify({'success': False, 'error': 'Numbers must be non-negative'})
        
        gcd, x, y = number_theory.gcd_euclid(a, b)
        
        return jsonify({
            'success': True,
            'number1': a,
            'number2': b,
            'gcd': gcd,
            'x': x,
            'y': y,
            'result': f'gcd({a}, {b}) = {gcd}',
            'equation': f'{gcd} = {a}×({x}) + {b}×({y})'
        })
    
    except ValueError:
        return jsonify({'success': False, 'error': 'Invalid number format'})
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# ==================== SHA256 HASHING ====================
import hashlib
import struct

def sha256_hash(message):
    """Calculate SHA256 hash of message using Python's hashlib"""
    return hashlib.sha256(message.encode('utf-8')).hexdigest()

@app.route('/api/sha256', methods=['POST'])
def api_sha256():
    """SHA256 hashing endpoint"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        
        if not message:
            return jsonify({'success': False, 'error': 'Message cannot be empty'})
        
        hash_value = sha256_hash(message)
        
        return jsonify({
            'success': True,
            'message': message,
            'hash': hash_value,
            'hash_length': len(hash_value)
        })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})

# ==================== CMAC (CIPHER-BASED MAC) ====================

def xor_bytes(a, b):
    """XOR two byte strings"""
    return bytes(x ^ y for x, y in zip(a, b))

def left_shift(block):
    """Left shift a 128-bit block by 1"""
    shifted = int.from_bytes(block, byteorder='big') << 1
    shifted &= (1 << 128) - 1
    return shifted.to_bytes(16, byteorder='big')

def generate_subkeys_cmac(key, steps=None):
    """Generate CMAC subkeys K1 and K2 from the AES key"""
    cipher = AES.new(key, AES.MODE_ECB)
    zero_block = bytes(16)
    
    # L = AES(K, 0^128)
    L = cipher.encrypt(zero_block)
    if steps is not None:
        steps.append(f"Step 1: Generate L = AES(K, 0^128)")
        steps.append(f"  L = {binascii.hexlify(L).decode()}")
    
    # Constant for CMAC
    Rb = 0x87
    
    # K1 generation
    if (L[0] & 0x80) == 0:
        K1 = left_shift(L)
        if steps is not None:
            steps.append(f"\nStep 2: Generate K1 (MSB of L = 0)")
            steps.append(f"  K1 = LeftShift(L) = {binascii.hexlify(K1).decode()}")
    else:
        K1 = xor_bytes(left_shift(L), Rb.to_bytes(16, 'big'))
        if steps is not None:
            steps.append(f"\nStep 2: Generate K1 (MSB of L = 1)")
            steps.append(f"  K1 = LeftShift(L) XOR Rb = {binascii.hexlify(K1).decode()}")
    
    # K2 generation
    if (K1[0] & 0x80) == 0:
        K2 = left_shift(K1)
        if steps is not None:
            steps.append(f"\nStep 3: Generate K2 (MSB of K1 = 0)")
            steps.append(f"  K2 = LeftShift(K1) = {binascii.hexlify(K2).decode()}")
    else:
        K2 = xor_bytes(left_shift(K1), Rb.to_bytes(16, 'big'))
        if steps is not None:
            steps.append(f"\nStep 3: Generate K2 (MSB of K1 = 1)")
            steps.append(f"  K2 = LeftShift(K1) XOR Rb = {binascii.hexlify(K2).decode()}")
    
    return K1, K2

def cmac_generate(key, message, steps=None):
    """Generate CMAC tag for message using key with intermediate steps"""
    cipher = AES.new(key, AES.MODE_ECB)
    block_size = 16
    
    if steps is not None:
        steps.append("=" * 60)
        steps.append("CMAC GENERATION PROCESS")
        steps.append("=" * 60)
    
    K1, K2 = generate_subkeys_cmac(key, steps)
    
    # Process message into blocks
    if len(message) == 0:
        n = 1
        flag = False
    else:
        n = (len(message) + block_size - 1) // block_size
        flag = (len(message) % block_size == 0)
    
    if steps is not None:
        steps.append(f"\nStep 4: Message Blocking")
        steps.append(f"  Message Length: {len(message)} bytes")
        steps.append(f"  Number of Blocks: {n}")
        steps.append(f"  Last Block Complete: {flag}")
    
    blocks = [message[i*block_size:(i+1)*block_size] for i in range(n)]
    
    if steps is not None:
        for i, block in enumerate(blocks):
            steps.append(f"  Block {i+1}: {binascii.hexlify(block).decode()}")
    
    # Process last block
    if flag:
        last_block = xor_bytes(blocks[-1], K1)
        if steps is not None:
            steps.append(f"\nStep 5: Last Block Processing (Complete)")
            steps.append(f"  Last Block XOR K1 = {binascii.hexlify(last_block).decode()}")
    else:
        # Pad incomplete block with 10^*
        padded = blocks[-1] + b'\x80' + b'\x00' * (block_size - len(blocks[-1]) - 1)
        last_block = xor_bytes(padded, K2)
        if steps is not None:
            steps.append(f"\nStep 5: Last Block Processing (Incomplete)")
            steps.append(f"  Padded Block: {binascii.hexlify(padded).decode()}")
            steps.append(f"  Padded XOR K2 = {binascii.hexlify(last_block).decode()}")
    
    # CMAC computation
    X = bytes(block_size)
    if steps is not None:
        steps.append(f"\nStep 6: CMAC Computation")
        steps.append(f"  Initial X: {binascii.hexlify(X).decode()}")
    
    for i in range(n - 1):
        Y = xor_bytes(X, blocks[i])
        X = cipher.encrypt(Y)
        if steps is not None and n > 1:
            steps.append(f"  Block {i+1}: X XOR Block = {binascii.hexlify(Y).decode()}")
            steps.append(f"           AES Output  = {binascii.hexlify(X).decode()}")
    
    # Final block
    Y = xor_bytes(X, last_block)
    T = cipher.encrypt(Y)
    if steps is not None:
        steps.append(f"\nStep 7: Final Block Processing")
        steps.append(f"  X XOR Last Block = {binascii.hexlify(Y).decode()}")
        steps.append(f"  CMAC Tag         = {binascii.hexlify(T).decode()}")
    
    return T

@app.route('/api/cmac', methods=['POST'])
def api_cmac():
    """Handle CMAC generation and verification"""
    try:
        data = request.get_json()
        message = data.get('message', '')
        key = data.get('key', '')
        operation = data.get('operation', 'generate')
        
        if not message or not key:
            return jsonify({'success': False, 'error': 'Message and key are required'})
        
        # Encode message and key to bytes
        message_bytes = message.encode('utf-8')
        key_bytes = key.encode('utf-8')
        
        # Pad or truncate key to 16 bytes (128-bit)
        if len(key_bytes) < 16:
            key_bytes = key_bytes.ljust(16, b'\x00')
        else:
            key_bytes = key_bytes[:16]
        
        if operation == 'generate':
            # Generate CMAC with intermediate steps
            steps = []
            steps.append(f"Input Message: {message}")
            steps.append(f"Input Key: {key}")
            steps.append(f"Message (hex): {binascii.hexlify(message_bytes).decode()}")
            steps.append(f"Key (hex): {binascii.hexlify(key_bytes).decode()}")
            steps.append("")
            
            cmac_tag = cmac_generate(key_bytes, message_bytes, steps)
            cmac_hex = binascii.hexlify(cmac_tag).decode('utf-8')
            
            return jsonify({
                'success': True,
                'cmac': cmac_hex,
                'steps': steps,
                'result': '\n'.join(steps)
            })
        else:
            # For verification, generate and show intermediate steps
            steps = []
            steps.append(f"Input Message: {message}")
            steps.append(f"Input Key: {key}")
            steps.append(f"Message (hex): {binascii.hexlify(message_bytes).decode()}")
            steps.append(f"Key (hex): {binascii.hexlify(key_bytes).decode()}")
            steps.append("")
            
            cmac_tag = cmac_generate(key_bytes, message_bytes, steps)
            cmac_hex = binascii.hexlify(cmac_tag).decode('utf-8')
            
            return jsonify({
                'success': True,
                'steps': steps,
                'result': '\n'.join(steps)
            })
    
    except Exception as e:
        return jsonify({'success': False, 'error': str(e)})


if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
