#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function
import numbers


class Program(object):
    def __init__(self, ls, description=None):
        self.__fracs = []
	self.__description = description
        for frac in ls:
            try:
                num, denom = frac
            except TypeError:
                try:
                    num, denom = frac.numerator, frac.denominator
                except:
                    raise TypeError("must provide fractran.Program either ")
            if not isinstance(num, numbers.Integral):
                raise TypeError("numerator must be numbers.Integral")
            if not isinstance(denom, numbers.Integral):
                raise TypeError("denominator must be numbers.Integral")
            self.__fracs.append((num, denom))
    
    def description(self):
        return self.__description

    def eval_gen(self, n):
        if not isinstance(n, numbers.Integral):
            raise TypeError("can only evaluate numbers.Integral")
        while True:
            change = False
            for (num, denom) in self.__fracs:
                if (n * num) % denom == 0:
                    n = (n * num) // denom
                    change = True
                    yield n
                    break
            if not change:
                break

    def eval(self, n):
        return list(self.eval_gen(n))

    def eval_last(self, n):
        if not isinstance(n, numbers.Integral):
            raise TypeError("can only evaluate numbers.Integral")
        change = True
        while change:
            change = False
            for num, denom in self.__fracs:
                if (n * num) % denom == 0:
                    n = (n * num) // denom
                    change = True
                    break
        return n
