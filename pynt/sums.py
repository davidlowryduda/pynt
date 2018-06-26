"""
sums.py
=======

Number theoretic functions for manipulating and creating sums of arithmetic
functions.

License Info
============

(c) David Lowry-Duda 2018 <davidlowryduda@davidlowryduda.com>

This is available under the MIT License. See
<https://opensource.org/licenses/MIT> for a copy of the license,
or see the home github repo
<https://github.com/davidlowryduda/pynt>.
"""
from typing import Callable, List, Union
from pynt.base import factors


def convolution_coeff(
        val: int,
        fun1: Callable[[int], Union[int, complex]],
        fun2: Callable[[int], Union[int, complex]],
) -> Union[int, complex]:
    """
    Returns the `val` coefficient of the Dirichlet convolution of `fun1` and
    `fun2`, sometimes written `(fun1 * fun2) (val)`. Equivalently, this returns
    the sum of `fun1(d)*fun2(val/d)` across all divisors `d` of `val`.

    Input:
        val: a positive integer
        fun1: an arithmetic function
        fun2: an arithmetic function

    Output:
        An integer (if fun1 and fun2 return integers) or a complex number.

    Examples:
        >>> def f(x): return 2*x
        >>> def g(x): return 1
        >>> convolution_coeff(6, f, g)  # f(1) + f(2) + f(3) + f(6)
        24
    """
    ret = 0
    for factor in factors(val):
        # mypy complains about this line since it doesn't correctly
        # implement fallback operations. This is in issue
        # https://github.com/python/mypy/issues/2128
        ret += fun1(factor) * fun2(val // factor)
    return ret


def compute_partial_sums(
        seq: List[Union[int, complex]],
) -> List[Union[int, complex]]:
    """
    Returns a list of the partial sums of a sequence.

    Input:
        seq: a list of integers or complex numbers

    Output:
        a list of integers or complex numbers

    Examples:
    >>> compute_partial_sums([1, 1, 1, 1])
    [1, 2, 3, 4]
    """
    ret_list = []
    partial_sum: Union[int, complex] = 0
    for elem in seq:
        # mypy issue 2128 again on this line
        partial_sum += elem
        ret_list.append(partial_sum)
    return ret_list
