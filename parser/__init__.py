#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function
from .core import parse_line, FracParseException


def process(filename):
    """Takes a filename and returns a list of the fraction pairs.

    Treats '#' as a comment.

    Say add.frac is a file which contains:
        # Addition
        # Input: 2**a * 3**b
        # Output: 3**(a+b)
        3 / 2

    >>> process('add.frac')
    [(3, 2)]

    Can also evaluate exponents and multiplication, python-style."""
    def process_helper(f):
        fracs = []
        for i, line in enumerate(f):
            if line.isspace():
                continue
            try:
                parsed = parse_line(line)
                if parsed:
                    fracs.append(parsed)
            except FracParseException as e:
                print("Error parsing file at line {}: \n\t{}".format(i+1, line))
                print(fracs)
                raise e
        return fracs

    if type(filename) == file:
        return process_helper(filename)
    with open(filename) as frac_file:
        return process_helper(frac_file)
