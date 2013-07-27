#!/usr/bin/env python

from collections import namedtuple
import pprint

indent = '    '

def tokenize(code):
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
    #print indent*recur +"parenthesize({0}, {1})".format(tokens, _list)
    
    if _list == None:
        return parenthesize(tokens, [], recur+1)
    else:
        token = None
        if tokens:
            token = tokens.pop(0)
        #print indent*recur +"Token: {0}".format(token)

        if token == None:
            return _list.pop()
        elif token == "(":
            #import ipdb; ipdb.set_trace()
            _list += [parenthesize(tokens, [], recur+1)]
            return parenthesize(tokens, _list, recur+1)
        elif token == ")":
            return _list
        else:
            _list += [categorize(token)]
            return parenthesize(tokens, _list, recur+1)


code = '((lambda (x) x) "Lisp")'

if __name__ == "__main__":
    import doctest
    doctest.testmod()

    import sys

    tokens = tokenize(''.join(sys.argv[1:]))
    pprint.pprint(tokens)

    print "#"*10

    parentheses = parenthesize(tokens)
    pprint.pprint(parentheses)
