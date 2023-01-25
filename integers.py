
# Euclid's division algorithm for the nonnegatives
def gcd0(a, b):
    if a == 0:
        return b
    elif b == 0:
        return a
    else:
        if a < b:
            return gcd0(a, b % a)
        else:
            return gcd0(a % b, b)

# a wrapper for the integers
def gcd(a, b):
    assert a != 0 or b != 0
    return gcd0(abs(a), abs(b))

# find x, y s.t. a * x + b * y = gcd(a, b) for nonnegative a, b
def gcdCoeff0(a, b):
    if a == 0:
        return 0, 1, b   # a * 0 + b * 1 = b = gcd(a, b)
    elif b == 0:
        return 1, 0, a   # a * 1 + b * 0 = a = gcd(a, b)
    else:
        if a < b:
            x, y, g = gcdCoeff0(a, b % a)           # a * x + (b % a) * y = g
            return (x - y * (b // a)), y, g     # a * (x - y * (b // a)) + b * y = g
        else:
            x, y, g = gcdCoeff0(a % b, b)           # (a % b) * x + b * y = g
            return x, (y - x * (a // b)), g     # a * x + b * (y - x * (a // b)) = g

# a wrapper for the integers
def gcdCoeff(a, b):
    assert a != 0 or b != 0
    x, y, g = gcdCoeff0(abs(a), abs(b))
    if a < 0:
        x = -x
    if b < 0:
        y = -y
    return x, y, g

# a * {a^{-1}} = 1 mod p
def invModPrime(a, p):
    assert a % p != 0          # gcd(a, p) = 1
    x, _, _ = gcdCoeff(a, p)   # a * x + ? * p = 1
    return x                   # x = a^{-1} mod p


# test
if __name__ == "__main__":
    tested = 0

    for a in range(-30, +30):
        for b in range(-30, +30):
            if a == 0 and b == 0:
                continue
            
            g1 = gcd(a, b)
            x, y, g2 = gcdCoeff(a, b)

            # brutal method to find g
            bound = min(abs(a), abs(b))
            for g in range(bound, 0, -1):
                if a % g == 0 and b % g == 0: # found gcd
                    assert g == g1
                    assert g == g2
                    assert g == a * x + b * y
                    tested += 1
                    break

    for p in (2, 3, 5, 7, 11, 13, 17, 19, 23, 29):
        for a in range(1, p):
            assert (a * invModPrime(a, p)) % p == 1
            tested += 1
    
    print("tested : " + str(tested))







