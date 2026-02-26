# RSA Algorithm Implementation with Intermediate Steps

# Function to check prime number
def is_prime(n):
    if n <= 1:
        return False
    for i in range(2, int(n**0.5) + 1):
        if n % i == 0:
            return False
    return True


# Function to find gcd
def gcd(a, b):
    while b != 0:
        a, b = b, a % b
    return a


# Function to find modular inverse using Extended Euclidean Algorithm
def mod_inverse(e, phi):
    for d in range(1, phi):
        if (e * d) % phi == 1:
            return d
    return None


def rsa():
    print("=== RSA Algorithm Implementation ===\n")

    # Step 1: Input two prime numbers
    p = int(input("Enter prime number p: "))
    q = int(input("Enter prime number q: "))

    # Prime checking
    if not is_prime(p) or not is_prime(q):
        print("Both numbers must be prime!")
        return

    print("\nStep 1: Prime numbers verified")
    print("p =", p)
    print("q =", q)

    # Step 2: Compute n
    n = p * q
    print("\nStep 2: Compute n = p * q")
    print("n =", n)

    # Step 3: Compute Euler Totient Function
    phi = (p - 1) * (q - 1)
    print("\nStep 3: Compute φ(n) = (p-1)(q-1)")
    print("φ(n) =", phi)

    # Step 4: Choose e
    print("\nStep 4: Choose e such that 1 < e < φ(n) and gcd(e, φ(n)) = 1")
    for i in range(2, phi):
        if gcd(i, phi) == 1:
            e = i
            break

    print("Selected e =", e)

    # Step 5: Compute d
    print("\nStep 5: Compute d such that (d * e) mod φ(n) = 1")
    d = mod_inverse(e, phi)
    print("Computed d =", d)

    # Public and Private Keys
    print("\nPublic Key (e, n) =", (e, n))
    print("Private Key (d, n) =", (d, n))

    # Step 6: Encryption
    message = int(input("\nEnter message (integer less than n): "))
    print("\nEncryption:")
    print("Cipher = message^e mod n")
    cipher = pow(message, e, n)
    print("Cipher =", cipher)

    # Step 7: Decryption
    print("\nDecryption:")
    print("Message = cipher^d mod n")
    decrypted = pow(cipher, d, n)
    print("Decrypted Message =", decrypted)


# Run program
rsa()