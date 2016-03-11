#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function
import numbers


def make_fun(name):
    def out_fn(self, other):
        return getattr(int(self), name)(int(other))
    out_fn.func_name = name
    return out_fn


class AbstractFactoredInt(numbers.Integral):
    def __init__(self, val):
        self._value = val


def __long__(self):
    return self._value


for attr in ['add', 'and', 'abs', 'div', 'eq', 'floordiv', 'invert', 'le',
             'lshift', 'lt', 'mod', 'mul', 'neg', 'or', 'pos', 'pow', 'radd',
             'rand', 'rdiv', 'rfloordiv', 'rlshift', 'rmod', 'rmul', 'ror',
             'rpow', 'rrshift', 'rshift', 'rtruediv', 'rxor', 'truediv',
             'trunc', 'xor']:
    real_name = '__{}__'.format(attr)
    setattr(AbstractFactoredInt, real_name, make_fun(real_name))

del make_fun
