import numpy as np
from functools import reduce
import operator
import collections.abc

def _coef(coefficient, degree, variable="x"):
    if coefficient == 0:
        return ""
    to_print = ""
    if coefficient != 1:
        to_print += str(coefficient)
    if degree == 0:
        return to_print
    elif degree == 1:
        return to_print + variable
    else:
        return to_print + variable + "^" + str(degree)

# is this the best type to inherit?
class Poly(collections.abc.Iterable):

    def __iter__(self):
        # if it works
        return iter(self.coefficients)

    def __getitem__(self, item):
        return self.coefficients[item]
    @staticmethod
    def horner(x):
        # make function?
        return lambda a, b: x * a + b

    __slots__ = ("coefficients", "degree", "coefficientType")

    def __init__(self, coefficientList):
        self.coefficients = np.trim_zeros(np.array(coefficientList), trim="b")
        self.degree = len(self.coefficients) - 1
        self.coefficientType = None  # TODO: dynamically determine type of coefficeints from args

    def __add__(self, second):
        if isinstance(second, (int, np.signedinteger)):
            temp = self.coefficients
            temp[0] += second
            return Poly(temp)
        temp2 = self
        if self.degree < second.degree:
            temp2, second = second, self
        return Poly(self.coefficients +
                    np.pad(second.coefficients, (0, temp2.degree - second.degree)))

    def __mul__(self, second):
        if isinstance(second, (int, np.signedinteger)):
            return Poly(self.coefficients * second)
        maxLength = max(self.degree, second.degree) + 1
        powTwo = 1
        while powTwo < maxLength:
            powTwo *= 2
        return Poly(self._karatsuba(np.pad(self.coefficients, (0, powTwo - self.degree - 1)),
                                    np.pad(second.coefficients, (0, powTwo - second.degree - 1))))

    @staticmethod
    def _karatsuba(first, second):
        length = len(first)
        if length == 1:
            return np.array([first[0] * second[0]])
        else:
            temp1 = np.split(first, 2)
            temp2 = np.split(second, 2)
            a = Poly._karatsuba(temp1[0], temp2[0])
            c = Poly._karatsuba(temp1[1], temp2[1])
            b = Poly._karatsuba(temp1[0] + temp1[1], temp2[0] + temp2[1]) - a - c
            return (np.pad(a, (0, length)) +
                    np.pad(b, (length // 2, length // 2)) +
                    np.pad(c, (length, 0)))

    def __len__(self):
        return self.degree + 1

    def __call__(self, x):
        return reduce(self.horner(x), self.coefficients[::-1])

    def __repr__(self):
        if self.degree == 0:
            return str(self.coefficients[0])
        toPrint = []
        for i in range(0, self.degree + 1):
            toPrint += [_coef(self.coefficients[i], i) + (self.coefficients[i] != 0) * "+"]
            print(toPrint)
        return reduce(operator.add, toPrint[::-1])[:-1]

    def __hash__(self):
        return hash(tuple(self.coefficients))

    def derivative(self, degree=1):
        if not isinstance(degree, (int, np.signedinteger)):
            raise TypeError("Can only take derivative whole number of times")
        elif degree < 0:
            raise ValueError("Consider using integrals")

        if degree == 0:
            return self
        else:
            for i in range(1, self.degree + 1):
                self.coefficients[i] *= i
            self.coefficients = self.coefficients[1:]
            self.degree -= 1
            return self.derivative(degree - 1)

    @classmethod
    def derive(cls, self, degree=1):
        if not isinstance(degree, (int, np.signedinteger)):
            raise TypeError("Can only take derivative whole number of times")
        elif degree < 0:
            return Poly.integrate(self, -degree)

        return Poly._derive(self.coefficients.copy(), degree)

    @classmethod
    def _derive(cls, coef, degree):
        if degree == 0:
            return Poly(coef)
        else:
            for i in range(1, len(coef)):
                coef[i] *= i
            return Poly._derive(coef[1:], degree - 1)

    @classmethod
    def integrate(cls, poly, degree=1):
        if not isinstance(degree, (int, np.signedinteger)):
            raise TypeError("Can only take derivative whole number of times")
        elif degree < 0:
            return Poly.derive(poly, -degree)
        return Poly._integrate(poly.coefficients.copy(), degree)

    @classmethod
    def _integrate(cls, coef, degree):
        if degree == 0:
            return Poly(coef)
        else:
            for i in range(0, len(coef)):
                coef[i] /= i + 1
            return Poly._integrate(np.pad(coef, (1, 0)), degree - 1)