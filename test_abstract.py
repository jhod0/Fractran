#!/usr/bin/env python
# -*- coding: utf-8 -*-
# Author: Jackson O'Donnell
#   jacksonhodonnell@gmail.com
"""Test cases for module abstract.

Intended for use with Nose. To test, simply run nosetests in this
directory."""

from __future__ import division, print_function
import abstract
from abstract import Add, Copy, Mult


def test_add():
    add = Add.compile({"A": 2, "B": 3, "C": 5})
    assert add.eval_last(2**12 * 3**3) == 5**15
    assert add.eval_last(2**0 * 3**7) == 5**7
    add = Add.compile({"A": 5, "B": 7, "C": 2})
    assert add.eval_last(5**3 * 7**8) == 2**11
    assert add.eval_last(5**10 * 7**3) == 2**13


def test_copy():
    cpy = Copy.compile({"A": 2, "B": 3, "C": 5})
    assert cpy.eval_last(2**11) == 3**11 * 5**11
    assert cpy.eval_last(2**4) == 3**4 * 5**4
    cpy = Copy.compile({"A": 11, "B": 5, "C": 7})
    assert cpy.eval_last(11**11) == 5**11 * 7**11
    assert cpy.eval_last(11**4) == 5**4 * 7**4


def test_mult():
    mult = Mult.compile({"A": 2, "B": 3, "C": 5})
    assert mult.eval_last(2**3 * 3**5) == 5**15
    assert mult.eval_last(2**7 * 3**3) == 5**21
    assert mult.eval_last(2**9) == 1
    assert mult.eval_last(3**11) == 1
    mult = Mult.compile({"A": 17, "B": 13, "C": 5})
    assert mult.eval_last(17 * 13) == 5
    assert mult.eval_last(17**2 * 13**5) == 5**10
