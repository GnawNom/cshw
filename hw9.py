#Name: Joe Wang
#Login:cs61a-yb
#Section/GSI:115/Hamilton Nguyen
from ucb import *
"""Homework 9: Trees, Exceptions, and Calculator"""

"""1) A mobile is a type of hanging sculpture. For example, the mobile linked
below was created by Julie Frith: http://goo.gl/jJatN

A simple binary mobile consists of two branches, left and right. Each branch is
a rod of a certain length, from which hangs either a weight or another mobile.

Improve the classes for Branch, Weight, and Mobile below in the following ways:

  A) The left and right attributes of a Mobile should both be Branch instances.
  Check that the types of constructor arguments for Mobile are Branch
  instances, and raise an appropriate TypeError for incorrect argument types.
  See the doctest for Mobile for exception details.

  B) The length of a Branch and the weight of a Weight should be positive
  numbers. Implement check_positive to check if an object x is a positive
  number.
  
  D) Add a property weight that gives the total weight of the mobile.

  E) A mobile is said to be balanced if the torque applied by its left branch
  is equal to that applied by its right branch (that is, if the length of the
  left rod multiplied by the weight hanging from that rod is equal to the
  corresponding product for the right side) and if each of the submobiles
  hanging off its branches is balanced. Add a property method isbalanced that
  returns True if and only if the Mobile is balanced.
"""

class Mobile(object):
    """A simple binary mobile that has branches of weights or other mobiles.
    
    >>> Mobile(1, 2)
    Traceback (most recent call last):
        ...
    TypeError: 1 is not a Branch
    >>> m = Mobile(Branch(1, Weight(2)), Branch(2, Weight(1)))
    >>> m.weight
    3
    >>> m.isbalanced
    True
    >>> m.left.contents = Mobile(Branch(1, Weight(1)), Branch(2, Weight(1)))
    >>> m.weight
    3
    >>> m.left.contents.isbalanced
    False
    >>> m.isbalanced # All submobiles must be balanced for m to be balanced
    False
    >>> m.left.contents.right.contents.weight = 0.5
    >>> m.left.contents.isbalanced
    True
    >>> m.isbalanced
    False
    >>> m.right.length = 1.5
    >>> m.isbalanced
    True
    """

    def __init__(self, left, right):
        "*** YOUR CODE HERE ***"
        if type(left) != Branch:
            raise TypeError(str(left)+' is not a Branch')
        if type(right) != Branch:
            raise TypeError(str(right)+' is not a Branch')
        self.left = left
        self.right = right

    @property
    def weight(self):
        """The total weight of the mobile."""
        "*** YOUR CODE HERE ***"
        return self.left.contents.weight+self.right.contents.weight

    @property
    def isbalanced(self):
        """True if and only if the mobile is balanced."""
        "*** YOUR CODE HERE ***"
        if type(self.left.contents)==Weight and type(self.right.contents)==Weight:
            return self.left.torque==self.right.torque
        else:
            return self.left.contents.isbalanced and self.right.contents.isbalanced and(self.left.torque==self.right.torque)
        

def check_positive(x):
    """Check that x is a positive number, and raise an exception otherwise.
    
    >>> check_positive('hello')
    Traceback (most recent call last):
    ...
    TypeError: hello is not a number
    >>> check_positive('1')
    Traceback (most recent call last):
    ...
    TypeError: 1 is not a number
    >>> check_positive(-2)
    Traceback (most recent call last):
    ...
    ValueError: -2 <= 0
    """
    "*** YOUR CODE HERE ***"
    if type(x) not in (float, int):
        raise TypeError(str(x)+' is not a number')
    elif x<=0:
        raise ValueError(str(x)+' <= 0')


class Branch(object):
    """A branch of a simple binary mobile."""

    def __init__(self, length, contents):
        if type(contents) not in (Weight, Mobile):
            raise TypeError(str(contents) + ' is not a Weight or Mobile')
        check_positive(length)
        self.length = length
        self.contents = contents

    @property
    def torque(self):
        """The torque on the branch"""
        return self.length * self.contents.weight


class Weight(object):
    """A weight."""
    def __init__(self, weight):
        check_positive(weight)
        self.weight = weight
        self.isbalanced = True

