#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function
import sys
from parser import process, FracParseException
from parser.core import parse_num
from core import Program
from factor import factor


usage_string = """Usage: {} <fracfile> <arg>


Note: You can pass an argument as '2**3 * 3**5' if you surround it
by single quotes (')
"""


def factor_to_string(num):
    facs = factor(num)
    facs = ["{}**{}".format(n, p)
            for n, p in sorted(facs.items(), key=lambda n: n[0])]
    return ' * '.join(facs)


def process_program(prgm, arg, iter_limit=None):
    previous_vals = set()
    previous_vals.add(arg)
    print("start:\n{}: {}".format(arg, factor_to_string(arg)))
    for i, item in enumerate(prgm.eval_gen(arg)):
        if item in previous_vals:
            print("{}, {}: unbreakable recursion"
                  .format(item, factor_to_string(item)))
            break
        print("{}: {}".format(item, factor_to_string(item)))
        previous_vals.add(item)
        if i == iter_limit:
            print("Iteration limit reached")
            break


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print(usage_string.format(sys.argv[0]))
        sys.exit(1)
    try:
        with open(sys.argv[1]) as f:
            program = Program(process(f))
            arg = parse_num(sys.argv[2])
            process_program(program, arg)
    except IOError as e:
        print("File does not exist: {}".format(sys.argv[1]))
