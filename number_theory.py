"""
Number Theory Algorithms
- Rabin-Miller Primality Test
- Primitive Root Finding
- Euclid's Algorithm (GCD)
"""

import random


def gcd_euclid(a, b):
    """
    Euclid's algorithm to find GCD of two numbers.
    Returns: (gcd, x, y) where gcd = a*x + b*y (Extended Euclidean Algorithm)
    """
    if b == 0:
        return a, 1, 0
    else:
        gcd, x1, y1 = gcd_euclid(b, a % b)
        x = y1
        y = x1 - (a // b) * y1
        return gcd, x, y


def rabin_miller(n, k=5):
    """
    Rabin-Miller primality test.
    Returns: True if n is probably prime, False if definitely composite.
    k: number of rounds (higher k = higher confidence)
    """
    if n < 2:
        return False
    if n == 2 or n == 3:
        return True
    if n % 2 == 0:
        return False
    
    # Write n-1 as 2^r * d where d is odd
    r, d = 0, n - 1
    while d % 2 == 0:
        r += 1
        d //= 2
    
    # Witness loop
    for _ in range(k):
        a = random.randint(2, n - 2)
        x = pow(a, d, n)  # a^d mod n
        
        if x == 1 or x == n - 1:
            continue
        
        composite = True
        for _ in range(r - 1):
            x = pow(x, 2, n)
            if x == n - 1:
                composite = False
                break
        
        if composite:
            return False
    
    return True

def is_prime(n):
    if n<=1:
        return False
    for i in range(2,n//2+1):
        if n%i==0:
            return False
    return True

def find_primitive_root(n):
    """
    Find a primitive root modulo n.
    A primitive root g modulo n is a number where:
    g^1, g^2, ..., g^φ(n) mod n generates all numbers coprime to n.
    
    Works best when n is prime.
    Returns: A primitive root if found, None otherwise.
    """
    if not is_prime(n):
        return "Primitive Roots does not exists"
    roots=[]
    for g in range(2,n):
        values=set()
        for k in range(1,n):
            values.add(pow(g,k,n))
        if len(values)==n-1:
            roots.append(g)
    return roots


def get_number_theory_analysis(number):
    """
    Analyze a number with all three operations.
    Returns a dictionary with results.
    """
    try:
        num = int(number)
        if num < 0:
            return {'error': 'Please enter a positive number'}
        
        results = {
            'number': num,
            'is_prime': rabin_miller(num, k=10),
            'primitive_root': None,
            'gcd_info': None
        }
        
        # Find primitive root if number is prime
        if results['is_prime'] and num > 2:
            results['primitive_root'] = find_primitive_root(num)
        
        return results
    
    except ValueError:
        return {'error': 'Invalid number format'}


def format_euclid_result(a, b):
    """
    Format Euclidean algorithm result nicely.
    """
    gcd, x, y = gcd_euclid(int(a), int(b))
    return {
        'gcd': gcd,
        'a': int(a),
        'b': int(b),
        'equation': f"gcd({a}, {b}) = {a}*{x} + {b}*{y} = {gcd}",
        'x': x,
        'y': y
    }