"""2) Your partner designed a beautiful balanced Mobile, but forgot to fill in
the classes of each part, instead just writing T.

T(T(4,T(T(4,T(1)),T(1,T(4)))),T(2,T(10)))

The built-in Python funciton eval takes a string argument, evaluates it as a
Python expression, and returns its value.

>>> eval('2+2')
4
>>> eval('Weight(3)').isbalanced
True

Complete the definition of interpret_mobile so that it returns a well-formed
mobile by guessing the class for each T. The function should exhaustively test
all possible combinations of types, handling TypeErrors until a correct series
of types is found.

Warning: Interpreting a large mobile is quite slow (can you say why?).  You
will want to remove the doctest for the large mobile during development.
"""
@trace
def interpret_mobile(s):
    """Return a Mobile described by string s by substituting one of the classes
    Branch, Weight, or Mobile for each occurrenct of the letter T.

    >>> simple = 'Mobile(T(2,T(1)), T(1,T(2)))'
    >>> interpret_mobile(simple).weight
    3
    >>> interpret_mobile(simple).isbalanced
    True
    >>> s = 'T(T(4,T(T(4,T(1)),T(1,T(4)))),T(2,T(10)))'
    >>> m = interpret_mobile(s)
    >>> m.weight
    15
    >>> m.isbalanced
    True
    """
    next_T = s.find('T')
    if next_T == -1: # The string 'T' was not found in s
        "*** YOUR CODE HERE ***"
        
        try:
            return eval(s)
        except TypeError:
            return None
    for t in ('Branch', 'Weight', 'Mobile'):
        substituted = s[:next_T] + t + s[next_T+1:] # substitute 'T' with t
        "*** YOUR CODE HERE ***"
        substituted=interpret_mobile(substituted)
        if type(substituted)==Mobile:
            return substituted
        
    return None

"""3) Complete the definition of a function subsets that returns a list of all
subsets of a set s.  Each subset should itself be a set. The solution can be
expressed in a single line (although a multi-line solution is fine)."""

def subsets(s):
    """Return a list of the subsets of s.

    >>> subsets({True, False})
    [{False, True}, {False}, {True}, set()]
    >>> counts = {x for x in range(10)} # A set comprehension
    >>> subs = subsets(counts)
    >>> len(subs)
    1024
    >>> counts in subs
    True
    >>> len(counts)
    10
    """
    assert type(s) == set, str(s) + ' is not a set.'
    if not s:
        return [set()]
    element = s.pop() # Remove an element
    rest = subsets(s) # Find all subsets of the remaining elements
    s.add(element)    # Add the element back, so that s is unchanged
    "*** YOUR CODE HERE ***"
    if len(s)==1:
        return [{element}]+rest
    return [s]+[{element}]+rest
"""4) Extra for experts.  Using reduce and lambda, define subsets using a
one-line return statement.

Note: The function name was changed and doctests were added on 10/31.
"""

from functools import reduce

def subsets_for_experts(s):
    """Return a list of the subsets of s.

    >>> counts = {x for x in range(10)} # A set comprehension
    >>> subs = subsets_for_experts(counts)
    >>> len(subs)
    1024
    >>> counts in subs
    True
    >>> len(counts)
    10
    """
    "*** YOUR CODE HERE ***"
    

"""5) Required for everyone. Extend the calculator program from lecture, copied
below, to include a new operator, word, that concatenates the string
representations of two numeric arguments and treats the result as a number.
Word takes exactly two arguments.  The operator should raise a TypeError
whenever the result of concatenation cannot be interpreted as a number.

Also, complete the function calc_test to verify that your changes do what they
are meant to do. In this test, you will consider a series of Calculator
expressions.  For each one, the following line gives the target result.
Compute the result that would be printed by the Calculator REPL and compare it
to the target.
"""

def calc_test():
    """Verify that the word operator and comma-free syntax work as expected."""
    examples = """
      calc> add(1, 2)
      3
      calc> add(1, mul(2, 3))
      7

      calc> word(12, 34)
      1234
      calc> word(-5, 67.8)
      -567.8
      calc> add(5, word(6, 7))
      72

      calc> word(1)
      TypeError: word requires exactly 2 arguments
      calc> word(-1, -1)
      TypeError: -1-1 is not a well-formed number
      calc> word(0.2, 0.2)
      TypeError: 0.20.2 is not a well-formed number
    """.split('\n')
    while examples:
        line = examples.pop(0).strip()
        if not line:
            continue
        assert line.startswith('calc> '), 'Malformed calc test ' + line
        calc_expression = line[6:]
        target = examples.pop(0).strip()
        result = None # Construct what would have been printed by the REPL
        "*** YOUR CODE HERE ***"
        assert result == target, result + ' is not ' + target

from operator import mul

def read_eval_print_loop():
    """Run a read-eval-print loop for calculator."""
    while True:
        try:
            expression_tree = calc_parse(input('calc> '))
            print(calc_eval(expression_tree))
        except (SyntaxError, TypeError, ZeroDivisionError) as err:
            print(type(err).__name__ + ':', err)
        except (KeyboardInterrupt, EOFError):  # <Control>-D, etc.
            print('Calculation completed.')
            return

