import re

token_pat = re.compile("\s*(?:(\d+)|(\w+)|(.))")

def tokenize(program):
    for number, word, operator in token_pat.findall(program):
        if number:
            yield number_token(number)
        elif word:
            yield word_token(word)
        elif operator == "+":
            yield add_token()
        elif operator == "-":
            yield sub_token()
        elif operator == "*":
            yield mul_token()
        elif operator == "/":
            yield div_token()
        elif operator == "^":
            yield pow_token()
        elif operator == '(':
            yield lparen_token()
        elif operator == ')':
            yield rparen_token()
        else:
            raise SyntaxError('unknown operator: %s', operator)
    yield end_token()


class Parser:
    def __init__(self, tokens):
        self.tokens = tokens
        self.token = None

    def next(self):
        self.token = self.tokens.next()
        return self.token

    def expression(self, rbp=0):
        if not self.token: self.next()
        t = self.token
        self.next()
        left = t.nud(self)
        while rbp < self.token.lbp:
            t = self.token
            self.next()
            left = t.led(self, left)
        return left

    def match(self, kind=None):
        if kind and kind != type(self.token):
            raise SyntaxError('Expected %s, got %s' % (kind, self.token))
        self.next()

class number_token(object):
    def __init__(self, value):
        self.value = int(value)
    def nud(self, parser):
        return str(self.value)

class word_token(object):
    def __init__(self, word):
        self.word = word
    def nud(self, parser):
        return self.word

class add_token(object):
    lbp = 10
    def nud(self, parser):
        return "+%s" % parser.expression(100)
    def led(self, parser, left):
        right = parser.expression(10)
        return "%s + %s" % (left, right)

class sub_token(object):
    lbp = 10
    def nud(self, parser):
        return "-%s" % parser.expression(100)
    def led(self, parser, left):
        return "%s - %s" % (left, parser.expression(10))

class mul_token(object):
    lbp = 20
    def led(self, parser, left):
        return "%s * %s" % (left, parser.expression(20))

class div_token(object):
    lbp = 20
    def led(self, parser, left):
        return "%s / %s" % (left, parser.expression(20))

class pow_token(object):
    lbp = 30
    def led(self, parser, left):
        return "%s ^ %s" % (left, parser.expression(30 - 1))

class lparen_token(object):
    lbp = 0
    def nud(self, parser):
        expr = parser.expression()
        parser.match(rparen_token)
        return "(%s)" % expr

class rparen_token(object):
    lbp = 0

class end_token(object):
    lbp = 0


def parse(program):
    tokens = tokenize(program)
    parser = Parser(tokens)
    return parser.expression()

import signal
def int_handler(signum=None, frame=None):
    print
    exit()
# Handle CTRL-C
signal.signal(signal.SIGINT, int_handler)

def input():
    import readline
    while 1:
        try:
            line = raw_input('> ')
        except EOFError:
            # Handle CTRL-D
            int_handler()
        yield line

def error(msg):
    print "[Error] %s" % msg

print "Loading sympy..."
import sympy

variables = {}

for line in input():
    line = line.strip()
    if line == "exit" or line == "quit":
        break
    if len(line) == 0:
        continue
    integrate_m = re.search(r'^integrate(\s|$)(.*)', line)
    assign_m = re.search(r'^(\w+)\s*=\s*(\d+)$', line)
    getvar_m = re.search(r'^(\w+)$', line)
    if integrate_m:
        rest = integrate_m.groups()[1].strip()
        m = re.search(r'^(.*)\s+with\s+(\w+)\s*,\s*([-\w]+)\s*,\s*([-\w]+)', rest)
        if m:
            expr, var, a, b = m.groups()
            expr = sympy.S(expr)
            for k, v in variables.items():
                expr = expr.subs(k, v)
            a = sympy.S(a)
            b = sympy.S(b)
            a = a.subs('inf', sympy.oo)
            b = b.subs('inf', sympy.oo)
            print sympy.Integral(expr, (var, a, b)).evalf()
        else:
            error("integrate EXPR with VAR,A,B")
    elif getvar_m:
        var = getvar_m.groups()[0]
        if var in variables:
            print variables[var]
        else:
            error("unassigned variable '%s'" % var)
    elif assign_m:
        var, value = assign_m.groups()
        variables[var] = sympy.S(value)
        print value
    else:
        error("unrecognized command '%s'" % line)

