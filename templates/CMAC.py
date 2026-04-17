from Crypto.Cipher import AES
from Crypto.Util.Padding import pad
import binascii

# -------- HELPER FUNCTIONS --------
def xor_bytes(a, b):
    return bytes(x ^ y for x, y in zip(a, b))

def left_shift(block):
    shifted = int.from_bytes(block, byteorder='big') << 1
    shifted &= (1 << 128) - 1
    return shifted.to_bytes(16, byteorder='big')

def print_hex(label, data):
    print(f"{label}: {binascii.hexlify(data).decode()}")

# -------- CONSTANT --------
Rb = 0x87

# -------- SUBKEY GENERATION --------
def generate_subkeys(key):
    cipher = AES.new(key, AES.MODE_ECB)
    zero_block = bytes(16)

    L = cipher.encrypt(zero_block)
    print_hex("L (AES-ENC of 0)", L)

    # K1
    if (L[0] & 0x80) == 0:
        K1 = left_shift(L)
    else:
        K1 = xor_bytes(left_shift(L), (Rb).to_bytes(16, 'big'))
    print_hex("K1", K1)

    # K2
    if (K1[0] & 0x80) == 0:
        K2 = left_shift(K1)
    else:
        K2 = xor_bytes(left_shift(K1), (Rb).to_bytes(16, 'big'))
    print_hex("K2", K2)

    return K1, K2

# -------- CMAC FUNCTION --------
def cmac(key, message):
    cipher = AES.new(key, AES.MODE_ECB)
    block_size = 16

    print("\n--- SUBKEY GENERATION ---")
    K1, K2 = generate_subkeys(key)

    # Blocks
    if len(message) == 0:
        n = 1
        flag = False
    else:
        n = (len(message) + block_size - 1) // block_size
        flag = (len(message) % block_size == 0)

    print(f"\nTotal Blocks: {n}")

    blocks = [message[i*block_size:(i+1)*block_size] for i in range(n)]

    # Last block
    if flag:
        print("\nLast block COMPLETE → XOR with K1")
        last_block = xor_bytes(blocks[-1], K1)
    else:
        print("\nLast block INCOMPLETE → Padding + XOR with K2")
        padded = pad(blocks[-1], block_size)
        print_hex("Padded Last Block", padded)
        last_block = xor_bytes(padded, K2)

    print_hex("Processed Last Block", last_block)

    # CMAC computation
    X = bytes(block_size)
    print_hex("\nInitial X", X)

    for i in range(n - 1):
        print(f"\n--- Block {i+1} ---")
        print_hex("Block", blocks[i])

        Y = xor_bytes(X, blocks[i])
        print_hex("X XOR Block", Y)

        X = cipher.encrypt(Y)
        print_hex("AES Output", X)

    # Final block
    print("\n--- Final Block ---")
    Y = xor_bytes(X, last_block)
    print_hex("X XOR LastBlock", Y)

    T = cipher.encrypt(Y)
    print_hex("Final CMAC Tag", T)

    return T

# -------- USER INPUT --------
key_input = input("Enter key (16 characters): ")
message_input = input("Enter message: ")

# Ensure key is 16 bytes
key = key_input.encode()
if len(key) != 16:
    print("Key must be exactly 16 bytes (16 characters).")
    exit()

message = message_input.encode()

print("\nKey:", key)
print("Message:", message)

# -------- RUN CMAC --------
cmac(key, message)