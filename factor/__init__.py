#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function
import numbers
from . import abstract


def factor(n):
    if not isinstance(n, numbers.Integral):
        raise TypeError("must provide numbers.Integral")
    assert n > 0
    out = dict()
    fac = 2
    while n > 1 and fac * fac <= n:
        if n % fac == 0:
            out[fac] = 1
            n //= fac
        while n % fac == 0:
            out[fac] += 1
            n //= fac
        if fac == 2:
            fac += 1
        else:
            fac += 2
    if n != 1:
        out[n] = 1
    return out

class FactoredInt(abstract.AbstractFactoredInt):
    def __init__(self, n=1):
        self._facs = factor(n)

    def _set_facs(self, facs):
        if not type(facs) == dict:
            raise TypeError()
        self._facs = facs

    @classmethod
    def from_factors(cls, facs):
        """Creates a FactoredInt instance from an iterator of (n, p) pairs.
        
        Each (n, p) pair should represent a prime factor and its power.
        
        Examples:
            >>> int(from_factors([(2, 3), (3, 2)]) # 2**3 * 3**2 = 72
            72
        """
        out = cls()
        out._set_facs(dict(facs))
        return out
