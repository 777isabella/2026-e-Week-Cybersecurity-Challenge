#Challenge #1: Cryptanalysis Project
#Isabella Morgan 20629238

#Prime Factorization of N
# N = 99 99 99 99 97 84 00 00 00 00 96 39
# = 999999999784000000009639

import math
import time

# source: https://www.geeksforgeeks.org/dsa/pollards-rho-algorithm-prime-factorization/

def pollard_rho(n):
    #even #s are trivially factored, return 2
    if n % 2 == 0:
        return 2

    #tortoise(x), hare (y)
    #c is constant in pseudo-random func f(x) = x^2 + c mod n
    x = 2
    y = 2
    c = 1
    d = 1 #gcd result; stays 1 until factor is found

    while d == 1:
        x = (x * x + c) % n     #tortoise move
        y = (y * y + c) % n     #hare first step
        y = (y * y + c) % n     #hare 2nd step

        #check if diff. between tortoise and hare shares a factor
        # w/ N. if gcd > 1, non-trivial divisor found
        d = math.gcd(abs(x - y), n)

    #if d ==n, the algorithm got stuck in a complete cycle w/out finding
    # a useful factor. handled by retrying w/ c incremented
    if d == n:
        c += 1
        return pollard_rho(n)

    #d is a non-trivial factor of n
    # 1 < d < n
    return d

#primality test:
#verify if factors are prime
def is_prime(n):
    if n < 2:
        return False
    if n < 4:
        return True
    if n % 2 == 0 or n % 3 == 0:
        return False

    #check divisors of 6k-1 and 6k+1 up to swrt(n)
    i = 5
    while i * i <= n:
        if n % i == 0 or n % (i + 2) == 0:
            return False
        i += 6  #move to next 6k

    return True     #no divisors found ; n is prime

#factorization wrapper
#factorization of the RSA modulus n
#steps:
#   1. print info abt n (values and bit-length)
#   2. call pollard_rho()
#   3. derive second factor as n // p (exact int division)
#   4. return both factors in asc. order (p <= q)
def factorize(n):
    print(f"Target N = {n}")
    print(f"Bit length: {n.bit_length()} bits")
    print(f"Decimal digits: {len(str(n))}\n")
    print("Running Pollard Rho's algorithm...")
    start = time.time()
    p = pollard_rho(n)
    elapsed = time.time() - start

    # N = p*q, second factor is N/ first
    q = n // p

    #return smaller factor as p, larger as q
    if p > q:
        p, q = q, p

    #tuple : (p, q, elapsed)
    return p, q, elapsed

def main():
    N = 999999999784000000009639

    p, q, elapsed = factorize(N)

    print(f"Factorization complete in {elapsed:.4f} seconds!!!\n")
    print("=" * 50)
    print(f" p = {p}")
    print(f" q = {q}")
    print("=" * 50)

    #verify answer
    print(f"\n Verification:")
    print(f" p is prime: {is_prime(p)}")
    print(f" q is prime: {is_prime(q)}")
    print(f" p * q == N: {p * q == N}")

    #security analysis
    print(f"\nRSA modulus successfully cracked.")
    print(f"N is only {N.bit_length()} bits long, which is too short to be secure.")
    print(f"Pollard's Rho needs roughly N^(1/4) approx {int(N**0.25):,} steps,")
    print(f"which is trivial for modern hardware.")
    print(f"Modern RSA requires a minimum of 2048-bit keys (recommended: 4096-bit).")

if __name__ == "__main__":
    main()
