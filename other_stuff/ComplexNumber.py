from __future__ import annotations
import unittest


class ComplexNumber:
    def __init__(self, re: float, im: float):
        self.re = re
        self.im = im

    def __add__(self, other: ComplexNumber) -> ComplexNumber:
        return ComplexNumber(self.re + other.re, self.im + other.im)

    def __sub__(self, other: ComplexNumber) -> ComplexNumber:
        return ComplexNumber(self.re - other.re, self.im - other.im)

    def __mul__(self, other: ComplexNumber) -> ComplexNumber:
        return ComplexNumber(self.re * other.re -
                             self.im * other.im, self.re *
                             other.im + self.im * other.re)

    def __neg__(self) -> ComplexNumber:
        return ComplexNumber(-self.re, -self.im)

    def __eq__(self, other: ComplexNumber) -> bool:
        return self.re == other.re and self.im == other.im

    def __hash__(self) -> int:
        return hash((self.re, self.im))

    def __radd__(self, other: ComplexNumber) -> ComplexNumber:
        return self.__add__(other)


class ComplexNumberTest(unittest.TestCase):
    def test_add(self):
        c1 = ComplexNumber(2.2, 2.2)
        c2 = ComplexNumber(2.2, 2.3)
        res = c1 + c2
        self.assertEqual(res.re, 4.4)
        self.assertEqual(res.im, 4.5)

    def test_neg(self):
        c1 = ComplexNumber(1, 2)
        res = -c1
        self.assertEqual(res.re, -1)
        self.assertEqual(res.im, -2)

    def test_eq(self):
        c1 = c2 = ComplexNumber(1, 2)
        res = c1 == c2
        self.assertEqual(res, True)

    def test_sub(self):
        c1 = ComplexNumber(5, -6)
        c2 = ComplexNumber(-3, 2)
        res = c1 - c2
        self.assertEqual(res.re, 8)
        self.assertEqual(res.im, -8)

    def test_mul(self):
        c1 = ComplexNumber(2, 3)
        c2 = ComplexNumber(-1, 1)
        res = c1 * c2
        self.assertEqual(res.re, -5)
        self.assertEqual(res.im, -1)


if __name__ == '__main__':
    unittest.main()
