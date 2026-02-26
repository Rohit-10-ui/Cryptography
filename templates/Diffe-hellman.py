# Diffie-Hellman Key Exchange with Detailed Intermediate Steps

def diffie_hellman():
    print("=== Diffie-Hellman Key Exchange (Detailed Steps) ===\n")
    
    # Step 1: Public parameters
    p = int(input("Enter a prime number (p): "))
    g = int(input("Enter a primitive root (g): "))
    
    print("\nStep 1: Publicly agreed values")
    print("Prime number (p) =", p)
    print("Primitive root (g) =", g)
    
    # Step 2: Private keys
    a = int(input("\nEnter Alice's private key (a): "))
    b = int(input("Enter Bob's private key (b): "))
    
    print("\nStep 2: Private Keys")
    print("Alice's private key (a) =", a)
    print("Bob's private key (b) =", b)
    
    # Step 3: Compute Public Keys
    print("\nStep 3: Public Key Computation")
    
    print("\nAlice computes:")
    print("A = g^a mod p")
    print(f"A = {g}^{a} mod {p}")
    A_full = g ** a
    print(f"A = {A_full} mod {p}")
    A = A_full % p
    print("A =", A)
    
    print("\nBob computes:")
    print("B = g^b mod p")
    print(f"B = {g}^{b} mod {p}")
    B_full = g ** b
    print(f"B = {B_full} mod {p}")
    B = B_full % p
    print("B =", B)
    
    # Step 4: Exchange Public Keys
    print("\nStep 4: Exchange Public Keys")
    print("Alice sends A =", A, "to Bob")
    print("Bob sends B =", B, "to Alice")
    
    # Step 5: Shared Secret Computation
    print("\nStep 5: Shared Secret Computation")
    
    print("\nAlice computes shared key:")
    print("K = B^a mod p")
    print(f"K = {B}^{a} mod {p}")
    K_alice_full = B ** a
    print(f"K = {K_alice_full} mod {p}")
    K_alice = K_alice_full % p
    print("Shared Key (Alice) =", K_alice)
    
    print("\nBob computes shared key:")
    print("K = A^b mod p")
    print(f"K = {A}^{b} mod {p}")
    K_bob_full = A ** b
    print(f"K = {K_bob_full} mod {p}")
    K_bob = K_bob_full % p
    print("Shared Key (Bob) =", K_bob)
    
    # Final Verification
    print("\nStep 6: Verification")
    if K_alice == K_bob:
        print("Key Exchange Successful!")
        print("Final Shared Secret Key =", K_alice)
    else:
        print("Key Exchange Failed!")

# Run program
diffie_hellman()