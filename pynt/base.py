"""
base.py
=======

Fundamental components for a simple python number theory library.

License Info
============

(c) David Lowry-Duda 2018 <davidlowryduda@davidlowryduda.com>

This is available under the MIT License. See
<https://opensource.org/licenses/MIT> for a copy of the license,
or see the home github repo
<https://github.com/davidlowryduda/pynt>.
"""
from typing import List, Tuple, Union
from itertools import product as cartesian_product
import numpy


def gcd(num1: int, num2: int) -> int:
    """
    Returns the greatest common divisor of `num1` and `num2`.

    Examples:
    >>> gcd(12, 30)
    6
    >>> gcd(0, 0)
    0
    >>> gcd(-1001, 26)
    13
    """
    if num1 == 0:
        return num2
    if num2 == 0:
        return num1
    if num1 < 0:
        num1 = -num1
    if num2 < 0:
        num2 = -num2
    # This is the Euclidean algorithm
    while num2 != 0:
        num1, num2 = num2, num1 % num2
    return num1


def smallest_prime_divisor(num: int, bound: Union[int, None] = None) -> int:
    """
    Returns the smallest prime divisor of the input `num` if that divisor is
    at most `bound`. If none are found, this returns `num`.

    Input:
        num: a positive integer
        bound: an optional bound on the size of the primes to check. If not
               given, then it defaults to `num`.

    Output:
        The smallest prime divisor of `num`, or `num` itself if that divisor is
        at least as large as `bound`.

    Raises:
        ValueError: if num < 1.

    Examples:
    >>> smallest_prime_divisor(15)
    3
    >>> smallest_prime_divisor(1001)
    7
    """
    if num < 1:
        raise ValueError("A positive integer is expected.")
    if num == 1:
        return num
    for prime in [2, 3, 5]:
        if num % prime == 0:
            return prime
    if bound is None:
        bound = num
    # Possible prime locations mod 2*3*5=30
    diffs = [6, 4, 2, 4, 2, 4, 6, 2]
    cand = 7
    i = 1
    while cand <= bound and cand*cand <= num:
        if num % cand == 0:
            return cand
        cand += diffs[i]
        i = (i + 1) % 8
    return num


# primesfrom2to(n) from
# https://stackoverflow.com/questions/2068372/fastest-way-to-list-all-primes-below-n
def primes(limit):
    """
    Returns the numpy array of primes up to (and not including) `limit`.

    Examples:
    >>> primes(10)
    array([2, 3, 5, 7])
    """
    sieve = numpy.ones(limit // 3 + (limit % 6 == 2), dtype=numpy.bool)
    for i in range(1, int(limit ** 0.5) // 3 + 1):
        if sieve[i]:
            k = (3 * i + 1) | 1
            sieve[k * k // 3::2 * k] = False
            sieve[k * (k - 2 * (i & 1) + 4) // 3:: 2 * k] = False
    return numpy.r_[2, 3, ((3 * numpy.nonzero(sieve)[0][1:] + 1) | 1)]


def factor(num: int) -> List[Tuple[int, int]]:
    """
    Returns the factorization of `num` as a list of tuples of the form (p, e)
    where `p` is a prime and `e` is the exponent of that prime in the
    factorization.

    Input:
        num: an integer to factor

    Output:
        a list of tuples (p, e), sorted by the size of p.

    Examples:
    >>> factor(100)
    [(2, 2), (5, 2)]
    >>> factor(-7007)
    [(7, 2), (11, 1), (13, 1)]
    >>> factor(1)
    []
    """
    if num in (-1, 0, 1):
        return []
    if num < 0:
        num = -num
    factors = []
    while num != 1:
        prime = smallest_prime_divisor(num)
        exp = 1
        num = num // prime
        while num % prime == 0:
            exp += 1
            num = num // prime
        factors.append((prime, exp))
    return factors


def factors(num: int) -> List[int]:
    """
    Returns the list of factors of an integer.

    Examples:
    >>> factors(6)
    [1, 2, 3, 6]
    >>> factors(30)
    [1, 2, 3, 5, 6, 10, 15, 30]
    """
    factorization = factor(num)
    primes_, exps = zip(*factorization)
    exp_choices = cartesian_product(*[range(exp+1) for exp in exps])
    ret = []
    for exp_choice in exp_choices:
        val = 1
        for prime, exp in zip(primes_, exp_choice):
            val *= (prime**exp)
        ret.append(val)
    return sorted(ret)
