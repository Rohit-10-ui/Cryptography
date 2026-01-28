"""
Playfair Cipher Module
Implements encryption and decryption using Playfair cipher
"""

def generate_matrix(key):
    """Generate 5x5 Playfair matrix from key"""
    key = key.upper().replace("J", "I")
    matrix = []
    used = set()
    for ch in key:
        if ch.isalpha() and ch not in used:
            matrix.append(ch)
            used.add(ch)
    for ch in "ABCDEFGHIKLMNOPQRSTUVWXYZ":
        if ch not in used:
            matrix.append(ch)
            used.add(ch)
    return [matrix[i:i+5] for i in range(0, 25, 5)]

def find_position(matrix, ch):
    """Find position of character in matrix"""
    for i in range(5):
        for j in range(5):
            if matrix[i][j] == ch:
                return i, j
    return None, None

def prepare_text(text):
    """Prepare text for Playfair encryption"""
    text = text.upper().replace("J", "I")
    prepared = ""
    i = 0
    while i < len(text):
        if text[i].isalpha():
            a = text[i]
            if i + 1 < len(text) and text[i + 1].isalpha():
                b = text[i + 1]
                if a == b:
                    prepared += a + "X"
                    i += 1
                else:
                    prepared += a + b
                    i += 2
            else:
                prepared += a + "X"
                i += 1
        else:
            i += 1
    if len(prepared) % 2 != 0:
        prepared += "X"
    return prepared

def encrypt(plaintext, key):
    """Encrypt using Playfair cipher"""
    matrix = generate_matrix(key)
    plaintext = prepare_text(plaintext)
    cipher = ""
    
    for i in range(0, len(plaintext), 2):
        a, b = plaintext[i], plaintext[i+1]
        r1, c1 = find_position(matrix, a)
        r2, c2 = find_position(matrix, b)
        
        if r1 == r2:  # same row
            cipher += matrix[r1][(c1 + 1) % 5]
            cipher += matrix[r2][(c2 + 1) % 5]
        elif c1 == c2:  # same column
            cipher += matrix[(r1 + 1) % 5][c1]
            cipher += matrix[(r2 + 1) % 5][c2]
        else:  # rectangle
            cipher += matrix[r1][c2]
            cipher += matrix[r2][c1]
    
    return cipher, matrix

def decrypt(ciphertext, key):
    """Decrypt using Playfair cipher"""
    matrix = generate_matrix(key)
    plain = ""
    
    for i in range(0, len(ciphertext), 2):
        a, b = ciphertext[i], ciphertext[i+1]
        r1, c1 = find_position(matrix, a)
        r2, c2 = find_position(matrix, b)
        
        if r1 == r2:  # same row
            plain += matrix[r1][(c1 - 1) % 5]
            plain += matrix[r2][(c2 - 1) % 5]
        elif c1 == c2:  # same column
            plain += matrix[(r1 - 1) % 5][c1]
            plain += matrix[(r2 - 1) % 5][c2]
        else:  # rectangle
            plain += matrix[r1][c2]
            plain += matrix[r2][c1]
    
    return plain, matrix

def format_matrix(matrix):
    """Format matrix as string for display"""
    return '\n'.join([' '.join(row) for row in matrix])