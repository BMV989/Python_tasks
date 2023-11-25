#!/usr/bin/env python

import sys


def f0():
    sys.exit(1)
    # raise BaseException


def f1():
    return "aboba" + 4
    # raise Exception


def f2():
    return 100 % 0
    # raise ArithmeticError


def f3():
    # https://docs.python.org/3.12/library/exceptions.html#FloatingPointError
    # exception FloatingPointError Not currently used.
    raise FloatingPointError


def f4():
    import math
    number = 1e10
    return math.exp(number)
    # raise OverflowError


def f5():
    return 1 / 0
    # raise ZeroDivisionError


def f6():
    assert 5 == 4
    # raise AssertionError


def f7():
    from collections import namedtuple
    Marks = namedtuple('Marks', 'Physics Chemistry Math English')
    marks = Marks(90, 85, 95, 100)
    marks.Chemistry = 100
    return marks
    # raise AttributeError


def f8():
    return open("XXX.XXX.XXX.XXX.XXX", "r")
    # raise EnvironmentError


def f9():
    import aboba
    # raise ImportError


def f10():
    dictionary = {1: 'a', 2: 'b', 3: 'c'}
    return dictionary[6]
    # raise LookupError


def f11():
    color = ['red', 'blue', 'green', 'black', 'white', 'orange']
    return color[6]
    # raise IndexError


def f12():
    ages = {'John': 19, 'Mike': 21, 'Kevin': 20}
    return ages['Markus']
    # raise KeyError


def f13():
    принт("Привет мир!")
    # raise NameError


def f14():
    compile("GG!!!!", filename="FF!!!!", mode="exec")
    # raise SyntaxError


def f15():
    return int("number")
    # raise ValueError


def f16():
    word = 'café'
    return "ASCII Representation of café: ", word.encode('ascii')
    # raise UnicodeError


def check_exception(f, exception):
    try:
        f()
    except exception:
        pass
    else:
        print("Bad luck, no exception caught: %s" % exception)
        sys.exit(1)


check_exception(f0, BaseException)
check_exception(f1, Exception)
check_exception(f2, ArithmeticError)
check_exception(f3, FloatingPointError)
check_exception(f4, OverflowError)
check_exception(f5, ZeroDivisionError)
check_exception(f6, AssertionError)
check_exception(f7, AttributeError)
check_exception(f8, EnvironmentError)
check_exception(f9, ImportError)
check_exception(f10, LookupError)
check_exception(f11, IndexError)
check_exception(f12, KeyError)
check_exception(f13, NameError)
check_exception(f14, SyntaxError)
check_exception(f15, ValueError)
check_exception(f16, UnicodeError)

print("Congratulations, you made it!")
