#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function
from parser import process
import numbers


class Program(object):
    """Represents a FRACTRAN program.

    Construction:
        Takes a list of fractions, and optionally a description.
        A fraction can either be a tuple of (numerator, denominator), or
            an object with 'numerator' and 'denominator' fields.
            Ex: fractions.Fraction(3, 2), or (3, 2)
    """
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
                    raise TypeError("must provide valid fraction")
            if not isinstance(num, numbers.Integral):
                raise TypeError("numerator must be numbers.Integral")
            if not isinstance(denom, numbers.Integral):
                raise TypeError("denominator must be numbers.Integral")
            self.__fracs.append((num, denom))

    @staticmethod
    def from_file(filename):
        """Parses a .frac file into a Program."""
        return Program(process(filename))

    def description(self):
        return self.__description

    def raw_fractions(self):
        return self.__fracs

    def eval_gen(self, n):
        """Runs the program with input n, yielding intermediate results.

        Example:
        >>> p = Program([(5, 2), (5, 3)])
        >>> g = p.eval_gen(12)
        >>> g.next()
        30
        >>> g.next()
        75
        >>> g.next()
        125
        >>> g.next()
        StopIteration
        """
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
        """Returns a list of each intermediate step in evaluation.

        Equivalent to list(self.eval_gen())"""
        return list(self.eval_gen(n))

    def eval_last(self, n):
        """Evaluates the output of running the program on input n.

        Example:
        >>> Program([(5, 2), (5, 3)]).eval_last(12)
        125
        """
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
