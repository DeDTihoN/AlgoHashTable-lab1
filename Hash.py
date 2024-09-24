import random
from sympy import isprime


class Hash:
    PRIME_INTERVAL = (31, 100)  # Interval for prime p
    MOD_INTERVAL = (int(1e9), int(1e9) + 100)  # Interval for m near 1e9

    def __init__(self, p=None, m=None):
        # Default m value and random p from the prime interval if not provided
        self.m = m if m is not None else random.randint(*self.MOD_INTERVAL)
        self.p = p if p is not None and isprime(p) else self._get_random_prime(*self.PRIME_INTERVAL)

    def _get_random_prime(self, start, end):
        primes = [x for x in range(start, end + 1) if isprime(x)]
        return random.choice(primes)

    def compute_hash(self, s: str):
        """Computes the hash of the given string s."""
        hash_value = 0
        p_pow = 1
        for c in s:
            hash_value = (hash_value + (ord(c) - ord('a') + 1) * p_pow) % self.m
            p_pow = (p_pow * self.p) % self.m
        return hash_value
