# FRACTRAN Interpreter

Interpreter for the [FRACTRAN](https://en.wikipedia.org/wiki/FRACTRAN) esoteric programming language.

For information about FRACTRAN, check its wikipedia page, that is beyond the scope of this documentation.

## Usage

Run main.py with a program file and an input number.

```bash
$ python2 main.py examples/add.frac 12
start:
12: 2**2 * 3**1
18: 2**1 * 3**2
27: 3**3
```

Example FRACTRAN program files are found in the [examples directory](examples).

The animate.py script can be used to generate a matplotlib animation of a program's execution, showing exponents as bars on a bar plot, and iterating.
Naturally, it require matplotlib.

## File Formats

Input files should contain one fraction per line, in the form:
```
2 * 3 * 5**7 / 7 * 11**2
```
In Python style, exponents are denoted by (\*\*), not (^).
Comments are allowed with the hash (#) character

Check the examples in the examples directory.

## Requirements

Works with Python 2.7, working on compatibility with Python 3.
The animate.py script requires matplotlib. It is known to work with version 1.4.3, others have not been tested.
