import struct

# Initial hash values (first 32 bits of fractional parts of square roots of primes)
H = [
    0x6a09e667, 0xbb67ae85, 0x3c6ef372, 0xa54ff53a,
    0x510e527f, 0x9b05688c, 0x1f83d9ab, 0x5be0cd19
]

# Round constants
K = [
    0x428a2f98, 0x71374491, 0xb5c0fbcf, 0xe9b5dba5,
    # (Add all 64 constants in real implementation)
]

def right_rotate(x, n):
    return (x >> n) | (x << (32 - n)) & 0xffffffff

def sha256_manual(message):
    message = bytearray(message, 'utf-8')
    original_length = len(message) * 8

    # Padding
    message.append(0x80)
    while (len(message) * 8) % 512 != 448:
        message.append(0)

    message += struct.pack('>Q', original_length)

    # Process chunks
    for i in range(0, len(message), 64):
        chunk = message[i:i+64]
        w = list(struct.unpack('>16L', chunk)) + [0]*48

        for j in range(16, 64):
            s0 = right_rotate(w[j-15], 7) ^ right_rotate(w[j-15], 18) ^ (w[j-15] >> 3)
            s1 = right_rotate(w[j-2], 17) ^ right_rotate(w[j-2], 19) ^ (w[j-2] >> 10)
            w[j] = (w[j-16] + s0 + w[j-7] + s1) & 0xffffffff

        a, b, c, d, e, f, g, h = H

        for j in range(16):  # simplified loop (real = 64 rounds)
            S1 = right_rotate(e, 6) ^ right_rotate(e, 11) ^ right_rotate(e, 25)
            ch = (e & f) ^ (~e & g)
            temp1 = (h + S1 + ch + K[j % len(K)] + w[j]) & 0xffffffff
            S0 = right_rotate(a, 2) ^ right_rotate(a, 13) ^ right_rotate(a, 22)
            maj = (a & b) ^ (a & c) ^ (b & c)
            temp2 = (S0 + maj) & 0xffffffff

            h = g
            g = f
            f = e
            e = (d + temp1) & 0xffffffff
            d = c
            c = b
            b = a
            a = (temp1 + temp2) & 0xffffffff

    return ''.join(format(x, '08x') for x in H)


# Test
msg=input("Enter a message to hash: ")
print(sha256_manual(msg))