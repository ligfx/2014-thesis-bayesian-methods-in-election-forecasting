#!/usr/bin/env python

import re
import sys

def input():
  while True:
    try:
      line = sys.stdin.readline()
    except KeyboardInterrupt:
      return

    if not line:
      return
    yield line

# > from sympy.import *
# > x = Symbol('x')
# > Integral(exp(-x**2/2)/sqrt(2*pi), (x, -oo, oo)).evalf()
# 1.0000000000
# > Integral(exp(-x**2/2)/sqrt(2*pi*a), (x, -oo, oo)).evalf()
# NameError: name 'a' is not defined
# > a = 4
# > Integral(exp(-x**2/2)/sqrt(2*pi*a), (x, -oo, oo)).evalf()
# 0.5000000000
#
# > integrate exp(-x**2/2)/sqrt(2*pi) with x, -inf, inf
# 1.0000000000
# > a = 4
# > integrate exp(-x**2/2)/sqrt(2*pi*a) with x, -inf, inf
# 0.5000000000

for line in input():
	line = line.strip()
	m = re.match(r"integrate(\s|$)(.*)", line)
	if m:
		args = m.groups()[1]
	else:
		print "Error!"