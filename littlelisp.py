#!/usr/bin/env python

from collections import namedtuple
import pprint

indent = '    '


def tokenize(code):
    """
    >>> tokenize('((x))')
    ['(', '(', 'x', ')', ')']

    >>> tokenize('((lambda (x) x) "Lisp")')
    ['(', '(', 'lambda', '(', 'x', ')', 'x', ')', '"Lisp"', ')']
    """
    code = code.replace("(", " ( ")
    code = code.replace(")", " ) ")
    code = code.strip()
    tokens = code.split(" ")
    return [token for token in tokens if token]


class types:
    LITERAL = 'literal'
    IDENTIFIER = 'identifier'

Atom = namedtuple("Atom", ["type", "value"])


def categorize(code):
    """
    >>> categorize("1")
    Atom(type='literal', value=1.0)

    >>> categorize('"tester"')
    Atom(type='literal', value='tester')

    >>> categorize('lambda')
    Atom(type='identifier', value='lambda')
    """
    try:
        return Atom(types.LITERAL, float(code))
    except ValueError:
        pass

    if code[0] == '"' and code[-1] == '"':
        return Atom(types.LITERAL, code[1:-1])
    else:
        return Atom(types.IDENTIFIER, code)


def parenthesize(tokens, _list=None, recur=0):
    """
    >>> parenthesize(['(', '(', 'lambda', '(', 'x', ')', 'x', ')', '"Lisp"', ')'])
    [[Atom(type='identifier', value='lambda'), [Atom(type='identifier', value='x')], Atom(type='identifier', value='x')], Atom(type='literal', value='Lisp')]

    >>> parenthesize(['(', '(', 'x', ')', ')'])
    [[Atom(type='identifier', value='x')]]
    """
    # print indent*recur +"parenthesize({0}, {1})".format(tokens, _list)

    if _list == None:
        return parenthesize(tokens, [], recur + 1)
    else:
        token = None
        if tokens:
            token = tokens.pop(0)
        # print indent*recur +"Token: {0}".format(token)

        if token == None:
            return _list.pop()
        elif token == "(":
            # import ipdb; ipdb.set_trace()
            _list += [parenthesize(tokens, [], recur + 1)]
            return parenthesize(tokens, _list, recur + 1)
        elif token == ")":
            return _list
        else:
            _list += [categorize(token)]
            return parenthesize(tokens, _list, recur + 1)


def parse(code):
    """
    >>> parse('((lambda (x) x) "Lisp")')
    [[Atom(type='identifier', value='lambda'), [Atom(type='identifier', value='x')], Atom(type='identifier', value='x')], Atom(type='literal', value='Lisp')]
    """
    return parenthesize(tokenize(code))


class Context(object):
    def __init__(self, scope, parent=None):
        self.scope = scope
        self.parent = parent

    def __getitem__(self, identifier):
        """
        >>> c1 = Context({"a":1})
        >>> c2 = Context({"b":2}, c1)
        >>> c2["a"]
        1
        """
        if identifier in self.scope:
            return self.scope[identifier]
        elif self.parent:
            return self.parent[identifier]


code = '((lambda (x) x) "Lisp")'

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    import sys

    pprint.pprint(parse(''.join(sys.argv[1:])))
