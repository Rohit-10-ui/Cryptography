#!/usr/bin/env python3
"""
Test script for number theory endpoints
"""
import json
import urllib.request
import time

# Give Flask time to fully start
time.sleep(2)

BASE_URL = "http://localhost:5000"

def test_endpoint(name, endpoint, data):
    """Test an API endpoint"""
    print(f"\n{'='*50}")
    print(f"Testing: {name}")
    print(f"{'='*50}")
    print(f"Request: {json.dumps(data)}")
    
    try:
        req = urllib.request.Request(
            f"{BASE_URL}{endpoint}",
            data=json.dumps(data).encode('utf-8'),
            headers={'Content-Type': 'application/json'}
        )
        with urllib.request.urlopen(req, timeout=5) as response:
            result = json.loads(response.read().decode('utf-8'))
            print(f"Response: {json.dumps(result, indent=2)}")
            return result
    except Exception as e:
        print(f"ERROR: {e}")
        return None

# Run tests
print("Number Theory API Tests")
print("=" * 50)

# Test 1: Primality test
test_endpoint(
    "Primality Test (17 - Prime)",
    "/api/primality-test",
    {"number": "17"}
)

test_endpoint(
    "Primality Test (100 - Composite)",
    "/api/primality-test",
    {"number": "100"}
)

# Test 2: Primitive root
test_endpoint(
    "Primitive Root (7)",
    "/api/primitive-root",
    {"number": "7"}
)

test_endpoint(
    "Primitive Root (11)",
    "/api/primitive-root",
    {"number": "11"}
)

# Test 3: Euclid's algorithm
test_endpoint(
    "GCD (48, 18)",
    "/api/euclid",
    {"number1": "48", "number2": "18"}
)

test_endpoint(
    "GCD (100, 35)",
    "/api/euclid",
    {"number1": "100", "number2": "35"}
)

print("\n" + "="*50)
print("All tests completed!")
print("="*50)
