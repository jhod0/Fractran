#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Jackson O'Donnell
#   jacksonhodonnell@gmail.com

"""Scipt for generating animations of FRACTRAN execution.

Takes the same two arguments as main.py, and uses matplotlib
to generate a bar plot.

The x-axis represents prime numbers, and the y-axis, or bar
values, represent the exponent of each prime in the factorization
of the input number.

This script iterates each step of the FRACTRAN execution, updating
the bar plot as the input number changes.

Optionally, takes a third argument, a file name, and writes
the animation to that file."""

from __future__ import division, print_function
import matplotlib.pyplot as plt
import matplotlib.animation as animation
import sys
from core import Program
from parser.core import parse_num
from factor import factor


program = None
program_gen = None
this_num = None
bar = None
fig, ax = plt.subplots()


def get_expts(nrange):
    nums = factor(this_num)
    return [nums.get(n, 0)
            for n in nrange]


def inc():
    global this_num
    try:
        this_num = program_gen.next()
    except StopIteration:
        pass


def init(nrange = [2, 3, 5, 7, 11, 13, 17, 19], maxheight=10):
    global bar, ax
    bar = ax.bar(range(1, len(nrange)+1), get_expts(nrange), 
                 0.35, align='center')
    ax.set_xticks(range(1, len(nrange)+1))
    ax.set_xticklabels(tuple(str(n) for n in nrange))
    ax.set_ylim((0, maxheight))


def animate(i, nrange=[2, 3, 5, 7, 11, 13, 17, 19]):
    for i, v in enumerate(get_expts(nrange)):
        bar[i].set_height(v)
    inc()
    return bar,


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: {} <program> <input> [ <outfile> ]".format(sys.argv[0]), 
              file=sys.stderr)
        sys.exit(-1)
    try:
        program = Program.from_file(sys.argv[1])
    except IOError:
        print("Could not open program file: {}".format(sys.argv[1]),
              file=sys.stderr)
        sys.exit(-1)
    this_num = parse_num(sys.argv[2])
    program_gen = program.eval_gen(this_num)
    ani = animation.FuncAnimation(fig, animate, 10, init_func=init,
                                  interval=1000)
    if len(sys.argv) == 4:
        ani.save(sys.argv[3], writer='imagemagick')
    else:
        plt.show()