# Eval & Apply

class Exp(object):
    """A call expression in Calculator.
    
    >>> Exp('add', [1, 2])
    Exp('add', [1, 2])
    >>> str(Exp('add', [1, Exp('mul', [2, 3])]))
    'add(1, mul(2, 3))'
    """

    def __init__(self, operator, operands):
        self.operator = operator
        self.operands = operands

    def __repr__(self):
        return 'Exp({0}, {1})'.format(repr(self.operator), repr(self.operands))

    def __str__(self):
        operand_strs = ', '.join(map(str, self.operands))
        return '{0}({1})'.format(self.operator, operand_strs)

def calc_eval(exp):
    """Evaluate a Calculator expression.

    >>> calc_eval(Exp('add', [2, Exp('mul', [4, 6])]))
    26
    """
    if type(exp) in (int, float):
        return exp
    if type(exp) == Exp:
        arguments = list(map(calc_eval, exp.operands))
        return calc_apply(exp.operator, arguments)

def calc_apply(operator, args):
    """Apply the named operator to a list of args.
    
    >>> calc_apply('+', [1, 2, 3])
    6
    >>> calc_apply('-', [10, 1, 2, 3])
    4
    >>> calc_apply('*', [])
    1
    >>> calc_apply('/', [40, 5])
    8.0
    """
    if operator in ('add', '+'):
        return sum(args)
    if operator in ('sub', '-'):
        if len(args) == 0:
            raise TypeError(operator + 'requires at least 1 argument')
        if len(args) == 1:
            return -args[0]
        return sum(args[:1] + [-arg for arg in args[1:]])
    if operator in ('mul', '*'):
        return reduce(mul, args, 1)
    if operator in ('div', '/'):
        if len(args) != 2:
            raise TypeError(operator + ' requires exactly 2 arguments')
        numer, denom = args
        return numer/denom
    if operator == 'word':
        "*** YOUR CODE HERE ***"
    
# Parsing (NO CHANGES ARE REQUIRED TO THIS PART OF CALCULATOR)

def calc_parse(line):
    """Parse a line of calculator input and return an expression tree."""
    tokens = tokenize(line)
    expression_tree = analyze(tokens)
    if len(tokens) > 0:
        raise SyntaxError('Extra token(s): ' + ' '.join(tokens))
    return expression_tree

def tokenize(line):
    """Convert a string into a list of tokens.
    
    >>> tokenize('add(2, mul(4, 6))')
    ['add', '(', '2', ',', 'mul', '(', '4', ',', '6', ')', ')']
    """
    spaced = line.replace('(',' ( ').replace(')',' ) ').replace(',', ' , ')
    return spaced.strip().split()

known_operators = ['add', 'sub', 'mul', 'div', '+', '-', '*', '/', 'word']

def analyze(tokens):
    """Create a tree of nested lists from a sequence of tokens.

    Operand expressions can be separated by commas, spaces, or both.
    
    >>> analyze(tokenize('add(2, mul(4, 6))'))
    Exp('add', [2, Exp('mul', [4, 6])])
    >>> analyze(tokenize('mul(add(2, mul(4, 6)), add(3, 5))'))
    Exp('mul', [Exp('add', [2, Exp('mul', [4, 6])]), Exp('add', [3, 5])])
    """
    assert_non_empty(tokens)
    token = analyze_token(tokens.pop(0))
    if type(token) in (int, float):
        return token
    if token in known_operators:
        if len(tokens) == 0 or tokens.pop(0) != '(':
            raise SyntaxError('expected ( after ' + token)
        return Exp(token, analyze_operands(tokens))
    else:
        raise SyntaxError('unexpected ' + token)

def analyze_operands(tokens):
    """Analyze a sequence of comma-separated operands."""
    assert_non_empty(tokens)
    operands = []
    while tokens[0] != ')':
        if operands and tokens.pop(0) != ',':
            raise SyntaxError('expected ,')
        operands.append(analyze(tokens))
        assert_non_empty(tokens)
    tokens.pop(0)  # Remove )
    return operands

def assert_non_empty(tokens):
    """Raise an exception if tokens is empty."""
    if len(tokens) == 0:
        raise SyntaxError('unexpected end of line')

def analyze_token(token):
    """Return the value of token if it can be analyzed as a number, or token.
    
    >>> analyze_token('12')
    12
    >>> analyze_token('7.5')
    7.5
    >>> analyze_token('add')
    'add'
    """
    try:
        return int(token)
    except (TypeError, ValueError):
        try:
            return float(token)
        except (TypeError, ValueError):
            return token
