#!/usr/bin/env python
# -*- coding: utf-8 -*-

from __future__ import division, print_function
import re


def parse_line(line):
    """Parses a line of a file into a (numerator, denominator) pair"""
    assert type(line) == str
    original_line = line
    if line == '':
        return None
    elif line.startswith('#'):
        return None
    elif '#' in line:
        line = line[:line.index('#')]
    try:
        numerator, denominator = line.split('/')
    except ValueError:
        raise MalformedLineException("line not split by '/'", original_line)
    return parse_num(numerator), parse_num(denominator)

def parse_num(string):
    if re.findall('[^0-9\W]', string):
        raise InvalidNumberException("Could not evaluate number", string)
    try: 
        out = eval(string)
        if type(out) not in (int, long):
            raise NotIntegerException("does not evaluate to integer", string)
        return out
    except Exception as e:
        print("error evaluating")
        raise e

# Error types
class FracParseException(Exception):
    pass

class MalformedLineException(FracParseException):
    pass

class InvalidNumberException(FracParseException):
    pass

class NotIntegerException(FracParseException):
    pass
