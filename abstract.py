#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Jackson O'Donnell
#   jacksonhodonnell@gmail.com

from __future__ import division, print_function
from core import Program
import copy


class PrimeGen(object):
    def __init__(self):
        self.primes = []
        self.prohibited = []
        self.n = 2

    def _is_prime(self):
        prime = True
        for p in self.primes:
            if self.n % p == 0:
                prime = False
                break
        return prime

    def prohibit(self, prohibited):
        self.prohibited = prohibited

    def next_prime(self):
        pro = True
        while pro:
            while not self._is_prime():
                self.n += 1
            self.primes.append(self.n)
            pro = self.n in self.prohibited
        return self.n

    def iter(self):
        while True:
            yield self.next_prime()


class SubProgram(object):
    """An abstract representation of a FRACTRAN subprogram.

    >>> # Addition example
    >>> addition = SubProgram([([(1, "A")], [(1, "C")]),
                               ([(1, "B")], [(1, "C")])],
                              registers=["A", "B", "C"])
    >>> program = addition.compile({"A": 2, "B": 3, "C": 5})
    >>> program.eval(12)
    [30, 75, 125]
    """
    def __init__(self, rules, registers, inputs=None, name=None):
        """Creates a SubProgram with the given rules and registers.

        If inputs is not provided, all registers are treated as
        inputs."""
        if inputs is None:
            self.in_names = registers
        else:
            for name in inputs:
                assert name in registers
            self.in_names = inputs
        self._registers = registers
        self._rules = rules
        self.name = name

    def rename(self, new_names):
        """Renames all registers in place, as specified in new_names."""
        self._registers = [new_names.get(reg, reg)
                           for reg in self._registers]
        self.in_names = [new_names.get(reg, reg)
                         for reg in self.in_names]

        for i, (left, right) in enumerate(self._rules):
            new_left = []
            for ln, lname in left:
                new_left.append((ln, new_names.get(lname, lname)))

            new_right = []
            for right_item in right:
                try:
                    rn, rname = right_item
                    new_right.append((rn, new_names.get(rname, rname)))
                except TypeError:
                    right_item.rename(new_names)
                    new_right.append(right_item)

            self._rules[i] = (new_left, new_right)

    def compile(self, reg_vals=None, primes=None):
        """Compiles a SubProgram to a Program."""
        if primes is None:
            primes = PrimeGen()

        if reg_vals is None:
            reg_vals = {reg: primes.next_prime()
                        for reg in self.in_names}
        else:
            # All provided values must be
            # valid registers
            for reg in reg_vals:
                assert reg in self._registers
            primes.prohibit(reg_vals.values())
        out_fractions = []

        for left, right in self._rules:
            denom = 1
            for n, name in left:
                assert name in self._registers
                if name in reg_vals:
                    reg = reg_vals[name]
                else:
                    reg_vals[name] = primes.next_prime()
                    reg = reg_vals[name]
                denom *= reg**n

            num = 1
            for right_item in right:
                try:
                    # If rule is number, name pair,
                    # do the same as above
                    n, name = right_item
                    if name in reg_vals:
                        reg = reg_vals[name]
                    else:
                        reg_vals[name] = primes.next_prime()
                        reg = reg_vals[name]
                    num *= reg**n
                except TypeError:
                    # Rule is applied subprogram
                    entry, proc = self.compile_applied(right_item, reg_vals,
                                                       primes)
                    # Prepend compiled subprogram to this subprogram
                    out_fractions = proc + out_fractions
                    # Make this rule an entry point for the subprogram
                    num *= entry

            # Add this rule to the program
            out_fractions.append((num, denom))

        description = "Compiled from SubProgram {}".format(self)
        return Program(out_fractions, description=description)

    @staticmethod
    def compile_applied(applied, vals, prime_gen):
        # rule is a AppliedProgram
        arg_names = applied.get_input_names()
        compiled = applied.compile({arg: vals[arg]
                                    for arg in arg_names},
                                   prime_gen)
        enter = prime_gen.next_prime()
        reenter = prime_gen.next_prime()

        proc_compiled = [(num*reenter, denom*enter)
                         for num, denom in compiled.raw_fractions()]
        return enter, proc_compiled + [(enter, reenter), (1, enter)]

    def __call__(self, *args):
        """Creates an AppliedProgram"""
        out = AppliedProgram(copy.deepcopy(self._rules), self._registers[:], 
                             inputs=self.in_names[:], name=self.name)
        assert len(args) == len(self.in_names)
        out.rename({cur: new for cur, new in zip(self.in_names, args)})
        return out


class AppliedProgram(SubProgram):
    def get_input_names(self):
        return self.in_names

    def __str__(self):
        return "{}({})".format(self.name, ', '.join(self.in_names))


Add = SubProgram([([(1, "A")], [(1, "C")]),
                  ([(1, "B")], [(1, "C")])],
                 registers=["A", "B", "C"],
                 name="Add")

Copy = SubProgram([([(1, "A")], [(1, "B"), (1, "C")])],
                  registers=["A", "B", "C"],
                  name="Copy")

Mult = SubProgram([([(1, "D")], [(1, "B")]), 
                   ([(1, "A")], [Copy("B", "C", "D")]),
                   ([(1, "B")], [])],
                  registers=["A", "B", "C", "D"],
                  inputs=["A", "B", "C"],
                  name="Mult")
